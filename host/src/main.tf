#############################################################################
# VARIABLES
#############################################################################

variable "region" {
  type = string
  default = "us-east-2"
}

#############################################################################
# PROVIDERS
#############################################################################

provider "aws" {
  region = var.region
}

#############################################################################
# DATA SOURCES
#############################################################################

data "archive_file" "publish_zip" {
  depends_on  = [null_resource.publish_files]
  type        = "zip"
  source_dir  = "${path.module}/../../src/publish/publish"
  output_path = "${path.module}/../../src/publish/publish.zip"
}

data "aws_iam_role" "existing_lambda_role" {
  name = "production.lambda-execute.role"
}

#############################################################################
# RESOURCES
#############################################################################  

resource "null_resource" "publish_files" {
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = <<EOT
        mkdir -p ../../src/publish/publish
        cp -r ../../src/package/ ../../src/publish/publish/
        cp ../../src/*.py ../../src/publish/publish/
    EOT
  }
}

module "lambda_function" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "WeatherForecastAPI-Python"
  description   = "AWS Lambda weather forecast API function for training purposes using Python."
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.13"
  create_role   = false
  #lambda_role  = aws_iam_role.lambda_role.arn
  lambda_role   = data.aws_iam_role.existing_lambda_role.arn
  tracing_mode  = "Active"
  publish       = true
  architectures = ["arm64"]

  environment_variables = {
  }

  tags = {
    Name        = "WeatherForecastAPI-Python.Function"
    Environment = "Sandbox"
    Repository  = "https://github.com/CurtisLawhorn/WeatherForecastAPI-Python.Function.git"
  }

  local_existing_package = "${path.module}/../../src/publish/publish.zip"
  source_path = "../../src"

  #attach_policy_statements = true
  #policy_statements = {
  #  cloud_watch = {
  #    effect    = "Allow",
  #    actions   = ["cloudwatch:PutMetricData"],
  #    resources = ["*"]
  #  }
  #}
  
}

#resource "aws_iam_role" "lambda_role" {
#  name = "production.lambda-execute2.role"
#  assume_role_policy = jsonencode({
#    Version = "2012-10-17",
#    Statement = [{
#      Action = "sts:AssumeRole",
#      Effect = "Allow",
#      Principal = {
#        Service = "lambda.amazonaws.com",
#      },
#    }],
#  })
#}

#resource "aws_iam_policy" "lambda_policy" {
#  name   = "lambda_policy"
#  policy = jsonencode({
#    Version = "2012-10-17",
#    Statement = [{
#      Action = [
#        "logs:CreateLogGroup",
#        "logs:CreateLogStream",
#        "logs:PutLogEvents",
#      ],
#      Effect   = "Allow",
#      Resource = "*",
#      #Resource = "arn:aws:logs:*:*:*",
#    }],
#  })
#}

#resource "aws_iam_role_policy_attachment" "lambda_logs" {
#  #role      = aws_iam_role.lambda_role.name
#  role       = data.aws_iam_role.existing_lambda_role.name
#  policy_arn = aws_iam_policy.lambda_policy.arn
#}

#############################################################################
# OUTPUTS
#############################################################################
