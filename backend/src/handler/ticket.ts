import mongo from "@/db";
import { TicketSchema } from "@/schema/ticket";
import { Hono } from "hono";

export const setupTicketRoutes = (app: Hono) => {
  app.post("/ticket", async (c) => {
    const body = await c.req.json();
    const parseResult = TicketSchema.safeParse(body);
  
    if (!parseResult.success) {
      c.status(400);
      return c.json({ error: parseResult.error });
    }
  
    const ticket = parseResult.data;
    await mongo.db.collection("tickets").insertOne(ticket);
  
    return c.json({
      data: ticket,
      message: "Ticket created",
    });
  });

  app.get("/ticket/:id", async (c) => {
    const id = c.req.param('id');
    const ticket = await mongo.db.collection("tickets").findOne({ id });

    if (!ticket) {
      c.status(400);
      return c.json({
        error: "Ticket not found",
      });
    }
  
    return c.json({
      data: ticket,
      message: "success",
    });
  });

  app.get("/ticket", async (c) => {
    const tickets = await mongo.db.collection("tickets").find().toArray();
  
    return c.json({
      data: tickets,
      message: "success",
    });
  });

  app.put("/ticket/:id", async (c) => {
    const id = c.req.param('id');
    const body = await c.req.json();
    const parseResult = TicketSchema.safeParse(body);
  
    if (!parseResult.success) {
      c.status(400);
      return c.json({ error: parseResult.error });
    }
  
    const ticket = parseResult.data;
    await mongo.db.collection("tickets").updateOne({ id }, { $set: ticket });
  
    return c.json({
      data: ticket,
      message: "Ticket updated",
    });
  });

  app.delete("/ticket/:id", async (c) => {
    const id = c.req.param('id');
    await mongo.db.collection("tickets").deleteOne({ id });
  
    return c.json({
      message: "Ticket deleted",
    });
  });
}

