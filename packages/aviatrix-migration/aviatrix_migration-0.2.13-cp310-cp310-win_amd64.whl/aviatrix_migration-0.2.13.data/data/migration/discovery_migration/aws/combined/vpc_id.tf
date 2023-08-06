variable "{{data.route_tables}}" {}

module "{{data.vpc_id}}" {
  source         = "../module_aws_brownfield_spoke_vpc"
  vpc_name       = "{{data.vpc_name}}"
  vpc_id         = "{{data.vpc_id}}"
  vpc_cidr       = {{data.vpc_cidr}}
  igw_id         = "{{data.igw_id}}"
{% if data.configure_gw_name %}
  spoke_gw_name  = "{{data.spoke_gw_name}}"
{% endif %}
{% if data.configure_gw_name %}
  transit_gw     = "{{data.transit_gw_name}}"
{% endif %}
  avtx_cidr      = "{{data.avtx_cidr}}"
  hpe            = {{data.hpe}}
  avtx_gw_size   = "{{data.avtx_gw_size}}"
  region         = "{{data.region}}"
  gw_zones       = {{data.gw_zones}}
{% if data.enable_spoke_egress %}
  enable_spoke_egress = true
{% endif %}
{% if data.onboard_account %}
  account_name   = aviatrix_account.aws_customer.account_name
{% else %}
  account_name   = "{{data.account_name}}"
{% endif %}
  route_tables   = var.{{data.route_tables}}
{% if data.domain is not none %}
  domain         = "{{data.domain}}"
{% endif %}
{% if data.inspection is not none %}
  inspection     = {{data.inspection}}
{% endif %}
{% if data.spoke_advertisement is not none %}
  spoke_adv      = "{{data.spoke_advertisement}}"
{% endif %}
{% if data.spoke_routes is not none %}
  spoke_routes   = "{{data.spoke_routes}}"
{% endif %}
{% if data.spoke_gw_tags is not none %}
  tags           = {{data.spoke_gw_tags}}
{% endif %}
{% if data.encrypt is not none %}
  encrypt        = {{data.encrypt}}
{% endif %}
  role_arn       = local.role_arn
  switch_traffic = false

  providers = { aws = {{data.providers}} }
}

{% if data.igw_id %}
resource "aws_internet_gateway" "igw-{{data.vpc_id}}" {
  vpc_id = "{{ data.vpc_id }}"
  tags = {{data.igw_tags}}
  provider = {{ data.providers }}
}
{% endif %}
