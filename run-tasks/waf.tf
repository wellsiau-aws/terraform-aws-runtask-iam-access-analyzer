module "runtask_cloudfront" {
  count  = local.waf_deployment
  source = "terraform-aws-modules/cloudfront/aws"

  comment             = "CloudFront for RunTask integration: ${var.name_prefix}"
  enabled             = true
  price_class         = "PriceClass_All"
  retain_on_delete    = false
  wait_for_deployment = false

  origin = {
    runtask_eventbridge = {
      domain_name = split("/", aws_lambda_function_url.runtask_eventbridge.function_url)[2]
      custom_origin_config = {
        http_port              = 80
        https_port             = 443
        origin_protocol_policy = "https-only"
        origin_ssl_protocols   = ["TLSv1.2"]
      }
    }
  }

  default_cache_behavior = {
    target_origin_id       = "runtask_eventbridge"
    viewer_protocol_policy = "https-only"

    # caching disabled: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-cache-policies.html#managed-cache-policy-caching-disabled
    cache_policy_id = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"

    origin_request_policy_id = aws_cloudfront_origin_request_policy.runtask_cloudfront[count.index].id
    use_forwarded_values     = false

    allowed_methods = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods  = ["GET", "HEAD", "OPTIONS"]

  }

  viewer_certificate = {
    cloudfront_default_certificate = true
  }
}

resource "aws_cloudfront_origin_request_policy" "runtask_cloudfront" {
  count   = local.waf_deployment
  name    = "${var.name_prefix}-runtask_cloudfront_origin_request_policy"
  comment = "Forward all request headers except host"
  cookies_config {
    cookie_behavior = "all"
  }
  headers_config {
    header_behavior = "whitelist"
    headers {
      items = [
        "x-tfc-task-signature",
        "content-type",
        "user-agent",
      "x-amzn-trace-id"]
    }
  }
  query_strings_config {
    query_string_behavior = "all"
  }
}