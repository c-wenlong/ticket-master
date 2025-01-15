import { Hono } from "hono";

import { metricRoutes } from "./metrics";

export const setupRoutes = (app: Hono) => {
  app.route("/metrics", metricRoutes);
}