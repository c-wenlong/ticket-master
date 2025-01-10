import * as z from 'zod';

export const TicketSchema = z.object({})

export type Ticket = z.infer<typeof TicketSchema>;