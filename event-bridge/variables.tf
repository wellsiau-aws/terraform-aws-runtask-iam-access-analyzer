variable "name_prefix" {
  description = "Name to be used on all the resources as identifier."
  type        = string
  default     = "ia2"
}

variable "event_bus_name" {
  description = "EventBridge event bus name"
  type        = string
  default     = "default"
}

variable "cloudwatch_log_group_retention" {
  description = "Lambda CloudWatch log group retention period"
  type        = string
  default     = "30"
  validation {
    condition     = contains(["1", "3", "5", "7", "14", "30", "60", "90", "120", "150", "180", "365", "400", "545", "731", "1827", "3653", "0"], var.cloudwatch_log_group_retention)
    error_message = "Valid values for var: cloudwatch_log_group_retention are (1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653, and 0)."
  }
}

variable "event_source" {
  description = "EventBridge source name"
  type        = string
  default     = "app.terraform.io"
}

variable "runtask_stages" {
  description = "List of all supported RunTask stages"
  type        = list(string)
  default     = ["pre_plan", "post_plan", "pre_apply"]
}

variable "tfc_org" {
  description = "Terraform Organization name"
  type        = string
}

variable "aws_region" {
  description = "The region from which this module will be executed."
  type        = string
  validation {
    condition     = can(regex("(us(-gov)?|ap|ca|cn|eu|sa)-(central|(north|south)?(east|west)?)-\\d", var.aws_region))
    error_message = "Variable var: region is not valid."
  }
}

variable "recovery_window" {
  description = "Numbers of day Number of days that AWS Secrets Manager waits before it can delete the secret"
  type        = number
  default     = 0
  validation {
    condition     = (var.recovery_window >= 0 && var.recovery_window <= 30)
    error_message = "Variable var: recovery_window must be between 0 and 30"
  }
}