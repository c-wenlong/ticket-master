import { Hono } from "hono";

import { analyticsRoutes } from "./analytics";

export const setupRoutes = (app: Hono) => {
  app.route("/analytics", analyticsRoutes);
}