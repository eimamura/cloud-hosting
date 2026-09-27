"""AWS Lambda entry (API Gateway, Function URL, or ALB). Handler: lambda_handler.handler."""

from mangum import Mangum

from app.main import app

handler = Mangum(app, lifespan="off")
