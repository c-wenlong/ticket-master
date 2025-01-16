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

## Endpoints

### 1. **Create a New Sprint**
**Endpoint:**
```
POST /analytics/
```
**Description:** Creates a new sprint.

**Optional Query Parameters:**
- `start_time` (number): Unix timestamp in milliseconds for the sprint start time. Defaults to the current time.
- `end_time` (number): Unix timestamp in milliseconds for the sprint end time. Must be after `start_time`. Defaults to `undefined`.

**Example cURL:**
```bash
curl -X POST "http://localhost:3000/analytics?start_time=1672531200000&end_time=1672617600000"
```
**Response:**
```json
{
  "base": {
    "code": 0,
    "message": "Sprint created"
  },
  "data": {
    "id": "<sprint_id>",
    "start_time": 1672531200000,
    "end_time": 1672617600000,
    "events": []
  }
}
```

---

### 2. **Get All Sprints**
**Endpoint:**
```
GET /analytics/
```
**Description:** Retrieves all sprints.

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/analytics"
```
**Response:**
```json
{
  "base": {
    "code": 0,
    "message": "success"
  },
  "data": [
    {
      "id": "<sprint_id>",
      "start_time": 1672531200000,
      "end_time": 1672617600000,
      "events": []
    }
  ]
}
```

---

### 3. **Get a Sprint by ID**
**Endpoint:**
```
GET /analytics/:id
```
**Description:** Retrieves a sprint by its ID.

**Path Parameters:**
- `id` (string): The ID of the sprint.

**Example cURL:**
```bash
curl -X GET "http://localhost:3000/analytics/<sprint_id>"
```
**Response:**
```json
{
  "base": {
    "code": 0,
    "message": "success"
  },
  "data": {
    "id": "<sprint_id>",
    "start_time": 1672531200000,
    "end_time": 1672617600000,
    "events": []
  }
}
```

---

### 4. **Emit an Event to a Sprint**
**Endpoint:**
```
POST /analytics/:id/emit_event
```
**Description:** Adds an event to the specified sprint.

**Path Parameters:**
- `id` (string): The ID of the sprint.

**Request Body:**
- `ticket_id` (string): The ID of the ticket.
- `timestamp` (number): Unix timestamp for the event.
- `description` (string): Description of the event.
- `status` (string): One of `"in_progress"`, `"open"`, `"done"`.
- `priority` (string): One of `"low"`, `"medium"`, `"high"`.

**Example cURL:**
```bash
curl -X POST "http://localhost:3000/analytics/<sprint_id>/emit_event" \
     -H "Content-Type: application/json" \
     -d '{
       "ticket_id": "TICKET_ABCD",
       "timestamp": 1672531200000,
       "description": "Fixing a bug",
       "status": "in_progress",
       "priority": "high"
     }'
```
**Response:**
```json
{
  "base": {
    "code": 0,
    "message": "Metric emitted"
  },
  "data": {
    "id": "<sprint_id>",
    "start_time": 1672531200000,
    "end_time": 1672617600000,
    "events": [
      {
        "ticket_id": "TICKET_ABCD",
        "timestamp": 1672531200000,
        "description": "Fixing a bug",
        "status": "in_progress",
        "priority": "high"
      }
    ]
  }
}
```

---

### 5. **Update a Sprint**
**Endpoint:**
```
PUT /analytics/:id
```
**Description:** Updates a sprint's details.

**Path Parameters:**
- `id` (string): The ID of the sprint.

**Request Body:**
- `start_time` (number, optional): New start time in milliseconds.
- `end_time` (number, optional): New end time in milliseconds.

**Example cURL:**
```bash
curl -X PUT "http://localhost:3000/analytics/<sprint_id>" \
     -H "Content-Type: application/json" \
     -d '{
       "end_time": 1672704000000
     }'
```
**Response:**
```json
{
  "base": {
    "code": 0,
    "message": "Sprint updated"
  },
  "data": {
    "id": "<sprint_id>",
    "start_time": 1672531200000,
    "end_time": 1672704000000,
    "events": []
  }
}
```

