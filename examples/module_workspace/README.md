# Usage Example

First step is to deploy the module into dedicated Terraform Cloud workspace. The output `runtask_id` is used on other Terraform Cloud workspace to configure the runtask.

* Build and package the Lambda files using the makefile. Run this command from the root directory of this repository.
  ```bash
  make all
  ```

* Use the provided module example to deploy the solution.

  ```bash
  cd ../examples/module_workspace
  ```

* Change the org name in the file [`provider.tf`](provider.tf#L5) to your TFC org.

  ```
  terraform {

    cloud {
      # TODO: Change this to your Terraform Cloud org name.
      organization = "<enter your org name here>"
      workspaces {
        ...
      }
    }
    ...
  }   
  ```

* Initialize Terraform Cloud. When prompted, enter a new workspace name, i.e. `aws-ia2-infra`
  ```bash
  terraform init
  ```

* Configure the AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in Terraform Cloud, i.e. using variable sets. [Follow these instructions to learn more](https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-create-variable-set).

* In order to create and configure the run tasks, you also need to have Terraform Cloud token stored as Variable/Variable Sets/Environment Variables in the workspace. Add `TFE_HOSTNAME` and `TFE_TOKEN` environment variable to the same variable set or directly on the workspace.
![TFC Configure Variable Set](../diagram/TerraformCloud-VariableSets.png?raw=true "Configure Terraform Cloud Variable Set")

* Configure the new workspace (i.e `aws-ia2-infra`) in Terraform Cloud to use `local` execution mode. Skip this if you publish the module into Terraform registry.

* Run Terraform apply 
  ```bash
  terraform apply
  ```

* Use the output value `runtask_id` when deploying the demo workspace. See example of [demo workspace here](../demo_workspace/README.md)