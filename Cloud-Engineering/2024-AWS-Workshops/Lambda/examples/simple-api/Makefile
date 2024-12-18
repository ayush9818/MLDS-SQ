AWS_ACCOUNT_ID=381492011988

build:
	docker build -t simple-api -f dockerfiles/lambda.Dockerfile .

login:
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com

tag:
	docker tag simple-api:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/simple-api:latest

push:
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/simple-api:latest

publish: build tag push
