
resource "aws_vpc_ipv4_cidr_block_association" "aviatrix_cidr" {
  count      = var.add_vpc_cidr ? 1 : 0
  vpc_id     = var.vpc_id
  cidr_block = var.avtx_cidr
}

resource "aws_internet_gateway" "IGW" {
  count  = length(var.igw_id) > 3 ? 0 : 1
  vpc_id = var.vpc_id
  tags = {
    Name = "aviatrix-${var.vpc_name}"
  }
}

resource "aws_subnet" "aviatrix_public" {
  count             = var.add_vpc_cidr ? (var.hpe ? 0 : 2) : 0
  vpc_id            = var.vpc_id
  cidr_block        = cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr[0].cidr_block, 1, count.index)
  availability_zone = var.gw_zones[count.index]
  tags = {
    Name = count.index == 0 ? "aviatrix-${var.vpc_name}-gw" : "aviatrix-${var.vpc_name}-gw-hagw"
  }
}

resource "aws_route_table" "aviatrix_public" {
  count  = var.add_vpc_cidr ? (var.hpe ? 0 : 1) : 0
  vpc_id = var.vpc_id
  tags = {
    Name = "aviatrix-${var.vpc_name}-gw"
  }
}

resource "aws_route" "aviatrix_default" {
  count                  = var.add_vpc_cidr ? (var.hpe ? 0 : 1) : 0
  route_table_id         = aws_route_table.aviatrix_public[0].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = var.igw_id == "" ? aws_internet_gateway.IGW[0].id : var.igw_id
}

resource "aws_route_table_association" "aviatrix_public" {
  count          = var.add_vpc_cidr ? (var.hpe ? 0 : 2) : 0
  subnet_id      = aws_subnet.aviatrix_public[count.index].id
  route_table_id = aws_route_table.aviatrix_public[0].id
}

resource "aviatrix_spoke_gateway" "gw" {
  cloud_type                        = 1
  account_name                      = var.account_name
  gw_name                           = var.spoke_gw_name
  vpc_id                            = var.vpc_id
  vpc_reg                           = var.region
  insane_mode                       = var.hpe
  gw_size                           = var.avtx_gw_size
  ha_gw_size                        = var.avtx_gw_size
  subnet                            = var.add_vpc_cidr ? cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr[0].cidr_block, 1, 0) : split(",", var.avtx_cidr)[0]
  ha_subnet                         = var.add_vpc_cidr ? cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr[0].cidr_block, 1, 1) : split(",", var.avtx_cidr)[1]
  insane_mode_az                    = var.hpe ? var.gw_zones[0] : null
  ha_insane_mode_az                 = var.hpe ? var.gw_zones[1] : null
  included_advertised_spoke_routes  = var.switch_traffic ? (var.add_vpc_cidr ? (length(var.spoke_adv) > 0 ? var.spoke_adv : join(",", concat(var.vpc_cidr, [var.avtx_cidr]))) : (length(var.spoke_adv) > 0 ? var.spoke_adv : join(",", var.vpc_cidr))) : var.avtx_cidr
  customized_spoke_vpc_routes       = var.spoke_routes
  manage_transit_gateway_attachment = false
  enable_active_mesh                = true
  single_az_ha                      = true
  tags                              = var.tags
  depends_on                        = [aws_route.aviatrix_default, aws_route_table_association.aviatrix_public, aws_route.pre_migration]
}

resource "aviatrix_spoke_transit_attachment" "attachment" {
  spoke_gw_name   = aviatrix_spoke_gateway.gw.gw_name
  transit_gw_name = var.transit_gw
  route_tables    = [for k, v in var.route_tables : aws_route_table.aviatrix_managed[k].id]
}

resource "aws_route_table" "aviatrix_managed" {
  for_each = var.route_tables
  vpc_id   = var.vpc_id
  tags     = merge(each.value.tags, { Org_RT = each.key })
}

resource "aviatrix_transit_firenet_policy" "default" {
  count                        = var.inspection ? 1 : 0
  transit_firenet_gateway_name = var.transit_gw
  inspected_resource_name      = "SPOKE:${aviatrix_spoke_gateway.gw.gw_name}"
  depends_on                   = [aviatrix_spoke_transit_attachment.attachment]
}

resource "aviatrix_segmentation_security_domain_association" "default" {
  count                = length(var.domain) > 0 ? 1 : 0
  transit_gateway_name = var.transit_gw
  security_domain_name = var.domain
  attachment_name      = aviatrix_spoke_gateway.gw.gw_name
  depends_on           = [aviatrix_spoke_transit_attachment.attachment]
}


resource "aws_route" "pre_migration" {
  for_each = {
    for route in local.routes : "${route.destination}.${route.key}" => route
    if substr(route["target"], 0, 5) != "vpce-"
  }
  route_table_id            = aws_route_table.aviatrix_managed[each.value.key].id
  destination_cidr_block    = each.value.destination
  gateway_id                = split("-", each.value.target)[0] == "igw" ? each.value.target : null
  instance_id               = split("-", each.value.target)[0] == "i" ? each.value.target : null
  nat_gateway_id            = split("-", each.value.target)[0] == "nat" ? each.value.target : null
  local_gateway_id          = split("-", each.value.target)[0] == "Igw" ? each.value.target : null # outpost gateway
  network_interface_id      = split("-", each.value.target)[0] == "eni" ? each.value.target : null
  vpc_peering_connection_id = split("-", each.value.target)[0] == "pcx" ? each.value.target : null

  # VPC gateway endpoints routes can't be added here, endpoint manages RTs

}

resource "null_resource" "vpce_route" {
  for_each = {
    for route in local.routes : "${route.destination}.${route.key}" => route
    if substr(route["target"], 0, 5) == "vpce-"
  }
  provisioner "local-exec" {
    command = "python3 -m dm.add_vpce_route ${var.region} ${var.role_arn} ${each.value["target"]} ${aws_route_table.aviatrix_managed[each.value.key].id}"
  }
}

locals {
  routes = flatten([
    for rt_key, rt_val in var.route_tables : [
      for route in rt_val.routes : {
        key         = rt_key
        destination = route.destination
        target      = route.target
      }
    ]
  ])
}
