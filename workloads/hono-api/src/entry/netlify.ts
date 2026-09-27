// Netlify Functions (v2) entry. A deployment project re-exports this from `netlify/functions/`.
import { app } from "../app.ts";

export default (request: Request) => app.fetch(request);

export const config = { path: "/*" };
