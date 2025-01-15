import * as z from "zod";

export const TicketStatusSchema = z.enum(["in_progress", "open", "done"]);

export const EventSchema = z.object({
  event_id: z.string(),
  timestamp: z.number().int(),
  event_detail: z.string(),
  event_value: z.number().int(),
  ticket_id: z.string(),
  ticket_status: TicketStatusSchema,
});

export const QueryOperationSchema = z.literal("AND").or(z.literal("OR"));

export const QueryEventSchema = z.object({
  start: z.number().int(),
  end: z.number().int(),
  ticket_status: z.optional(TicketStatusSchema.or(z.array(TicketStatusSchema))),
});
