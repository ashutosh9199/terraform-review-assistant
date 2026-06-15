# AI-Powered Terraform Review Assistant

An enterprise SaaS platform to automatically analyze Terraform infrastructure code for Security, Cost, Governance, and Operational best practices using Azure OpenAI.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React, TypeScript, Material UI, Vite
- **Infrastructure**: Terraform targeting Azure
- **CI/CD**: GitHub Actions

## Setup & Local Development
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Docker
Run the full stack locally:
```bash
docker-compose up --build
```
