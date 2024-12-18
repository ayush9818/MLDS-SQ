APP_NAME=iris-pipeline
ECR_URL=public.ecr.aws/g0i4r9p4

requirements.txt: poetry.lock
	poetry export -f requirements.txt --output requirements.txt --without-hashes

requirements: requirements.txt

build: Dockerfile
	docker build --platform=linux/amd64 -t ${APP_NAME}:latest .

run:
	docker run \
		-v ~/.aws:/root/.aws \
		-e AWS_PROFILE \
		iris-pipeline

clean:
	docker stop ${APP_NAME} && docker rm ${APP_NAME}

login:
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_URL}
tag:
	docker tag ${APP_NAME}:latest ${ECR_URL}/${APP_NAME}:latest
push:
	docker push ${ECR_URL}/${APP_NAME}:latest

publish: build tag push
