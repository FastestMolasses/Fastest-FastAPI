build-container: ## Build container
	docker buildx build --platform=linux/amd64 -t $(CONTAINER_NAME) .

run-container: ## Run container
	docker run --name=$(CONTAINER_NAME) -d -p 5500:8000 $(CONTAINER_NAME)

upload-container: ## Upload container to ECR
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(CONTAINER_REPO_NAME)
	docker tag $(CONTAINER_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(CONTAINER_REPO_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(CONTAINER_REPO_NAME):latest

cutover-ecs: ## Cutover to new ECS task definition
	aws ecs update-service --cluster $(ECS_CLUSTER_NAME) --service $(ECS_SERVICE_NAME) --force-new-deployment

deploy-cloudwatch-lambda: ## Deploy the cloudwatch lambda ## TODO: UPDATE FOR SAMPLE LAMBDA
	zip -j sns_cloudwatch_webhook.zip app/lmbd/sns_cloudwatch_webhook/main.py
	aws lambda update-function-code --function-name sns-cloudwatch-webhook --zip-file fileb://sns_cloudwatch_webhook.zip
	rm sns_cloudwatch_webhook.zip

help: ## Display help
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF}' $(MAKEFILE_LIST) | sort
