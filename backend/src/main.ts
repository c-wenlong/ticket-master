import mongo from "@/db";
import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { handle } from "hono/aws-lambda";
import { logger } from "hono/logger";
import { loadEnv } from "./env";
import { setupTicketRoutes } from "./handler/ticket";

await loadEnv();
await mongo.MustInit();

const app = new Hono();

app.use("*", logger());
setupTicketRoutes(app);

if (process.env.NODE_ENV !== "production") {
  console.log("Starting server");
  serve({
    fetch: app.fetch,
    port: 3000,
  });
}

export const handler = handle(app);
