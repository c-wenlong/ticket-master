import mongo from "@/db";
import { setupRoutes } from "@/handler";
import { Hono } from "hono";
import { handle } from "hono/aws-lambda";
import { logger } from "hono/logger";
import { loadConfig } from "./config";

const cfg = await loadConfig();
await mongo.MustInit(cfg);

const app = new Hono();

app.use("*", logger());
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
