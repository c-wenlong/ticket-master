import * as z from "zod";

export const SettingSchema = z.object({
  duplicate_threshold: z.number(),
  max_ticket_size: z.number(),
});

export type Setting = z.infer<typeof SettingSchema>;