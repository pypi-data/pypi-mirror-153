{% if data.tf_controller_access.mode == "SSM" %}
provider "aws" {
  region = "{{data.tf_controller_access.region}}"
  alias  = "{{data.tf_controller_access.alias}}"
  {% if data.tf_controller_access.ssm_role %}
  assume_role { role_arn = "arn:aws:iam::${var.aws_ctrl_account}:role/${var.ssm_role}" }
  {% endif %}
}

data "aws_ssm_parameter" "avx-password" {
  name     = "{{data.tf_controller_access.password_store}}"
  provider = aws.{{data.tf_controller_access.alias}}
}

data "aws_ssm_parameter" "avx-azure-client-secret" {
  name     = "{{data.subscriptionInfo.secret_data_src}}"
  provider = aws.us_west_2
}
{% endif %}

provider "aviatrix" {
{% if data.tf_controller_access.mode == "SSM" %}
  username      = "admin"
  password      = data.aws_ssm_parameter.avx-password.value
{% endif %}
  controller_ip = var.controller_ip
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
  subscription_id            = var.subscription_id
  client_id                  = "{{data.subscriptionInfo.app_id}}"
  {% if data.tf_controller_access.mode == "ENV" %}
  client_secret              = var.azure_client_secret
  {% else %}
  client_secret              = data.aws_ssm_parameter.avx-azure-client-secret.value
  {% endif %}
  tenant_id                  = "{{data.subscriptionInfo.dir_id}}"
  alias                      = "{{data.subscriptionInfo.alias}}"
}
