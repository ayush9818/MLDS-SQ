# Deploying a Streamlit App in AWS

This workshop is all about DOING! We will start with a basic Streamlit application which loads some artifacts from the filesystem and allows users to make inferences in a graphical user interface (GUI). We will make some improvements to the application, and then tool it for an AWS deployment.

## Getting Started

The included applications are both built with poetry but also include a requirements.txt file for setting up any virtual environment as well as a Dockerfile if you prefer to run as a container. Both the `pipeline` and `iris_app` sub-projects include their own README files explaining how to install/run the applications.

You should run the applications yourself before moving on with the activity and deployment components. The pipeline should be run first to produce the artifacts. If you are running in Docker, you will want to be sure and mount a local volume so that the produced artifacts are written to your local filesystem. Additionally, you will need to copy these files over to the `iris_app` project, or directly mount the `iris_app/artifacts` directory to your pipeline Docker image. Alternatively, if you are running without Docker, you can configure the pipeline to write artifacts directly to the `iris_app/artifacts` directory. Command references can be found in each project's README file.

## Pipeline

The included pipeline application should be familiar at this point: train a simple classifier on the iris dataset and save the model + dataset to an `artifacts/` folder. However, I have made some changes to the pipeline so that it will load configuration from a yaml file kept locally or pulled from S3. Then, at the end of the pipeline, the artifacts will be uploaded to S3 in a location determined by environment variables as well as the config file.

In summary, the following files will be uploaded to S3:

- dataset: `s3://{BUCKET_NAME}/[ARTIFACTS_PREFIX]/{version}/iris.joblib`
- trained model object (TMO): `s3://{BUCKET_NAME}/[ARTIFACTS_PREFIX]/{version}/iris_classifier.joblib`

Where the key is determined by:

- `BUCKET_NAME`: environment variable of the same name; defaults to `smf2659-iris`
- `ARTIFACTS_PREFIX`: environment variable of the same name; defaults to `artifacts/`
- `version`: config file `.run_config.version` key; defaults to `default`

## Streamlit

The Streamlit application provides a simple GUI for performing inference on a trained classifier model and presenting the predicted class to the user. The application relies on the data and TMO (`iris.joblib` and `iris_classifier.joblib`) being in the `artifacts/` folder relative to where the application is run.

The user can adjust their input to inference by dragging sliders around. Every time a slider changes, the application will re-compute its entire state so that the new prediction can be made.

The application includes a couple of functions to load the model and the dataset from disk into memory and also includes some constants used to identify where the artifacts are kept. Additionally, several environment variables are present that include information about the files uploaded to S3 by the pipeline in the previous step.

## Activity

It is your job to improve this application and deploy it to the cloud. We will only deal with the Streamlit application today, but the pipeline could easily be deployed in a similar manner.

### Problems

- The application reloads data and the TMO every time the input changes. This is unnecessary and greatly slows down the application.
- The application relies on a local artifacts folder which may not be available when the application is deployed.
- Bonus: We cannot select a model once the app has started up.

### Caching

Streamlit has really easy caching mechanisms built in and provided as python decorators.

See the [Streamlit docs for Caching](https://docs.streamlit.io/library/advanced-features/caching) to learn more.

Since our dataset is static, it can be cached using the `streamlit.cache_data` decorator:

```python
@st.cache_data
def load_data():
    print("Loading artifacts from: ", artifacts.absolute())
    ...
    return class_names, X
```

Our TMO however is not as easily serializable and needs to be consumed throughout the application; for it, we will use the `streamlit.cache_resource` decorator:

```python
@st.cache_resource
def load_model():
    # Download files from S3
    clf = joblib.load(iris_model_file)
    return clf
```

### S3 Interface

Next, we will set up our application to fetch files from a configurable location in S3. We can make use of the constants already available and simple download the files from S3 to the artifacts location our application is already reading from.

It may be helpful to store the S3 key for each object in a variable in case we wan to use it or log it later.

```python
# Configure S3 location for each artifact
iris_s3_key = str(ARTIFACTS_PREFIX / MODEL_VERSION / iris_file.name)
iris_model_s3_key = str(ARTIFACTS_PREFIX / MODEL_VERSION / iris_model_file.name)
```

Now let's modify our load_data function to first download the file from S3. Remember, we will want to make use of Streamlit caching so that this call to AWS only happens once when the app first starts up.

```python
def load_data():
    print("Loading artifacts from: ", artifacts.absolute())
    # Download files from S3
    aws.download_s3(BUCKET_NAME, iris_s3_key, iris_file)
    ...
    return class_names, X
```

Make a similar change to the `load_model()` function.

### Model Selection

To load locally available models, we could do something like the following

```python
def load_model_versions(path):
    return [p.name for p in path.glob("*") if p.is_dir()]
```

And then allow the user to select the model with a streamlit `selectbox` like so:

```python
# Find available model versions in artifacts dir
available_models = load_model_versions(artifacts)

# Create a dropdown to select the model
model_version = st.selectbox("Select Model", list(available_models))
```

However, we will want to list available models from S3 and also add caching to this function as well.

## Deployment

We will now deploy this application to AWS ECS where it can be elastically scaled, run 24/7, and exposed on the internet for others to use.

We will be following the same steps as presented in the [AWS ECS Workshop](https://github.com/MSIA/2023-AWS-Workshops/blob/main/ECS/ecs-console.md).

The application is already set up to be built as a Docker image. The steps that remain are summarized below:

1. Create an ECR Repository for the image
   1. Build, tag, and push your image as described in the ECR Push Commands
2. Create an ECS Cluster if you do not still have one
3. Create an ECS Task Definition for the `iris-app`
   1. Remember to configure the resource requests to use small values for cpu/memory
   2. Set the environment variables required for the application (at least `BUCKET_NAME`)
4. Create an ECS Service based on this Task Definition
   1. Create a Task Role with permissions to read files from the configured S3 Bucket
   2. Configure the service with an Application Load Balancer (ALB)
   3. You may use an existing security group and just select the "default" named security group; or, you can create a new one and allow Ingress on port 80 from the NU VPN CIDR (`165.124.160.0/21`)
5. Once the application is deployed, you can view the Service dashboard and from the **Networking** tab, you should be able to find the URL at which the ALB is deployed
   1. Note: If you create a new SG in step 4.3, you may also have to amend the security group to allow internal communication; e.g. on the security group, add a rule that allows All Traffic for source of the same security group. This allows connections from the ALB to the container in ECS.
   2. Note: If you use the existing "default" security group, it will already have internal traffic allowed, but you may have to add an Ingress rule for port 80 from NU VPN (if you did not do this during the ECS Workshop).
