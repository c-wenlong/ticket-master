export type AppConfig = {
  dbUserName: string;
  dbPassword: string;
  dbHost: string;
  dbName: string;
  dbPort: string;
  devHttpPort: number;
};

export const loadConfig = async () => {
  if (process.env.NODE_ENV !== "production") {
    await loadDotenv();
  } else {
    console.log("Running in production mode");
  }

  const config: AppConfig = {
    dbUserName: process.env.DOCUMENTDB_USERNAME ?? "admin",
    dbPassword: process.env.DOCUMENTDB_PASSWORD ?? "password",
    dbHost: process.env.DOCUMENTDB_HOSTNAME ?? "localhost",
    dbName: process.env.DOCUMENTDB_DATABASE ?? "ticket_master",
    dbPort: process.env.PORT ?? "27018",
    devHttpPort: Number(process.env.DEV_HTTP_PORT ?? "3000"),
  };

  console.log("Loaded config", config);

  return config;
};

const loadDotenv = async () => {
  const dotenv = await import("dotenv");
  const fs = await import("fs");
  const path = await import("path");
  
  const dotenvPath = path.resolve(__dirname, "../../../.env");

  if (!fs.existsSync(dotenvPath)) {
    console.warn(
      "No .env file found in root of project directory, using default values",
    );
    return;
  }

  const out = dotenv.config({
    path: dotenvPath,
  });

  if (out.error) {
    throw out.error;
  }

  console.log("Loaded .env file in development");
};
