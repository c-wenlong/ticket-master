### For frontend, we use st.secrets[] to access our api keys.
1. Create a folder in the frontend/ called `.streamlit`.
2. Create a file called `secrets.toml`.
3. Insert your API here, in the following format.
```toml
API_KEY="vdvdfdvdfvdsnvkljnfvkljsn3498832g5b24"
```
### For backend, we use a `.env` file to store our api keys.

# Frontend Directory Structure

```src/ # Root source directory
├── components/         # Reusable UI components for Streamlit frontend
├── notebooks/          # Jupyter notebooks for development and setup
├── pages/              # Streamlit pages and routes
├── services/           # Backend service integrations (OpenAI, Qdrant, etc.)
├── App.py              # Entry point for streamlit
└── .gitignore          # Git ignore configuration
```

# Backend Directory Structure

```src/ # Root source directory
├── documentdb/         # Reusable CRUD components for Serverless API Interface (DocumentDB)
├── services/           # Handlers for Serverless API Interface
    ├── openai          # OpenAI LLM Handlers
    └── qdrant          # Qdrant Vector DB Handlers
└── .gitignore          # Git ignore configuration (TODO)
```