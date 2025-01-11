import { Hono } from "hono";
import { ticketRoutes } from "./ticket";

export const setupRoutes = (app: Hono) => {
  app.route("/ticket", ticketRoutes);
}