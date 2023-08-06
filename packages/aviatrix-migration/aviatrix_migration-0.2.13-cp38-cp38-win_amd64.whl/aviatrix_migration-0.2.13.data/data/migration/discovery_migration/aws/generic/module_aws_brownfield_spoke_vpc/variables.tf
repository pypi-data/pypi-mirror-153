#generic
variable "region" {}

variable "account_name" {}

variable "role_arn" {}

variable "vpc_name" {}

variable "vpc_cidr" {
  type = list(string)
}

variable "vpc_id" {}

variable "avtx_cidr" {
  default     = ""
  description = "CIDR used by the Aviatrix gateways"
}

variable "tgw_vpc" {
  default     = false
  description = "Decides if VPC should be attached to a TGW"
}

variable "avtx_gw_size" {
  default = ""
}

variable "hpe" {
  default = false
}

variable "igw_id" {}

variable "route_tables" {}

variable "gw_zones" {
  type = list
}

variable "switch_traffic" {
  type    = bool
  default = false
}

variable "add_vpc_cidr" {
  type    = bool
  default = false
}

variable "spoke_gw_name" {
  default = ""
}

variable "transit_gw" {
  default = ""
}

variable "tags" {
  description = "Map of tags to assign to the gateway."
  type        = map
  default     = null
}

variable "domain" {
  description = "Provide security domain name to which spoke needs to be deployed. Transit gateway mus tbe attached and have segmentation enabled."
  type        = string
  default     = ""
}

variable "inspection" {
  description = "Set to true to enable east/west Firenet inspection. Only valid when transit_gw is East/West transit Firenet"
  type        = bool
  default     = false
}

variable "spoke_routes" {
  description = "A list of comma separated CIDRs to be customized for the spoke VPC routes. When configured, it will replace all learned routes in VPC routing tables, including RFC1918 and non-RFC1918 CIDRs. It applies to this spoke gateway only"
  type        = string
  default     = ""
}

variable "spoke_adv" {
  description = "A list of comma separated CIDRs to be advertised to on-prem as Included CIDR List. When configured, it will replace all advertised routes from this VPC."
  type        = string
  default     = ""
}

variable "encrypt" {
  description = "Enable EBS volume encryption for Gateway. Only supports AWS and AWSGOV provider. Valid values: true, false. Default value: false"
  type        = bool
  default     = false
}
