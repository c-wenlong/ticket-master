import { Hono } from "hono";
import { handle } from "hono/aws-lambda";
import { logger } from "hono/logger";

import { loadConfig } from "@/config";
import mongo from "@/db";
import { setupRoutes } from "@/handler";
import { errorMiddleware } from "@/middleware";

const cfg = loadConfig();
await mongo.MustInit(cfg);

const app = new Hono();

app.use("*", logger());
app.use("*", errorMiddleware);
setupRoutes(app);

if (process.env.NODE_ENV !== "production") {
  const { serve } = await import("@hono/node-server");

  serve({
    fetch: app.fetch,
    port: cfg.devHttpPort,
  });

  console.info(`Server started on port ${cfg.devHttpPort}`);
}

export const handler = handle(app);
