{% if data.add_vpc_cidr %}
resource "aws_vpc_ipv4_cidr_block_association" "aviatrix_cidr" {
  vpc_id     = var.vpc_id
  cidr_block = var.avtx_cidr
}
{% endif %}

resource "aws_internet_gateway" "IGW" {
  count  = var.igw_id == "" ? 1 : 0
  vpc_id = var.vpc_id
  tags = {
    Name                        = "aviatrix-${var.vpc_name}"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }
}

resource "aws_subnet" "aviatrix_public" {
  count             = var.hpe ? 0 : 2
  vpc_id            = var.vpc_id
{% if data.add_vpc_cidr %}
  cidr_block        = cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr.cidr_block, 1, count.index)
{% else %}
  cidr_block        = cidrsubnet(var.avtx_cidr, 1, count.index)
{% endif %}
  availability_zone = var.gw_zones[count.index]
  tags = {
    Name                        = count.index == 0 ? "aviatrix-${var.vpc_name}-gw" : "aviatrix-${var.vpc_name}-gw-hagw"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }
}

resource "aws_route_table" "aviatrix_public" {
  count  = var.hpe ? 0 : 1
  vpc_id = var.vpc_id
  tags = {
    Name                        = "aviatrix-${var.vpc_name}-gw"
    "Aviatrix-Created-Resource" = "Do-Not-Delete-Aviatrix-Created-Resource"
  }
}

resource "aws_route" "aviatrix_default" {
  count                  = var.hpe ? 0 : 1
  route_table_id         = aws_route_table.aviatrix_public[0].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = var.igw_id == "" ? aws_internet_gateway.IGW[0].id : var.igw_id
}

resource "aws_route_table_association" "aviatrix_public" {
  count          = var.hpe ? 0 : 2
  subnet_id      = aws_subnet.aviatrix_public[count.index].id
  route_table_id = aws_route_table.aviatrix_public[0].id
}

resource "aviatrix_spoke_gateway" "gw" {
  cloud_type                        = 1
  account_name                      = var.account_name
{% if data.configure_gw_name %}
  gw_name                           = var.spoke_gw_name
{% else %}
  gw_name                           = "aws-${local.region[var.region]}-${join("", formatlist("%02x", split(".", split("/", var.avtx_cidr)[0])))}-gw"
{% endif %}
  vpc_id                            = var.vpc_id
  vpc_reg                           = var.region
  insane_mode                       = var.hpe
  gw_size                           = var.avtx_gw_size
  ha_gw_size                        = var.avtx_gw_size
{% if data.add_vpc_cidr %}
  subnet                            = cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr.cidr_block, 1, 0)
  ha_subnet                         = cidrsubnet(aws_vpc_ipv4_cidr_block_association.aviatrix_cidr.cidr_block, 1, 1)
{% else %}
  subnet                            = cidrsubnet(var.avtx_cidr, 1, 0)
  ha_subnet                         = cidrsubnet(var.avtx_cidr, 1, 1)
{% endif %}
  insane_mode_az                    = var.hpe ? var.gw_zones[0] : null
  ha_insane_mode_az                 = var.hpe ? var.gw_zones[1] : null
{% if data.add_vpc_cidr %}
  included_advertised_spoke_routes  = var.switch_traffic ?  join(",", concat(var.vpc_cidr, [var.avtx_cidr])) : var.avtx_cidr
{% elif data.configure_spoke_advertisement %}
  included_advertised_spoke_routes  = var.switch_traffic ? var.spoke_adv != "" ? var.spoke_adv : join(",", var.vpc_cidr): var.avtx_cidr
{% else %}
  included_advertised_spoke_routes  = var.switch_traffic ? join(",", var.vpc_cidr) : var.avtx_cidr
{% endif %}
  customized_spoke_vpc_routes       = var.spoke_routes != "" ? var.spoke_routes : null
  manage_transit_gateway_attachment = false
{% if data.pre_v2_21_0 %}
  enable_active_mesh                = true
{% endif %}
  single_az_ha                      = true
  enable_encrypt_volume             = var.encrypt
  tags                              = var.tags
  depends_on = [aws_route.aviatrix_default, aws_route_table_association.aviatrix_public, aws_route.pre_migration, aws_internet_gateway.IGW]
}

{% if data.enable_spoke_egress %}
resource "aviatrix_gateway_snat" "internet" {
  count = var.enable_spoke_egress ? (var.switch_traffic ? 2 : 0) : 0

  gw_name    = count.index == 0 ? aviatrix_spoke_gateway.gw.gw_name : aviatrix_spoke_gateway.gw.ha_gw_name
  snat_mode  = "customized_snat"
  sync_to_ha = false
  {% for policy in data.snat_policies %}
  snat_policy {
    {% if policy.src_ip %}
    src_cidr          = "{{policy.src_ip}}"
    {% endif %}
    {% if policy.src_port %}
    src_port          = "{{policy.src_port}}"
    {% endif %}
    {% if policy.dst_ip %}
    dest_cidr         = "{{policy.dst_ip}}"_ip
    {% endif %}
    {% if policy.dst_port %}
    dest_port         = "{{policy.dst_port}}"
    {% endif %}
    {% if policy.protocol %}
    protocol          = "{{policy.protocol}}"
    {% endif %}
    {% if policy.interface %}
    interface         = "{{policy.interface}}"
    {% endif %}
    {% if policy.connection.startswith("$") %}
    connection        = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
    {% else %}
    connection        = "{{policy.connection}}"
    {% endif %}
    {% if policy.mark %}
    mark              = "{{policy.mark}}"
    {% endif %}
    {% if policy.new_src_ip.startswith("$") %}
    snat_ips          = count.index == 0 ? aviatrix_spoke_gateway.gw.private_ip : aviatrix_spoke_gateway.gw.ha_private_ip
    {% else %}
    snat_ips          = "{{policy.new_src_ip}}"
    {% endif %}
    {% if policy.new_src_port %}
    snat_port         = "{{policy.new_src_port}}"
    {% endif %}
    {% if policy.exclude_rtb %}
    exclude_rtb       = "{{policy.exclude_rtb}}"
    {% endif %}
    apply_route_entry = {{policy.apply_route_entry}}
  }
  {% endfor %}
}
{% endif %}

resource "aviatrix_spoke_transit_attachment" "attachment" {
  spoke_gw_name   = aviatrix_spoke_gateway.gw.gw_name
{% if data.configure_gw_name %}
  transit_gw_name = var.transit_gw
{% else %}
  transit_gw_name = "aws-${local.region[var.region]}-transit-gw"
{% endif %}
  route_tables    = [for k, v in var.route_tables : aws_route_table.aviatrix_managed[k].id if var.route_tables[k].ctrl_managed == "True"]
}

resource "aws_route_table" "aviatrix_managed" {
  for_each = var.route_tables
  vpc_id   = var.vpc_id
  tags     = merge(each.value.tags, { Org_RT = each.key })
}

resource "aviatrix_transit_firenet_policy" "spoke" {
  count                        = var.inspection ? 1 : 0
  transit_firenet_gateway_name = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
  inspected_resource_name      = "SPOKE:${aviatrix_spoke_gateway.gw.gw_name}"
}

resource "aviatrix_segmentation_security_domain_association" "spoke" {
  count                = var.domain != "" ? 1 : 0
  transit_gateway_name = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
  security_domain_name = var.domain
  attachment_name      = aviatrix_spoke_gateway.gw.gw_name
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
{% if not data.configure_gw_name %}
  region = {
    us-west-1      = "usw1"
    us-west-2      = "usw2"
    us-east-1      = "use1"
    us-east-2      = "use2"
    ca-central-1   = "cac1"
    sa-east-1      = "sae1"
    eu-west-1      = "euw1"
    eu-west-2      = "euw2"
    eu-west-3      = "euw3"
    eu-central-1   = "euc1"
    eu-north-1     = "eun1"
    ap-south-1     = "aps1"
    ap-southeast-1 = "apse1"
    ap-southeast-2 = "apse2"
    ap-northeast-1 = "apne1"
    ap-northeast-2 = "apne2"
    ap-northeast-3 = "apne3"
    cn-north-1     = "cnn1"
    cn-northwest-1 = "cnnw1"
  }
{% endif %}
}
