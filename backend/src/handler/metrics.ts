import mongo, { METRICS_COLLECTION } from "@/db";
import { Hono } from "hono";

enum MetricStatusCode {
  Success = 0,
  IllegalPayload = 1000,
}

export const metricRoutes = new Hono();

metricRoutes.post("/emit", async (req, res) => {
  const metricCollection = mongo.db.collection(METRICS_COLLECTION);
})