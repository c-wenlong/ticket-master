import { Hono } from "hono";
import { metricRoutes } from "./metrics";
import { ticketRoutes } from "./ticket";

export const setupRoutes = (app: Hono) => {
  app.route("/ticket", ticketRoutes);
  app.route("/metrics", metricRoutes);
}