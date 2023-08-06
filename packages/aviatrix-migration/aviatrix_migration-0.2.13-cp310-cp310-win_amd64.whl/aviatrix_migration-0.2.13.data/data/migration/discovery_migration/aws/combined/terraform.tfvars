controller_ip    = "{{data.controller_ip}}"
aws_account      = "{{data.account_id}}"
aws_account_role = "{{data.aws_account_role}}"
aws_ctrl_account = "{{data.controller_account}}"
ctrl_role_app    = "{{data.ctrl_role_app}}"
ctrl_role_ec2    = "{{data.ctrl_role_ec2}}"
gateway_role_app = "{{data.gateway_role_app}}"
gateway_role_ec2 = "{{data.gateway_role_ec2}}"
{% if data.tf_controller_access.ssm_role %}
ssm_role         = "{{data.tf_controller_access.ssm_role}}"
{% endif %}

