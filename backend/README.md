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

### Metrics Collection Schema

```ts
export const TicketStatusSchema = z.enum(["in_progress", "open", "done"]);

export const EventSchema = z.object({
  event_id: z.string(),
  timestamp: z.number().int(),
  event_detail: z.string(),
  event_value: z.number().int(),
  ticket_id: z.string(),
  ticket_status: TicketStatusSchema,
});

export const QueryOperationSchema = z.literal("AND").or(z.literal("OR"));

export const QueryEventSchema = z.object({
  start: z.number().int(),
  end: z.number().int(),
  ticket_status: z.optional(TicketStatusSchema.or(z.array(TicketStatusSchema))),
});
```

### HTTP Endpoints

- `/metrics/emit` - POST - Emits metrics
  - Request Body: `EventSchema` 

```json
{
  "event_id": "xxxxxxxxxxxxxxxxxxxxx",
  "timestamp": 1630000000,
  "event_detail": "event detail",
  "event_value": 1,
  "ticket_id": "xxxxxxxxxxxxxxxxxxxxx",
  "ticket_status": "open"
}
```

- `/metrics/query` - POST - Query metrics
  - Request Body: `QueryEventSchema`

```json
{
  "start": 1630000000,
  "end": 1630000000,
  "ticket_status": ["open", "done"]
}

{
  "start": 1630000000,
  "end": 1630000000,
  "ticket_status": "open"
}
```
