export const loadEnv = async () => {
  if (process.env.NODE_ENV === "production") {
    console.log("Not loading .env file in production");
    return;
  }

  const path = await import("path");
  const dotenv = await import("dotenv");

  const out = dotenv.config({
    path: path.resolve(__dirname, "../../.env"),
  });

  if (out.error) {
    console.error(out.error);
    throw out.error;
  }

  console.log("Loaded .env file");
};
