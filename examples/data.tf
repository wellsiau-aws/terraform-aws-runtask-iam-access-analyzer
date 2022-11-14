data "tfe_organization" "org" {
  name = var.tfc_org
}

data "tfe_workspace" "workspace" {
  name         = var.demo_workspace_name
  organization = data.tfe_organization.org.name
}