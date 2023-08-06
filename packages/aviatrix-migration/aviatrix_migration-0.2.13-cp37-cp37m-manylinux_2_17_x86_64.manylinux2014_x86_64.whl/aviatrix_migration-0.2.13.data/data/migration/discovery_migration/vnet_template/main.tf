{% if data.onboard_account %}
resource "aviatrix_account" "azure_{{data.account_name}}" {
  account_name        = var.account_name
  cloud_type          = 8
  arm_subscription_id = var.subscription_id
  arm_directory_id    = "{{data.subscriptionInfo.dir_id}}"
  arm_application_id  = "{{data.subscriptionInfo.app_id}}"
  {% if data.tf_controller_access.mode == "ENV" %}
  arm_application_key = var.azure_client_secret
  {% else %}
  arm_application_key = data.aws_ssm_parameter.avx-azure-client-secret.value
  {% endif %}
}
{% endif %}

{% if data.terraform.enable_s3_backend %}
terraform {
  backend "s3" {}
}
{% endif %}