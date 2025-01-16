import * as z from "zod";

export const TicketStatusSchema = z.enum(["in_progress", "open", "done"]);

export const TicketPrioritySchema = z.enum(["low", "medium", "high"]);

export const EventSchema = z.object({
  ticket_id: z.string(),
  timestamp: z.number().int(),
  description: z.string(),
  status: TicketStatusSchema,
  priority: TicketPrioritySchema,
});

export type Event = z.infer<typeof EventSchema>;

export const SprintSchema = z.object({
  id: z.string(),
  start_time: z.coerce.date(),
  end_time: z.coerce.date(),
  events: z.array(EventSchema).optional(),
})

export const UpdateSprintSchema = SprintSchema.partial().omit({ id: true, events: true});

export type Sprint = z.infer<typeof SprintSchema>;

export type UpdateSprint = z.infer<typeof UpdateSprintSchema>;