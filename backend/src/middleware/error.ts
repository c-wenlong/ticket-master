import { MiddlewareHandler } from "hono";

export const errorMiddleware: MiddlewareHandler = async (c, next) => {
  await next();

  if (c.error) {
    console.error(c.error);

    const resp = {
      base: {
        code: 5000,
        message: "Internal server error",
        errorMessage: c.error.message,
      },
    } satisfies HttpResponse;

    c.status(500);
    c.json(resp);
  }
};
