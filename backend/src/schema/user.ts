import * as z from 'zod';

export const RoleSchema = z.enum(["DEVELOPER", "DESIGNER", "MANAGER", "PRODUCT", "BUSINESS_DEVELOPMENT"]);

export const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(),
  role: RoleSchema,
})

export type User = z.infer<typeof UserSchema>;