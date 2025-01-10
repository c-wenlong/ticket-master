import * as z from "zod"
import { SettingSchema } from "./setting"

export const ProjectSchema = z.object({
  id: z.string(),
  name: z.string(),
  members: z.array(z.string()),
  settings: SettingSchema,
})

export type Project = z.infer<typeof ProjectSchema>