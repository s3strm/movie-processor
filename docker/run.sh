#!/usr/bin/env bash
dir=$(dirname $0)

_usage() {
  echo "$0 <s3_key>" >&2
}

[[ $# -ne 1 ]] && _usage && exit 1

KEY=$1
STACK_NAME=$(${dir}/../bin/get_setting MOVIE_MP4META_STACK_NAME)
DOCKER_STACK_NAME=$(${dir}/../bin/get_setting DOCKER_STACK_NAME)
CONTAINER_NAME=$(${dir}/../bin/get_setting MOVIE_MP4META_ECR_REPO)

TASK_DEFINITION_ARN=$(
  aws cloudformation describe-stacks \
    --stack-name "${STACK_NAME}" \
    --query 'Stacks[].Outputs[?OutputKey==`TaskDefinition`].OutputValue[]' \
    --output "text"
)

CLUSTER_NAME=$(
  aws cloudformation describe-stacks \
    --stack-name "${DOCKER_STACK_NAME}" \
    --query 'Stacks[].Outputs[?OutputKey==`Cluster`].OutputValue[]' \
    --output "text"
)

OVERRIDES=$(cat <<EOF
{ "containerOverrides": [
    {
      "name": "${CONTAINER_NAME}",
      "environment": [
        { "name": "KEY", "value": "${KEY}" }
      ]
    }
  ]
}
EOF
)

aws ecs run-task \
  --cluster ${CLUSTER_NAME} \
  --task-definition ${TASK_DEFINITION_ARN} \
  --overrides "${OVERRIDES}"

