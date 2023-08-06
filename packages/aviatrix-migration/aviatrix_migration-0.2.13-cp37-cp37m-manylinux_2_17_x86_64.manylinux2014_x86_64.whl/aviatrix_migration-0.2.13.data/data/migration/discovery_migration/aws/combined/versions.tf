terraform {
  {% if data.tf_cloud %}
  cloud {
    organization = "{{data.tf_cloud.organization}}"
    workspaces {
      {% if data.tf_cloud.workspace_name %}
      name = "{{data.tf_cloud.workspace_name}}"
      {% else %}
      tags = {{data.tf_cloud.tags}}
      {% endif %}
    }
  }  
  {% endif %}
  required_providers {
    aviatrix = {
      source  = "aviatrixsystems/aviatrix"
      version = {{data.aviatrix_provider}}
    }
    aws = {
      source  = "hashicorp/aws"
      version = {{data.aws_provider}}
    }
  }
  required_version = {{data.terraform_version}}
}
