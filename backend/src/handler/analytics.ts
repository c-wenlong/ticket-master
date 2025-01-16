import { Hono } from "hono";

import mongo, { SPRINT_COLLECTION } from "@/db";
import { EventSchema, Sprint, UpdateSprintSchema } from "@/schema";
import { ObjectId } from "mongodb";

enum StatusCode {
  Success = 0,
  IllegalPayload = 1000,
  SprintNotFound = 1001,
  SprintNotCreated = 1002,
}

export const analyticsRoutes = new Hono();

/**
 * Create a new sprint
 * Optional query parameters:
 * - start_time: unix timestamp in milliseconds. Defaults to current time
 * - end_time: unix timestamp in milliseconds. Defaults to undefined
 */
analyticsRoutes.post("/", async (c) => {
  const startTimeSearchParam = Number(c.req.query()["start_time"]);
  const endTimeSearchParam = Number(c.req.query()["end_time"]);

  const startTime = startTimeSearchParam
    ? new Date(startTimeSearchParam)
    : new Date();
  const endTime = !endTimeSearchParam
    ? undefined
    : endTimeSearchParam < startTimeSearchParam
    ? undefined
    : new Date(endTimeSearchParam);

  const sprint: Partial<Sprint> = {
    start_time: startTime,
    end_time: endTime,
    events: [],
  };

  const insertResult = await mongo.db
    .collection(SPRINT_COLLECTION)
    .insertOne(sprint);

  if (!insertResult.acknowledged) {
    const resp = {
      base: {
        code: StatusCode.SprintNotCreated,
        message: "Sprint not created",
      },
    } satisfies HttpResponse;

    c.status(500);
    return c.json(resp);
  }

  sprint.id = insertResult.insertedId.toHexString();
  const resp = {
    base: {
      code: StatusCode.Success,
      message: "Sprint created",
    },
    data: sprint,
  } satisfies HttpResponse;

  return c.json(resp);
});

analyticsRoutes.get("/", async (c) => {
  const sprints = await mongo.db.collection(SPRINT_COLLECTION).find().toArray();
  sprints.forEach((sprint) => {
    sprint.id = sprint._id.toHexString();
  });

  const resp = {
    base: {
      code: StatusCode.Success,
      message: "success",
    },
    data: sprints,
  } satisfies HttpResponse;

  return c.json(resp);
});

analyticsRoutes.get("/:id", async (c) => {
  const id = c.req.param().id;
  const sprint = await mongo.db
    .collection(SPRINT_COLLECTION)
    .findOne({ _id: new ObjectId(id) });

  if (!sprint) {
    const resp = {
      base: {
        code: StatusCode.SprintNotFound,
        message: "Sprint not found",
      },
    } satisfies HttpResponse;

    c.status(404);
    return c.json(resp);
  }

  sprint.id = sprint._id.toHexString();
  const resp = {
    base: {
      code: StatusCode.Success,
      message: "success",
    },
    data: sprint,
  } satisfies HttpResponse;

  return c.json(resp);
});

analyticsRoutes.post("/:id/emit_event", async (c) => {
  const body = await c.req.json();
  const sprintId = c.req.param().id;
  const parseResult = EventSchema.safeParse(body);

  if (!parseResult.success) {
    const resp = {
      base: {
        code: StatusCode.IllegalPayload,
        message: "Illegal payload",
        errorMessage: parseResult.error.message,
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const event = parseResult.data;
  const updateRes = await mongo.db
    .collection<Sprint>(SPRINT_COLLECTION)
    .updateOne({ _id: new ObjectId(sprintId) }, { $push: { events: event } });

  if (!updateRes.acknowledged) {
    const resp = {
      base: {
        code: StatusCode.SprintNotFound,
        message: "Sprint not found",
      },
    } satisfies HttpResponse;

    c.status(404);
    return c.json(resp);
  }

  const sprint = (await mongo.db
    .collection(SPRINT_COLLECTION)
    .findOne({ _id: new ObjectId(sprintId) }))!;
  sprint.id = sprint._id.toHexString();
  const resp = {
    base: {
      code: StatusCode.Success,
      message: "Metric emitted",
    },
    data: sprint,
  } satisfies HttpResponse;
  return c.json(resp);
});

analyticsRoutes.put("/:id", async (c) => {
  const body = await c.req.json();
  const sprintId = c.req.param().id;
  const parseResult = UpdateSprintSchema.safeParse(body);

  if (!parseResult.success) {
    const resp = {
      base: {
        code: StatusCode.IllegalPayload,
        message: "Illegal payload",
        errorMessage: parseResult.error.message,
      },
    } satisfies HttpResponse;

    c.status(400);
    return c.json(resp);
  }

  const updateSprint = parseResult.data;
  const updateRes = await mongo.db
    .collection(SPRINT_COLLECTION)
    .updateOne({ _id: new ObjectId(sprintId) }, { $set: updateSprint });

  if (!updateRes.acknowledged) {
    const resp = {
      base: {
        code: StatusCode.SprintNotFound,
        message: "Sprint not found",
      },
    } satisfies HttpResponse;

    c.status(404);
    return c.json(resp);
  }

  const sprint = (await mongo.db
    .collection(SPRINT_COLLECTION)
    .findOne({ _id: new ObjectId(sprintId) }))!;
    
  sprint.id = sprint._id.toHexString();
  const resp = {
    base: {
      code: StatusCode.Success,
      message: "Sprint updated",
    },
    data: sprint,
  } satisfies HttpResponse;
  return c.json(resp);
});
