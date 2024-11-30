# Python Web API Serverless Application

This project shows how to run a Python API project as an AWS Lambda.

## Here are some steps to follow from to get started with the Terraform:

The role (production.lambda-execute.role) and policies (below) for Lambda execution and trace logging need to be setup ahead of time.

Lambda execution (AWSLambdaBasicExecutionRole)
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

Trace logging (AWSLambdaTracerAccessExecutionPolicy)
```
{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": [
            "xray:PutTraceSegments",
            "xray:PutTelemetryRecords"
        ],
        "Resource": [
            "*"
        ]
    }
}
```  

To deploy your function to AWS Lambda, run the below commands from the /hosting/src folder. 

```
    terraform init
    terraform validate
    terraform plan
    terraform apply
    terraform destroy
```

## Here are some steps to follow to get started from the command line:

Once you have edited your template and code you can deploy your application using the [Amazon.Lambda.Tools Global Tool](https://github.com/aws/aws-extensions-for-dotnet-cli#aws-lambda-amazonlambdatools) from the command line.

Install Amazon.Lambda.Tools Global Tools if not already installed.
```
    dotnet tool install -g Amazon.Lambda.Tools
```

If already installed check if new version is available.
```
    dotnet tool update -g Amazon.Lambda.Tools
```

