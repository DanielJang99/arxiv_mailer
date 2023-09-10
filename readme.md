# Arxiv Feed Mailer with AWS Lambda :page_facing_up: :incoming_envelope: :cloud:

-   Python program designed to fetch and deliver ArXiv research paper updates to your email inbox using AWS Lambda.
-   Stay updated on the latest research papers in your field of interest without manually checking the ArXiv website.
-   The program is designed to be configurable, allowing you to customize your ArXiv feed preferences to tailor your research interest.
-   This project was inspired from [this repo](https://github.com/basnijholt/arxiv-feed-mailer).

## Example

![alt text](https://github.com/DanielJang99/arxiv_mailer/blob/master/screenshots/results.png)

## Prerequisites

-   Python3.8 or above (AWS Lambda will [no longer support Python3.7](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html#runtime-support-policy))
-   Mac OS or Linux
-   Basic understanding of AWS S3, Lambda, IAM, and EventBridge

## Setup

1. Clone this repo
2. Create a virtual environment: `python3 -m venv /path/`. Activate it with `source /path/bin/activate`.
3. Enter project directory with `cd arxiv_mailer`. Install dependecies with `pip -r requirements.txt`
4. Customize: Specify sender mail address and receiver mail address (both can be the same), and add RSS news feed links in `personal_variables.py`. Each RSS news feed link should tailor your field of academic interest. Refer to the [documentation](https://info.arxiv.org/help/rss.html) to learn more about arXiv RSS.
5. Follow the [instructions here](https://medium.com/@nakulkurane/sending-gmail-on-aws-lambda-via-python-a7fa991a97f1) to download `client_secret.json` file from Google Developer Console. Save the file to the project directory.
6. You can now run the program locally with `python3 arxiv_feeder.py`. More instructions on running the program in AWS Lambda is on the next section.

## Usage with AWS Lambda

Running the program with AWS Lambda requires the following additional steps. Make sure you have completed the previous setup before proceeding.

1. Create a new directory named `python`. Copy `<your venv path>/lib` folder to `python` directory. Then compress `python` to a zip file. [Reference](https://medium.datadriveninvestor.com/how-to-set-up-layers-python-in-aws-lambda-functions-1355519c11ed)
2. Open [AWS console](https://aws.amazon.com/console/). Create a new **S3 bucket** and upload your `client_secret.json` AND compressed zip file of `python`.
3. Make a new **IAM policy** that defines Read & Write Access to the S3 bucket containing your `client_secret.json`. ![alt text](https://github.com/DanielJang99/arxiv_mailer/blob/master/screenshots/S3_access_policy.png)
4. Move to Lambda console and create a new layer with the `python` zip file in your S3 bucket.
   ![alt text](https://github.com/DanielJang99/arxiv_mailer/blob/master/screenshots/aws_layer.png)
5. Create a new AWS Lambda function with Python (3.8 or above) runtime. The make the following configurations:
    1. Upload `arxiv_mailer_code.zip` to the Lambda function's Code Source
    2. Add the layer (from step 4) to the Lambda function
    3. Add the S3 access policy (from step 3) to the Lambda function's Execution Role Permissions policies. [AWS Doc for reference](https://repost.aws/knowledge-center/lambda-execution-role-s3-bucket)
       ![alt text](https://github.com/DanielJang99/arxiv_mailer/blob/master/screenshots/lambda_exection_role.png)
    4. Add environment variables to the Lambda Function, where
        ```
        BUCKET_NAME = <Name of your S3 bucket>
        SECRET_OBJECT_KEY = client_secret.json
        SECRET_FILE_PATH = /tmp/client_secret.json
        ```
        ![alt text](https://github.com/DanielJang99/arxiv_mailer/blob/master/screenshots/env_var.png)
        [AWS Doc for reference](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html)
    5. Add a Trigger using EventBridge, where a Cron expression can be used to schedule Lambda function execution ![alt text](https://github.com/DanielJang99/arxiv_mailer/blob/master/screenshots/trigger.png)
6. All set!
