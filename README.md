# BeyondChats Assignment

This is a full‑stack project for BeyondChats.  
It includes:
- **Backend (FastAPI + MySQL)** → provides APIs for articles
- **Script‑Node (Node.js)** → scrapes blogs, updates articles using Google API + OpenAI
- **Frontend (React)** → displays updated articles in the browser

##  How to Run

### Backend
```bash
cd backend-fastapi
python -m venv venv
venv\Scripts\activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload --port 8000
###Script‑Node
cd script-node
npm install
npm start
###frontend-react
cd frontend-react
npm install
npm run dev
[GitHub Repository](https://github.com/esku21/beyondchats-assignment)
