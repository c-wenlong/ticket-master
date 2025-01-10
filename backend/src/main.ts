import mongo from "@/db";
import { Hono } from "hono";
import { handle } from "hono/aws-lambda";
import { logger } from "hono/logger";
import { loadEnv } from "./env";

await loadEnv();
await mongo.MustInit();

const app = new Hono();

app.use("*", logger());

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

export const handler = handle(app);
