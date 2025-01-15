import { Hono } from "hono";

import mongo, { METRICS_COLLECTION } from "@/db";
import { EventSchema, QueryEventSchema } from "@/schema";

enum MetricStatusCode {
  Success = 0,
  IllegalPayload = 1000,
  MetricsNotFound = 1001,
}

export const metricRoutes = new Hono();

metricRoutes.post("/emit", async (c) => {
  const body = await c.req.json();
  const parseResult = EventSchema.safeParse(body);

  if (!parseResult.success) {
    const resp = {
      base: {
        code: MetricStatusCode.IllegalPayload,
        message: "Illegal metric data",
        errorMessage: parseResult.error.message,
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const event = parseResult.data;
  await mongo.db.collection(METRICS_COLLECTION).insertOne(event);

  const resp = {
    base: {
      code: MetricStatusCode.Success,
      message: "Metric emitted",
    },
    data: event,
  } satisfies HttpResponse;

  return c.json(resp);
});

metricRoutes.get("/:id", async (c) => {
  const id = c.req.param().id;
  const event = await mongo.db
    .collection(METRICS_COLLECTION)
    .findOne({ event_id: id });

  if (!event) {
    const resp = {
      base: {
        code: MetricStatusCode.MetricsNotFound,
        message: "Metric not found",
      },
    } satisfies HttpResponse;

    c.status(404);
    return c.json(resp);
  }

  const resp = {
    base: {
      code: MetricStatusCode.Success,
      message: "success",
    },
    data: event,
  } satisfies HttpResponse;

  return c.json(resp);
});

metricRoutes.post("/query", async (c) => {
  const body = await c.req.json();
  const parseResult = QueryEventSchema.safeParse(body);

  if (!parseResult.success) {
    const resp = {
      base: {
        code: MetricStatusCode.IllegalPayload,
        message: "Illegal query data",
        errorMessage: parseResult.error.message,
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const query = parseResult.data;
  const filter: any = {
    timestamp: { $gte: query.start, $lte: query.end },
  };


  if (query.ticket_status) {
    if (typeof query.ticket_status === "string") {
      filter.ticket_status = query.ticket_status;
    } else {
      filter.ticket_status = { $in: query.ticket_status };
    }
  }

  const events = await mongo.db
    .collection(METRICS_COLLECTION)
    .find(filter)
    .toArray();

  const resp = {
    base: {
      code: MetricStatusCode.Success,
      message: "success",
    },
    data: events,
  } satisfies HttpResponse;

  return c.json(resp);
});
