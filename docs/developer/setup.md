# TicketMaster Setup Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Create and activate a virtual environment:

```bash
# On Windows
python -m .venv .venv
.\.venv\Scripts\activate

# On macOS/Linux
python3 -m .venv .venv
source .venv/bin/activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

### Frontend Directory Structure

```src/ # Root source directory
├── components/         # Reusable UI components for Streamlit frontend
├── notebooks/          # Jupyter notebooks for development and setup
├── pages/              # Streamlit pages and routes
├── services/          # Backend service integrations (OpenAI, Qdrant, etc.)
├── App.py             # Entry point for streamlit
└── .gitignore         # Git ignore configuration
```

### Backend Directory Structure

```src/ # Root source directory
├── documentdb/         # Reusable CRUD components for Serverless API Interface (DocumentDB)
├── services/          # Handlers for Serverless API Interface
    ├── openai         # OpenAI LLM Handlers
    └── qdrant         # Qdrant Vector DB Handlers
└── .gitignore         # Git ignore configuration (TODO)
```

## Streamlit Secrets Configuration

1. Create a `.streamlit` directory in your project root:
```bash
mkdir frontend/.streamlit
```

2. Create a `secrets.toml` file inside the `.streamlit` directory:
```bash
touch frontend/.streamlit/secrets.toml
```

3. Add your configuration secrets to `secrets.toml`, you can use `.streamlit.secrets.example.toml` file as an example:
```toml
["QDRANT"]
QDRANT_URL="https://e4006880-32d2-45b3-9bec-d22b237c2985.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY="API_KEY"
COLLECTION_NAME="NAME"

["OPENAI"]
OPENAI_API_KEY="API_KEY"
```

4. Add `.streamlit/secrets.toml` to your `.gitignore` file:
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

5. Access secrets in your Streamlit app:
```python
import streamlit as st

# Access your secrets
openai_key = st.secrets["OPENAI_API_KEY"]
db_connection = st.secrets["DOCUMENT_DB_CONNECTION_STRING"]
```

## Running the Application

1. Make sure you have the file `frontend/src/App.py`, this is the entry point to the application. All files within `frontend/src/pages/` will also be rendered when you load `App.py`.

2. Run the Streamlit app:

```bash
streamlit run frontend/src/App.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`.

## Troubleshooting

If you encounter any issues:

1. Ensure all required packages are installed
2. Check that all enum values match between Status, Priority, and Type
3. Verify that ticket dictionary structure matches the expected format
4. Clear browser cache if changes aren't reflecting
5. Verify that your `secrets.toml` file is properly formatted and contains all required credentials

## Lambda Backend Docker Container Build Setup

1. Navigate to

```
backend\src\ticket
```
2. Build Image
```
docker build -t test:{folder_name} --build-arg LAMBDA_FUNC_PATH={folder_name} .
```

where folder_name is the backend function folder you wish to build. e.g.

```
docker build -t test:create --build-arg LAMBDA_FUNC_PATH=create .
```

3. Tag Image
```
docker tag test:{folder_name} 590183762717.dkr.ecr.ap-southeast-1.amazonaws.com/test:{folder_name}
```

4. Push Image
```
docker push 590183762717.dkr.ecr.ap-southeast-1.amazonaws.com/test:{folder_name}
```