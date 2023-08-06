import os

ENVIRONMENT = os.environ['ENVIRONMENT']
DEVELOPER = os.environ.get('DEVELOPER')
LAMBDA_NAME = os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
