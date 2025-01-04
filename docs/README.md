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