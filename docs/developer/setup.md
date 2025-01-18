# TicketMaster Setup Guide

## Overview

TicketMaster is a full-stack ticket management system built with Streamlit, OpenAI, and QDrant. This guide provides comprehensive setup instructions for both frontend and backend components.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git
- Code editor (Cursor recommended)
- QDrant account
- OpenAI API key

## Project Structure

### Frontend Directory (`frontend/`)

```
src/
├── .streamlit/          # Streamlit configuration and secrets
├── components/          # Reusable UI components
│   ├── card.py         # Kanban card component
│   ├── form.py         # Ticket creation forms
│   ├── kanban.py       # Kanban board component
│   └── table.py        # Ticket table component
├── notebooks/          # Jupyter notebooks for development
├── pages/              # Streamlit pages
│   ├── 🏠_Home.py      # Home page
│   ├── 🎫_Tickets_Overview.py  # Tickets list view
│   └── 🎯_Kanban_Board.py     # Kanban board view
├── services/           # Backend service integrations
│   ├── openai.py      # OpenAI service integration
│   └── qdrant.py      # QDrant service integration
├── App.py             # Main Streamlit application
└── .gitignore         # Git ignore configuration
```

### Backend Directory (`backend/`)

```
src/
├── documentdb/        # DocumentDB CRUD operations
│   ├── __init__.py
│   └── crud.py
├── services/         # Service handlers
│   ├── openai/      # OpenAI integration
│   │   ├── __init__.py
│   │   └── handler.py
│   └── qdrant/      # QDrant integration
│       ├── __init__.py
│       └── handler.py
└── .gitignore       # Git ignore configuration
```

## Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ticket-master.git
cd ticket-master
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration Setup

### Frontend Configuration (.streamlit/secrets.toml)

1. Create the `.streamlit` directory:

```bash
mkdir frontend/.streamlit
```

2. Create and configure secrets.toml:

```bash
touch frontend/.streamlit/secrets.toml
```

3. Add the following configuration (replace with your actual values):

```toml
[QDRANT]
QDRANT_URL = "https://your-qdrant-instance.cloud.qdrant.io:6333"
QDRANT_API_KEY = "your-qdrant-api-key"
COLLECTION_NAME = "tickets"

[OPENAI]
OPENAI_API_KEY = "your-openai-api-key"

[DOCUMENTDB]
CONNECTION_STRING = "your-documentdb-connection-string"
DATABASE_NAME = "ticketmaster"
COLLECTION_NAME = "tickets"
```

### Backend Configuration (.env)

1. Create .env file in the backend directory:

```bash
touch backend/.env
```

2. Add the following configuration:

```env
# QDrant Configuration
QDRANT_URL=https://your-qdrant-instance.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=tickets

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# DocumentDB Configuration
DOCUMENT_DB_CONNECTION_STRING=your-documentdb-connection-string
DOCUMENT_DB_NAME=ticketmaster
DOCUMENT_DB_COLLECTION=tickets
```

## Security Best Practices

1. Add configuration files to .gitignore:

```bash
# Add to .gitignore
frontend/.streamlit/secrets.toml
backend/.env
```

2. Create example configuration files:

```bash
# Create frontend/streamlit.secrets.example.toml
[QDRANT]
QDRANT_URL = "your-qdrant-url"
QDRANT_API_KEY = "your-qdrant-api-key"
COLLECTION_NAME = "collection-name"

[OPENAI]
OPENAI_API_KEY = "your-openai-api-key"

# Create backend/.env.example
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
OPENAI_API_KEY=your-openai-api-key
```

## Running the Application

### Frontend

```bash
cd frontend
streamlit run src/App.py
```

### Backend Development

```bash
cd backend
python -m uvicorn main:app --reload
```

## Accessing Secrets in Code

### Frontend (Streamlit)

```python
import streamlit as st

# QDrant configuration
qdrant_url = st.secrets["QDRANT"]["QDRANT_URL"]
qdrant_api_key = st.secrets["QDRANT"]["QDRANT_API_KEY"]
collection_name = st.secrets["QDRANT"]["COLLECTION_NAME"]

# OpenAI configuration
openai_api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]
```

### Backend (Python)

```python
import os
from dotenv import load_dotenv

load_dotenv()

# QDrant configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

## Troubleshooting

### Common Issues and Solutions

1. **Missing Dependencies**

   - Error: ModuleNotFoundError
   - Solution: Run `pip install -r requirements.txt`

2. **Configuration Issues**

   - Error: KeyError in st.secrets
   - Solution: Verify secrets.toml format and presence

3. **QDrant Connection**

   - Error: Connection refused
   - Solution: Check URL and API key in configuration

4. **OpenAI API**
   - Error: Invalid API key
   - Solution: Verify OpenAI API key in configuration

### Development Tools

1. **VS Code Extensions**

   - Python
   - Streamlit
   - TOML
   - Python Environment Manager

2. **Debugging**
   - Use `st.write()` for Streamlit debugging
   - Enable Streamlit's debug mode in development

## Best Practices

1. **Version Control**

   - Never commit secrets or configuration files
   - Use example configuration files
   - Regular commits with meaningful messages

2. **Development Workflow**

   - Use separate branches for features
   - Test locally before deployment
   - Follow code style guidelines

3. **Security**
   - Keep secrets secure
   - Regularly rotate API keys
   - Use environment-specific configurations

## Support and Resources

- QDrant Documentation: https://qdrant.tech/documentation/
- Streamlit Documentation: https://docs.streamlit.io/
- OpenAI API Documentation: https://platform.openai.com/docs/
