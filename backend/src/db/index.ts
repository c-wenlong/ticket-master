import { Db, MongoClient } from "mongodb";

let mongoClient: Optional<MongoClient> = null;
let db: Optional<Db> = null;

const MustInit = async () => {
  const dbUserName = process.env.DOCUMENTDB_USERNAME;
  const dbPassword = process.env.DOCUMENTDB_PASSWORD;
  const dbHost = process.env.DOCUMENTDB_HOSTNAME;
  const dbPort = process.env.PORT;

  if (!dbUserName || !dbPassword || !dbHost || !dbPort) {
    throw new Error("MongoDB environment variables are not set");
  }

  const uri = `mongodb://${dbUserName}:${encodeURIComponent(dbPassword)}@${dbHost}:${dbPort}/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false`;

  mongoClient = new MongoClient(uri);
  await mongoClient.connect();
  db = mongoClient.db();

  console.log("MongoDB connected");
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
