{% if not data.configure_gw_name %} 
locals {
  region = {
    "East US"         = "use"
    "Central US"      = "usc"
    "West US"         = "usw"
    "West US 2"       = "usw2"
    "North Europe"    = "eun"
    "West Europe"     = "euw"
    "South East Asia" = "asse"
    "Japan East"      = "jae"
    "China East 2"    = "che2"
    "China North 2"   = "chn2"
  }
}
{% endif %}

resource "azurerm_subnet" "aviatrix_public" {
  count                = var.hpe ? 0 : 2
  name                 = count.index == 0 ? "aviatrix-spoke-gw" : "aviatrix-spoke-hagw"
  resource_group_name  = var.resource_group_name
  virtual_network_name = var.vnet_name
  address_prefixes     = [cidrsubnet(var.avtx_cidr, 1, count.index)]
}

resource "azurerm_route_table" "aviatrix_public" {
  count                         = var.hpe ? 0 : 1
  name                          = "${substr(var.vnet_name, 0, 7)}-rt-${lower(replace(var.region, " ", ""))}-aviatrix-01"
  location                      = var.region
  resource_group_name           = var.resource_group_name
  disable_bgp_route_propagation = true

  route {
    name           = "default"
    address_prefix = "0.0.0.0/0"
    next_hop_type  = "Internet"
  }

  tags = {
    "Name" = "aviatrix-${var.vnet_name}-gw"
  }
  lifecycle {
    ignore_changes = [tags]
  }
}

resource "azurerm_subnet_route_table_association" "aviatrix_public" {
  count          = var.hpe ? 0 : 2
  subnet_id      = azurerm_subnet.aviatrix_public[count.index].id
  route_table_id = azurerm_route_table.aviatrix_public[0].id
}

resource "aviatrix_spoke_gateway" "gw" {
  cloud_type   = 8
  account_name = var.account_name
{% if data.configure_gw_name %}
  gw_name                           = var.spoke_gw_name
{% else %}
  #This gw_name function adds abbreviated region and converts avtx_cidr to hex e.g. "aws-usw1-0a330200-gw"
  gw_name                           = "azu-${local.region[var.region]}-${join("", formatlist("%02x", split(".", split("/", var.avtx_cidr)[0])))}-gw"
{% endif %}
  vpc_id                            = join(":", [var.vnet_name, var.resource_group_name])
  vpc_reg                           = var.region
  insane_mode                       = var.hpe
  gw_size                           = var.avtx_gw_size
  ha_gw_size                        = var.avtx_gw_size
  subnet                            = cidrsubnet(var.avtx_cidr, 1, 0)
  ha_subnet                         = cidrsubnet(var.avtx_cidr, 1, 1)
  zone                              = var.use_azs ? "az-1" : null
  ha_zone                           = var.use_azs ? "az-2" : null
  included_advertised_spoke_routes  = var.switch_traffic ? join(",", var.vnet_cidr) : var.avtx_cidr
  manage_transit_gateway_attachment = false
{% if data.pre_v2_21_0 %}
  enable_active_mesh                = true
{% endif %}
  single_az_ha                      = true
  depends_on                        = [azurerm_subnet_route_table_association.aviatrix_public, azurerm_subnet.aviatrix_public]
  tags                              = var.tags
  lifecycle {
    ignore_changes = [tags]
  }
}

resource "aviatrix_spoke_transit_attachment" "attachment" {
  spoke_gw_name   = aviatrix_spoke_gateway.gw.gw_name
{% if data.configure_gw_name %}
  transit_gw_name = var.transit_gw
{% else %}
  transit_gw_name = "azu-${local.region[var.region]}-transit-gw"
{% endif %}
  route_tables    = local.all_rts
}

resource "azurerm_route_table" "aviatrix_managed_main" {
  count                         = 2
  name                          = "${var.vnet_name}-main-${count.index + 1}"
  location                      = var.region
  resource_group_name           = var.resource_group_name
  disable_bgp_route_propagation = var.disable_bgp_propagation
  lifecycle {
    ignore_changes = [tags]
  }
}

resource "azurerm_route_table" "aviatrix_managed" {
  for_each = var.route_tables

  name                          = each.key
  location                      = var.region
  resource_group_name           = var.resource_group_name
  disable_bgp_route_propagation = each.value.disable_bgp_propagation
  tags                          = merge(each.value.tags, { Org_RT = each.key })
  lifecycle {
    ignore_changes = [tags]
  }
}

resource "azurerm_route" "pre_migration" {
  for_each = {
    for route in local.routes : "${route.destination}.${route.key}" => route
    if route["target"] != "VNet peering" && route["target"] != "VirtualNetworkServiceEndpoint"
  }
  name                   = each.value.name
  resource_group_name    = var.resource_group_name
  route_table_name       = azurerm_route_table.aviatrix_managed[each.value.key].name
  address_prefix         = each.value.destination
  next_hop_type          = each.value.type
  next_hop_in_ip_address = each.value.type == "VirtualAppliance" ? each.value.target : null

  # You cannot specify VNet peering or VirtualNetworkServiceEndpoint as the next hop type in user-defined routes
}

locals {
  managed_mains = [
    "${azurerm_route_table.aviatrix_managed_main[0].name}:${azurerm_route_table.aviatrix_managed_main[0].resource_group_name}",
    "${azurerm_route_table.aviatrix_managed_main[1].name}:${azurerm_route_table.aviatrix_managed_main[1].resource_group_name}"
  ]
  managed_rts = [for rt_key, rt in var.route_tables : "${rt_key}:${var.resource_group_name}"]
  all_rts     = concat(local.managed_mains, local.managed_rts)
  routes = flatten([
    for rt_key, rt_val in var.route_tables : [
      for route in rt_val.routes : {
        key         = rt_key
        destination = route.destination
        target      = route.target
        type        = route.type
        name        = route.name
      }
    ]
  ])
}

locals {
  actions = {
    "Microsoft.Netapp/volumes"  = ["Microsoft.Network/networkinterfaces/*", "Microsoft.Network/virtualNetworks/subnets/join/action"]
    "Microsoft.Web/serverFarms" = ["Microsoft.Network/virtualNetworks/subnets/action"]
    "Microsoft.Sql/managedInstances" = [
      "Microsoft.Network/virtualNetworks/subnets/join/action",
      "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
      "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action"
    ]
  }
}
