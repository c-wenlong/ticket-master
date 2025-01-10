export const loadEnv = async () => {
  if (process.env.NODE_ENV === "production") {
    console.log("Not loading .env file in production");
    return;
  }

  const dotenv = await import("dotenv");

  dotenv.config({
    path: "../../.env",
  });

  console.log("Loaded .env file");
};
