### Setup local development environment
- Install [pnpm](https://pnpm.io/installation) 

```bash
cd backend
# download or copy global-bundle.pem to backend folder
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

pnpm i
```

### Runtime environment variables

- The following environment variables are expected to be present in `.env` during development or the runtime environment in production.

```txt
DOCUMENTDB_USERNAME // Database username
DOCUMENTDB_PASSWORD // Database password
DOCUMENTDB_HOSTNAME // Database host
DOCUMENTDB_DATABASE // Database name
PORT // Database port
```

### Run local development environment

```bash
cd backend
pnpm start
```

### Build for production

```bash
cd backend
pnpm build:prod
```

- The build artifacts will be stored in the `backend/dist` directory. Entry point is `backend/dist/index.js`
