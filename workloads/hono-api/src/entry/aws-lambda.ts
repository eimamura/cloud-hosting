// AWS Lambda entry (API Gateway, Function URL, or ALB). Bundled to dist/aws-lambda.mjs; handler is `handler`.
import { handle } from "hono/aws-lambda";
import { app } from "../app.ts";

export const handler = handle(app);
