// Deno / Deno Deploy entry: `deno run --allow-net --allow-env src/entry/deno.ts`.
import { app } from "../app.ts";

Deno.serve({ port: Number(Deno.env.get("PORT") ?? 8000) }, app.fetch);
