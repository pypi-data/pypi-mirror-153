variable controller_ip {}
variable account_name {}
{% if data.tf_controller_access.account_id %}
variable aws_ctrl_account {}
{% endif %}
{% if data.tf_controller_access.ssm_role %}
variable "ssm_role" {}
{% endif %}
{% if data.tf_controller_access.mode == "ENV" %}
variable "azure_client_secret" {}
{% endif %}
variable subscription_id {}