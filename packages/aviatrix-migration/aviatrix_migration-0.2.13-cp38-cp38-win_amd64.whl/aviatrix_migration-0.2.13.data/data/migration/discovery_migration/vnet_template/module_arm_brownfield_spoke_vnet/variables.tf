variable "region" {}
variable "account_name" {}
variable "resource_group_name" {}
variable "vnet_name" {}
variable "vnet_cidr" {
  description = "CIDR used by the applications"
}
variable "avtx_cidr" {
  default     = ""
  description = "CIDR used by the Aviatrix gateways"
}
variable "avtx_gw_size" {}
variable "hpe" {
  default = true
}
variable "use_azs" {
  type = bool
}
variable "route_tables" {}
variable "switch_traffic" {
  type    = bool
  default = false
}
variable "disable_bgp_propagation" {
  type        = bool
  default     = true
  description = "Used to configure aviatrix_managed_main RTs"
}
variable "spoke_gw_name" {
  default = ""
}
variable "transit_gw" {
  default = ""
}
variable "tags" {
  description = "Map of tags to assign to the gateway."
  type        = map(any)
  default     = null
}