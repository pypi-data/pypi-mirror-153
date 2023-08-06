controller_ip = "{{data.controller_ip}}"
account_name = "{{data.account_name}}"
subscription_id = "{{data.subscription_id}}"
{% if data.tf_controller_access.account_id %}
aws_ctrl_account = "{{data.tf_controller_access.account_id}}"
{% endif %}
{% if data.tf_controller_access.ssm_role %}
ssm_role         = "{{data.tf_controller_access.ssm_role}}"
{% endif %}