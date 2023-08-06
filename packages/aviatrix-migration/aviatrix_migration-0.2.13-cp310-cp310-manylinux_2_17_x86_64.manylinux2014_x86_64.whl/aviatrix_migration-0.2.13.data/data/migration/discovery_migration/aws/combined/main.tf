{% if data.tf_controller_access.mode == "SSM" %}
data "aws_ssm_parameter" "avx-password" {
  name     = "{{data.tf_controller_access.password_store}}"
  provider = aws.{{data.tf_controller_access.alias}}
}
{% endif %}

{% if data.onboard_account %}
resource "aviatrix_account" "aws_customer" {
  {% if data.account_name is defined %}
  account_name         = "{{data.account_name}}"
  {% else %}
  account_name         = "aws-${var.aws_account}"
  {% endif %}
  cloud_type           = 1
  aws_account_number   = var.aws_account
  aws_iam              = true
  audit_account        = false
  aws_role_app         = "arn:aws:iam::${var.aws_account}:role/${var.ctrl_role_app}"
  aws_role_ec2         = "arn:aws:iam::${var.aws_ctrl_account}:role/${var.ctrl_role_ec2}"
  aws_gateway_role_app = "arn:aws:iam::${var.aws_account}:role/${var.gateway_role_app}"
  aws_gateway_role_ec2 = "arn:aws:iam::${var.aws_account}:role/${var.gateway_role_ec2}"
}
{% endif %}

{% if data.enable_s3_backend %}
terraform {
  backend "s3" {}
}
{% endif %}