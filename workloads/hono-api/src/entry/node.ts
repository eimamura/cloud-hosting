// Node.js server. Used by Docker, container PaaS, VPS, and Kubernetes deployments.
import { serve } from "@hono/node-server";
import { app } from "../app.ts";

const port = Number(process.env.PORT ?? 8080);

const server = serve({ fetch: app.fetch, port, hostname: "0.0.0.0" }, (addr) => {
  console.log(`hono-api listening on http://${addr.address}:${addr.port}`);
});

// Exit promptly on container stop signals.
for (const signal of ["SIGINT", "SIGTERM"] as const) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
