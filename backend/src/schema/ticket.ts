import * as z from "zod";

export const StatusSchema = z.enum(["OPEN", "IN_PROGRESS", "DONE"]);

export const PrioritySchema = z.enum(["LOW", "MEDIUM", "HIGH"]);

export const TicketTypeSchema = z.enum(["BUG", "FEATURE", "TASK"]);

export const TicketSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  status: StatusSchema,
  priority: PrioritySchema,
  type: TicketTypeSchema,
  reporter_id: z.string(),
  embedding: z.optional(z.array(z.number())),
  parent_ticket_id: z.optional(z.string()),
  assignee_id: z.optional(z.string()),
  labels: z.optional(z.array(z.string())),
});

export type Ticket = z.infer<typeof TicketSchema>;
