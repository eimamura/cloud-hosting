// Vercel Functions entry. A deployment project re-exports this from `api/[[...route]].ts`
// and rewrites all paths to /api.
import { handle } from "hono/vercel";
import { app } from "../app.ts";

const handler = handle(app);

export const GET = handler;
export const POST = handler;
export const PUT = handler;
export const PATCH = handler;
export const DELETE = handler;
export const OPTIONS = handler;
