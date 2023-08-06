variable "$route_tables" {}

module "${vpc_id}" {
  source         = "../module_aws_brownfield_spoke_vpc"
  vpc_name       = "$vpc_name"
  vpc_id         = "$vpc_id"
  vpc_cidr       = $vpc_cidr
  add_vpc_cidr   = $add_vpc_cidr
  igw_id         = "$igw_id"
  spoke_gw_name  = "$spoke_gw_name"
  transit_gw     = "$transit_gw_name"
  avtx_cidr      = "$avtx_cidr"
  spoke_adv      = "$spoke_advertisement"
  spoke_routes   = "$spoke_routes"
  hpe            = $hpe
  avtx_gw_size   = "$avtx_gw_size"
  region         = "$region"
  gw_zones       = $gw_zones
  account_name   = "$account_name"
  route_tables   = var.$route_tables
  role_arn       = local.role_arn
  switch_traffic = false
  domain         = "$domain"
  inspection     = $inspection
  tags           = $spoke_gw_tags
  providers = { aws = $providers }
}
