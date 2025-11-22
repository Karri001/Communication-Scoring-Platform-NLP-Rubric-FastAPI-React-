# Deployment Guide

## Option A: Render (Backend) + Vercel (Frontend)

### Backend (Render)
1. Create new Web Service → connect GitHub repository.
2. Root directory: `backend`
3. Environment: Python 3.10+
4. Build command: leave blank (Render auto-installs via requirements.txt)
5. Start command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
6. Add platform variables if needed (none required by default).
7. Wait for deploy; note the URL (e.g., https://your-backend.onrender.com)

### Frontend (Vercel)
1. Import repo → advanced settings:
   - Root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`
2. Add Environment Variable:
   - `VITE_API_BASE_URL=https://your-backend.onrender.com`
3. Deploy.

### Test
Open frontend URL → paste transcript → Score → verify network call to backend.

## Option B: Hugging Face Space (Single Backend)
- Create Space → “SDK: Docker” or “Python”
- Copy backend directory files
- Add a simple `frontend/index.html` served via FastAPI static mount

## Option C: Streamlit (Simplified)
If time short, combine logic into one `app.py` with Streamlit.

## SSL / CORS
- Backend `main.py` sets CORS allow_origins=["*"] for dev; tighten in production.

## Model Cold Start
First request may take ~2–4s to load sentence-transformers; log this in README.
