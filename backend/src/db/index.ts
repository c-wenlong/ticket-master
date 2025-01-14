import { AppConfig } from "@/config";
import { Db, MongoClient } from "mongodb";

let mongoClient: Optional<MongoClient> = null;
let db: Optional<Db> = null;

const MustInit = async (cfg: AppConfig) => {
  let uri = `mongodb://${cfg.dbUserName}:${encodeURIComponent(
    cfg.dbPassword,
  )}@${cfg.dbHost}:${
    cfg.dbPort
  }/?readPreference=secondaryPreferred&retryWrites=false`;
  if (process.env.NODE_ENV === "production") {
    uri += "&tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0";
  }

  mongoClient = new MongoClient(uri);
  await mongoClient.connect();
  db = mongoClient.db(cfg.dbName);

  console.info("MongoDB connected");
};

export default {
  get client() {
    if (!mongoClient) {
      throw new Error("MongoDB client is not initialized");
    }

    return mongoClient;
  },

  get db() {
    if (!db) {
      throw new Error("MongoDB database is not initialized");
    }

    return db;
  },

  MustInit,
};

export * from "./constant";
export * from "./type";
