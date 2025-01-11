export type AppConfig = {
  dbUserName: string;
  dbPassword: string;
  dbHost: string;
  dbPort: string;
  devHttpPort: number;
};

export const loadConfig = async () => {
  if (process.env.NODE_ENV !== "production") {
    const path = await import("path");
    const dotenv = await import("dotenv");

    const out = dotenv.config({
      path: path.resolve(__dirname, "../../.env"),
    });

    if (out.error) {
      throw out.error;
    }

    console.log("Loaded .env file in development");
  }

  const config: AppConfig = {
    dbUserName: process.env.DOCUMENTDB_USERNAME ?? "admin",
    dbPassword: process.env.DOCUMENTDB_PASSWORD ?? "password",
    dbHost: process.env.DOCUMENTDB_HOSTNAME ?? "localhost",
    dbPort: process.env.PORT ?? "27018",
    devHttpPort: Number(process.env.DEV_HTTP_PORT ?? "3000"),
  };

  return config;
};
