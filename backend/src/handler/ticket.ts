import mongo from "@/db";
import { TICKET_COLLECTION } from "@/db/constant";
import { Ticket, TicketSchema } from "@/schema/ticket";
import { Hono } from "hono";

enum TicketStatusCode {
  Success = 0,
  IllegalPayload = 1000,
  TicketNotFound = 1001,
}

export const ticketRoutes = new Hono();

ticketRoutes.post("/", async (c) => {
  const body = await c.req.json();
  const parseResult = TicketSchema.safeParse(body);

  if (!parseResult.success) {
    const resp = {
      base: {
        code: TicketStatusCode.IllegalPayload,
        message: "Illegal ticket data",
        errorMessage: parseResult.error.message,
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const ticket = parseResult.data;
  await mongo.db.collection(TICKET_COLLECTION).insertOne(ticket);

  const resp = {
    base: {
      code: TicketStatusCode.Success,
      message: "Ticket created",
    },
    data: ticket,
  } satisfies HttpResponse<Ticket>;

  return c.json(resp);
});

ticketRoutes.get("/:id", async (c) => {
  const id = c.req.param("id");
  const ticket = await mongo.db.collection(TICKET_COLLECTION).findOne({ id });

  if (!ticket) {
    const resp = {
      base: {
        code: TicketStatusCode.TicketNotFound,
        message: "Ticket not found",
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const resp = {
    base: {
      code: TicketStatusCode.Success,
      message: "success",
    },
    data: ticket,
  } satisfies HttpResponse;

  return c.json(resp);
});

ticketRoutes.get("/", async (c) => {
  const tickets = await mongo.db.collection(TICKET_COLLECTION).find().toArray();

  const resp = {
    base: {
      code: TicketStatusCode.Success,
      message: "success",
    },
    data: tickets,
  } satisfies HttpResponse;

  return c.json(resp);
});

ticketRoutes.put("/:id", async (c) => {
  const id = c.req.param("id");
  const body = await c.req.json();
  const parseResult = TicketSchema.safeParse(body);

  if (!parseResult.success) {
    const resp = {
      base: {
        code: TicketStatusCode.IllegalPayload,
        message: "Illegal ticket data",
        errorMessage: parseResult.error.message,
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const ticket = parseResult.data;
  await mongo.db
    .collection(TICKET_COLLECTION)
    .updateOne({ id }, { $set: ticket });

  const resp = {
    base: {
      code: TicketStatusCode.Success,
      message: "Ticket updated",
    },
    data: ticket,
  };

  return c.json(resp);
});

ticketRoutes.delete("/:id", async (c) => {
  const id = c.req.param("id");
  await mongo.db.collection(TICKET_COLLECTION).deleteOne({ id });

  const resp = {
    base: {
      code: TicketStatusCode.Success,
      message: "Ticket deleted",
    },
  } satisfies HttpResponse;

  return c.json(resp);
});
