<!-- BEGIN_TF_DOCS -->
# terraform-runtask-iam-access-analyzer

This module can be used to integrate Terraform Cloud Run Tasks with AWS IAM Access Analyzer for policy validation.

## Usage

You must complete the [general prerequisites](../README.md#Prerequisites) as referenced in the solution README before deploying this module.

* Build and package the Lambda files

  ```
  make all
  ```

* Change the TFC org name in the file [`provider.tf`](provider.tf#L5) to your TFC org.

  ```
  terraform {

    cloud {
      # TODO: Change this to your Terraform Cloud org name.
      organization = "<enter your org name here>"
      workspaces {
        tags = ["app:aws-event-bridge"]
      }
    }
    ...
  }   
  ```

* Populate the required variables, change the placeholder value below.
  ```bash
  echo 'tfc_org="<enter your org name here>"' >> tf.auto.tfvars
  echo 'aws_region="<enter the AWS region here>"' >> tf.auto.tfvars
  ```

* Initialize Terraform Cloud. When prompted, enter the name of the new workspace, i.e. `aws-iam_access-analyzer-run-task`
  ```bash
  terraform init
  ```

* Configure the AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in Terraform Cloud, i.e. using environment variable.

* In order to create and configure the run tasks, you also need to have Terraform Cloud keys stored as Variable/Variable Sets in the workspace. Add `TFE_HOSTNAME` and `TFE_TOKEN` environment variable to the same variable set or directly on the workspace.
![TFC Configure Variable Set](../diagram/TerraformCloud-VariableSets.png?raw=true "Configure Terraform Cloud Variable Set")

* Run Terraform apply
  ```bash
  terraform apply
  ```

* Navigate to your Terraform Cloud organization, go to Organization Settings > Integrations > Run tasks to find the newly created Run Task `aws-ia2-runtask`.

You can use this run task in any workspace where you have standard IAM resource policy document. Use the example steps below to continue with the demonstration.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 4.38.0 |
| <a name="requirement_tfe"></a> [tfe](#requirement\_tfe) | ~>0.38.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.38.0 |
| <a name="provider_random"></a> [random](#provider\_random) | n/a |
| <a name="provider_tfe"></a> [tfe](#provider\_tfe) | ~>0.38.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_runtask_cloudfront"></a> [runtask\_cloudfront](#module\_runtask\_cloudfront) | terraform-aws-modules/cloudfront/aws | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_cloudfront_origin_request_policy.runtask_cloudfront](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudfront_origin_request_policy) | resource |
| [aws_cloudwatch_event_rule.runtask_rule](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.runtask_target](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.runtask_callback](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.runtask_fulfillment](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.runtask_fulfillment_output](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.runtask_request](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.runtask_states](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/cloudwatch_log_group) | resource |
| [aws_iam_role.runtask_callback](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role) | resource |
| [aws_iam_role.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role) | resource |
| [aws_iam_role.runtask_fulfillment](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role) | resource |
| [aws_iam_role.runtask_request](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role) | resource |
| [aws_iam_role.runtask_rule](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role) | resource |
| [aws_iam_role.runtask_states](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role) | resource |
| [aws_iam_role_policy.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.runtask_fulfillment](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.runtask_rule](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.runtask_states](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy_attachment.runtask_callback](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.runtask_fulfillment](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.runtask_request](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.runtask_callback](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/lambda_function) | resource |
| [aws_lambda_function.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/lambda_function) | resource |
| [aws_lambda_function.runtask_fulfillment](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/lambda_function) | resource |
| [aws_lambda_function.runtask_request](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/lambda_function) | resource |
| [aws_lambda_function_url.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/lambda_function_url) | resource |
| [aws_secretsmanager_secret.runtask_hmac](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/secretsmanager_secret) | resource |
| [aws_secretsmanager_secret_version.runtask_hmac](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/secretsmanager_secret_version) | resource |
| [aws_sfn_state_machine.runtask_states](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/resources/sfn_state_machine) | resource |
| [random_uuid.runtask_hmac](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/uuid) | resource |
| [tfe_organization_run_task.aws_iam_analyzer](https://registry.terraform.io/providers/hashicorp/tfe/latest/docs/resources/organization_run_task) | resource |
| [archive_file.runtask_callback](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.runtask_eventbridge](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.runtask_fulfillment](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.runtask_request](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_caller_identity.current_account](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy.AWSLambdaBasicExecutionRole](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/data-sources/iam_policy) | data source |
| [aws_partition.current_partition](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/data-sources/partition) | data source |
| [aws_region.current_region](https://registry.terraform.io/providers/hashicorp/aws/4.38.0/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The region from which this module will be executed. | `string` | n/a | yes |
| <a name="input_tfc_org"></a> [tfc\_org](#input\_tfc\_org) | Terraform Organization name | `string` | n/a | yes |
| <a name="input_cloudwatch_log_group_name"></a> [cloudwatch\_log\_group\_name](#input\_cloudwatch\_log\_group\_name) | RunTask CloudWatch log group name | `string` | `"/hashicorp/terraform/runtask/iam-access-analyzer/"` | no |
| <a name="input_cloudwatch_log_group_retention"></a> [cloudwatch\_log\_group\_retention](#input\_cloudwatch\_log\_group\_retention) | Lambda CloudWatch log group retention period | `string` | `"30"` | no |
| <a name="input_deploy_waf"></a> [deploy\_waf](#input\_deploy\_waf) | Set to true to deploy CloudFront and WAF in front of the Lambda function URL | `string` | `false` | no |
| <a name="input_event_bus_name"></a> [event\_bus\_name](#input\_event\_bus\_name) | EventBridge event bus name | `string` | `"default"` | no |
| <a name="input_event_source"></a> [event\_source](#input\_event\_source) | EventBridge source name | `string` | `"app.terraform.io"` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | Name to be used on all the resources as identifier. | `string` | `"aws-ia2"` | no |
| <a name="input_recovery_window"></a> [recovery\_window](#input\_recovery\_window) | Numbers of day Number of days that AWS Secrets Manager waits before it can delete the secret | `number` | `0` | no |
| <a name="input_runtask_stages"></a> [runtask\_stages](#input\_runtask\_stages) | List of all supported RunTask stages | `list(string)` | <pre>[<br>  "pre_plan",<br>  "post_plan",<br>  "pre_apply"<br>]</pre> | no |
| <a name="input_supported_policy_document"></a> [supported\_policy\_document](#input\_supported\_policy\_document) | (Optional) allow list of the supported IAM policy document | `string` | `""` | no |
| <a name="input_workspace_prefix"></a> [workspace\_prefix](#input\_workspace\_prefix) | TFC workspace name prefix that allowed to run this runtask | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_runtask_hmac"></a> [runtask\_hmac](#output\_runtask\_hmac) | n/a |
| <a name="output_runtask_id"></a> [runtask\_id](#output\_runtask\_id) | n/a |
| <a name="output_runtask_url"></a> [runtask\_url](#output\_runtask\_url) | n/a |
<!-- END_TF_DOCS -->