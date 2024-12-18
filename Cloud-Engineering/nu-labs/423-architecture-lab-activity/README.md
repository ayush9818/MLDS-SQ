# Cloud Architecture

- Diagrams
  - [Diagrams.net / Draw.io](https://diagrams.net)
  - AWS Shapes Library
- Pricing Calculator
  - Pricing pages
  - [calculator.aws](https://calculator.aws)
- Security
  - Hashing
  - Encryption
  - Symmetric vs Asymmetric keys
  - PGP and alternatives

---

## Intro/Overview (5m)

### Labs for Cloud Engineering

We will have required lab sessions once per week for the duration of the quarter. In these labs, we will cover a variety of topics that may reinforce, expand, or just augment the topics covered during lecture.

I will do my best to make all lab content relevant to your assignments and final projects. We have a lot of material to cover, so please let me know if things are moving too quickly/slowly. Because these labs are meant to be very hands-on and practical, I will expect a good amount of presentation from all! Please keep your cameras on and make use of the chat and reaction features in Zoom (I will often ask for 👍 / 👎 in response to questions).

---

Labs will typically consist of the following format:

- Announcements etc. (~5m)
- Background information and scenario (~10m)
- Hands-on activity led by TA (~5m)
- Time to work independently on activity and  ask questions (~15m)
- Review of progress and example of completed activity (~10m)
- Wrap-up (~5m)

Content for each will be kept in a GitHub repository under the MSiA Organization. I will typically push the instructional content a day or two in advance along with the background/requirements for the activity. We will work through the activity together during the lab session and then I will push the completed activity a day or two after the lab for you to reference.

---

### Scenario for this lab

> Your company wants to build an automated machine learning pipeline to forecast sales for its line of athletic shoes. The pipeline should be fully event-driven and leverage several AWS services such as S3, SQS, Lambda, RDS, and ECS. The final product is a web application which allows internal business users to run various analytics against the live model. The company wants to leverage as many serverless/elastic services as is practical but is **not** eligible for any free-tier pricing. The company is not yet ready to commit to any reserved instances or savings plans. Services will be deployed in the US Ohio (us-east-2) region.

---

## Architecture and Services (10m)

Architecture Details:

1. Ingestion: Business processes will upload a spreadsheet to an S3 bucket using their own AWS credentials. The upload is captured by an S3 Event Notification which is directed to an AWS SQS Queue.

   > Details: 10-20 files per day, each around 200mb. (~500 GB already ingested).

2. Preprocessing: A Lambda function is configured to process messages in the Ingestion SQS Queue. The Lambda will fetch the new data from S3 and perform a series of cleaning and transformation steps before writing the results to a database in RDS.

   > Each file takes about 7 minutes to process when allocated 512mb of memory and 1024mb of ephemeral storage.

3. Data Storage: The data will be stored in a structured MySQL database running in AWS RDS. The data should be backed up nightly with snapshots kept for 3 months. Aside from model training, the database will also be used by several analytics teams running ad hoc SQL queries and by a separate sales web application making many lookup queries.

   > The data is used exclusively for reporting and analytics and thus does not have strict HA requirements. The database cluster should have at least 2 nodes each with at least 2vCPU. Total data stored will be about 150 GB.

4. Model Training: A nightly training job will run in AWS ECS (Fargate) which pulls in the structured data from RDS, trains a model, and uploads the trained model artifact to another S3 bucket.

   > The model training process takes about 90m to run when allocated 4 vCPU and 16mb of memory (64gb ephemeral storage).

5. Reporting: A web application will be deployed on AWS ECS (EC2) which fetches the trained model object (TMO) from S3 and uses it to perform inference on the users' requests.

   > The web server needs at least 2vCPU and 8 GiB of memory, 32 GB of storage, and should run 24/7. The application **cannot** run on ARM architecture.

6. Access: An Application Load Balancer will be used to expose the web service to users on the company intranet.

---

## Diagrams.net (15m)

We will be using Diagrams.net (formerly called Draw.io) for creating architecture diagrams in this course. The tool is open-source and free to use as a [web-app](https://app.diagrams.net). They include a collection of icons for AWS Services and Resources. You can also download a desktop app to run locally; follow the [instructions posted here](https://get.diagrams.net/).

1. Getting started with Diagrams.net
2. Starting an architecture diagram
3. Time to work on expanding the architecture diagram (independent)
4. Example of a completed architecture diagram (functional flow)
5. Example using resources instead of services
6. Example of a simplified network diagram

See starter template in [./architecture-starter.drawio](./architecture-starter.drawio)

---

## AWS Cost Calculator (10m)

1. Introduction to cost calculations
2. Common drivers of cost (compute vs storage vs networking etc.)
3. Where to find detailed pricing information (e.g. [lambda/pricing](https://aws.amazon.com/lambda/pricing/))
4. Using the [AWS Cost Calculator](https://calculator.aws) for comprehensive price estimates
5. Time to work on completing the cost estimation (independent)
6. Saving/sharing cost estimations (warning! refreshing the page will clear data)

---

## Security Fundamentals (10m)

Quick introduction to Hashing, Encryption, Keys, and Identity.

### Hashing

#### Introduction to hashing

Hashing is a method of transforming data into a fixed-length string of characters. The hash function takes input data and generates a hash code that is unique to that data. Emphasize that the output of a hash function cannot be reversed to recover the original data. ![Hashing Explained](https://www.thesslstore.com/blog/wp-content/uploads/2018/12/Hashing-Example.png)

#### Use case for hashing

Hashing is commonly used in password storage. When a user creates a password, the password is hashed and stored in a database. When the user tries to log in, the entered password is hashed and compared to the stored hash. If the hashes match, the user is authenticated. It is also very commonly used for identifying files based on their content. A distributor may publish the hash for a particular version of their software package. The user can then locally produce a hash of the software using the same hashing algorithm, and verify that it matches the published hash.

```shell
md5 README.md > checksum.md5
cat checksum.md5
md5 -c checksum.md5
```

---

### Encryption

#### Introduction to encryption

Encryption is the process of converting plain text into a coded message. Encryption is designed to protect the confidentiality of the data being transmitted or stored. The encryption process involves using an algorithm to scramble the data and a key to unscramble it.

---

##### Symmetric Encryption

One secret key can be used to encode and decode messages. This works great if all the parties have access to the secret key. But how do they get that secret key in a safe manner?

![Symmetric Encryption](https://www.thesslstore.com/blog/wp-content/uploads/2020/11/how-encryption-works-symmetric-encryption.png)

```shell
cat plaintext.txt
openssl enc -d -aes-256-cbc -pbkdf2 -in encrypted.enc -out decrypted.txt
cat encrypted.enc
openssl enc -d -aes-256-cbc -pbkdf2 -in encrypted.enc -out decrypted.txt
cat decrypted.txt
```

---

##### Asymmetric Encryption

Public/Private Key Pairs are used to safely encode, share, and decode sensitive data. The public key can _only_ encrypt messages and the private key can _only_ decrypt messages. Because of this, a potential receiver can share their public key safely to any sender who will then use the public key to encrypt data that only the recipient will be able to decrypt.

Similarly, asymmetric encryption can be used to verify identity. A sender will "sign" some piece of data that they wish to share; along with it they will publish the public key corresponding to their "signing key". Users can then "verify" that the data they have downloaded actually originated from the intended entity by checking it against the trusted public key.

![Symmetric Encryption](https://www.thesslstore.com/blog/wp-content/uploads/2020/12/how-asymmetric-encryption-works.png)

```shell
openssl genpkey -algorithm RSA -out private_key.pem
openssl rsa -pubout -in private_key.pem -out public_key.pem
cat public_key.pem

cat plaintext.txt
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in plaintext.txt -out encrypted.enc
cat encrypted.enc
openssl pkeyutl -decrypt -inkey private_key.pem -in encrypted.enc -out decrypted.txt
cat decrypted.txt
```

---

#### Use case for encryption

Encryption is commonly used in secure communication, such as online banking or email. When a user sends sensitive information, such as a credit card number, the data is encrypted before being transmitted. The recipient must have the key to decrypt the data and read the message.

---

### Key differences between hashing and encryption

Hashing is a **one-way process**, while encryption is a two-way process. With hashing, the output **cannot be reversed** to recover the original data. With encryption, the original data can be recovered using the key.

---

### Identity

We do not have time to cover identity in depth, but we will talk about it throughout the course. Identity is a very important topic in cloud computing and is comprised of authentication (proof of identity) and authorization (permissions of identity). All cloud providers have robust identity management systems both for managing access to the cloud resources (account permissions) as well as creating auth systems for applications in the cloud (managed identity solutions).

---

### Conclusion

Hashing and encryption are both very important tools for securing data. These topics become even more important as you move away from local development and begin deploying distributed applications to cloud environments

> Note: the diagrams above come from an online training course:
> [Tech Fundamentals | learn.cantrill.io](https://learn.cantrill.io/p/tech-fundamentals)
>
> If you are interested in going deeper with cloud training, you can also check out the AWS Cloud Practitioner Certification prep:
> [Cloud Practitioner - Digital and Classroom Training | AWS](https://aws.amazon.com/training/learn-about/cloud-practitioner/)
