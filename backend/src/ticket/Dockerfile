FROM public.ecr.aws/lambda/python:3.12


COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

ARG LAMBDA_FUNC_PATH=./
ENV LAMBDA_FUNC_PATH=${LAMBDA_FUNC_PATH}
COPY .env ${LAMBDA_TASK_ROOT}
COPY ${LAMBDA_FUNC_PATH}/lambda_function.py ${LAMBDA_TASK_ROOT}



CMD ["lambda_function.lambda_handler"]