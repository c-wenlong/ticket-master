import { Hono } from "hono";

import mongo, { METRICS_COLLECTION } from "@/db";

enum MetricStatusCode {
  Success = 0,
  IllegalPayload = 1000,
}

export const metricRoutes = new Hono();

metricRoutes.post("/emit", async (req, res) => {
  const metricCollection = mongo.db.collection(METRICS_COLLECTION);
});
