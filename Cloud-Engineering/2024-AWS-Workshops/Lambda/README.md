# AWS Lambda

AWS Lambda is a serverless computing service offered by AWS that allows developers to run their code in response to events, such as changes to data in an Amazon S3 bucket or a new record in an Amazon DynamoDB table, without the need to provision or manage servers.

## Benefits of AWS Lambda

Here are some of the benefits of using AWS Lambda:

- **No server management**: With AWS Lambda, you don't need to worry about server management, scaling, or availability. AWS Lambda automatically scales your applications based on the incoming traffic and provisions the necessary resources to handle it.
- **Pay-per-use pricing**: AWS Lambda has a pay-per-use pricing model, which means you only pay for the time your code is running. There is no need to pay for idle resources or capacity planning. Oftentimes this means super cheap compute for simple use cases.
- **Easy integration with other AWS services**: AWS Lambda can easily integrate with other AWS services, such as Amazon S3, Amazon DynamoDB, Amazon API Gateway, and Amazon Kinesis, to name a few.
- **Support for multiple programming languages**: AWS Lambda supports several programming languages, including Node.js, Python, Java, Go, and .NET, allowing you to choose the language that best fits your needs.
- **Fast deployment**: AWS Lambda allows you to deploy your code quickly and easily, allowing you to focus on your application's functionality rather than infrastructure management.

## Deploying Lambda

Here are the basic steps for configuring AWS Lambda:

1. Create a new Lambda function: To create a new Lambda function, go to the AWS Management Console, select the Lambda service, and click on the "Create function" button.

2. Choose the function's trigger: After creating the function, you need to choose the trigger that will invoke the function. AWS Lambda supports several triggers, including API Gateway, S3, DynamoDB, and Kinesis, among others.

3. Write the function code: Once you've chosen the trigger, you can write your function code. AWS Lambda supports several programming languages, including Node.js, Python, Java, Go, and .NET, allowing you to choose the language that best fits your needs.

4. Configure the function settings: After writing the function code, you can configure the function settings, such as the function timeout, memory allocation, and environment variables.

5. Test the function: Before deploying the function, you should test it to ensure it works as expected. AWS Lambda provides several testing options, including a testing console and command-line tools.

6. Deploy the function: After testing the function, you can deploy it to AWS Lambda, where it will automatically scale based on incoming traffic.

## Important Configuration

The most important configuration settings for a Lambda function depend on the specific use case and the needs of the application. However, here are some common settings that you should consider when configuring a Lambda function:

1. **Function timeout**: The maximum amount of time your Lambda function is allowed to run before it is terminated. This is an important setting to consider, as it affects the overall performance of your application and can cause unexpected behavior if set too low. The max timeout at the time of writing is 15 minutes.

2. **Memory allocation**: The amount of memory allocated to your Lambda function, which affects its overall performance and resource utilization. Higher memory allocation can result in faster function execution times, but can also increase the cost of running your function.

3. **Environment variables**: Environment variables can be used to store sensitive information, such as API keys or database credentials, as well as application-specific configuration settings. Using environment variables can help you keep your codebase clean and avoid hardcoding sensitive information in your code.

4. **Concurrency**: The number of requests that can be processed by your Lambda function at the same time. By default, AWS sets the concurrency limit to 1000 per region (shared across all function), but this can be increased by contacting AWS support.

5. **VPC configuration**: If your Lambda function needs to access resources in a VPC, you will need to configure your function to run in a VPC and assign it to a specific subnet and security group.

6. **Triggers**: The event sources that will trigger your Lambda function to run, such as an S3 bucket or a Kinesis stream. You can configure multiple triggers for a single Lambda function.

7. **Logging**: AWS Lambda provides built-in logging functionality, allowing you to view logs of your function's execution. You can also configure custom logging destinations, such as Amazon CloudWatch Logs, to store your function's logs.

It's important to note that these are just a few of the most important configuration settings for a Lambda function, and that the specific configuration requirements will depend on your application's needs and use case.

## Pricing

AWS Lambda pricing is based on the number of requests processed and the time your code takes to run. AWS Lambda provides a free tier that allows you to run up to 1 million requests per month for free. After that, pricing starts at $0.20 per 1 million requests and $0.00001667 for every GB-second of compute time.

## Common Use Cases

Here are some common use cases for AWS Lambda:

1. **Event-driven processing**: Lambda functions can be triggered by a variety of AWS event sources, such as S3 buckets, Kinesis streams, and DynamoDB tables. This allows you to perform processing tasks in response to events in real-time, without the need for continuously running servers.
2. **Serverless APIs**: Lambda functions can be used to build serverless APIs using AWS API Gateway. This allows you to create API endpoints that can handle HTTP requests and execute business logic without the need for a dedicated server.
3. **Batch processing**: Lambda functions can be used to process large batches of data, such as processing log files or generating reports. By using AWS Lambda, you can take advantage of the automatic scaling and pay-per-use pricing model to process large amounts of data efficiently and cost-effectively.
4. **Data processing and transformation**: Lambda functions can be used to process and transform data in real-time, such as filtering or aggregating data from streaming sources like Kinesis or Apache Kafka.
5. **Mobile and IoT backends**: Lambda functions can be used to build backends for mobile and IoT applications. This allows you to perform serverless compute tasks in response to events generated by mobile or IoT devices.
6. **Chatbots and voice assistants**: Lambda functions can be used to build chatbots and voice assistants using services like Amazon Lex or Amazon Alexa. This allows you to build natural language processing capabilities into your application without the need for dedicated servers.

These are just a few examples of the many use cases for AWS Lambda. The versatility and flexibility of Lambda make it a powerful tool for building scalable and cost-effective serverless applications.

## Activity

We are going to set up a few lambda functions to demonstrate common use cases. See [Activity.md](./Activity.md) for a step-by-step walkthrough.
