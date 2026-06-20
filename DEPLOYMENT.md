
# IdentityLens AI - Hugging Face Deployment Guide

This guide will walk you through deploying both the backend and frontend to Hugging Face Spaces!

---

## Option 1 (Recommended): Deploy to a Single Space
Deploy everything in one container! Easier and cheaper!

### Step 1: Create a Single Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - Space name: `identitylens-ai`
   - Owner: your HF username
   - License: MIT
   - SDK: Docker
   - Hardware: CPU basic (free)
4. Click "Create Space"

### Step 2: Upload Files to Single Space
- Option A (UI):
  1. Open your new HF Space
  2. Go to "Files and versions"
  3. Click "Upload files"
  4. Upload ALL of the following (preserving directory structure!):
     - `backend/` (entire folder)
     - `frontend/` (entire folder)
     - `Dockerfile` (from root, created earlier)
     - `README.md` (rename `README_SINGLE_SPACE.md` to `README.md`)
  5. Click "Commit changes"
- Option B (Git Push):
  1. Clone your new space repo locally
  2. Copy all project files into it
  3. Rename `README_SINGLE_SPACE.md` to `README.md`
  4. Add, commit, push!

### Step 3 (Optional): Add OpenAI Key
1. In your HF Space, go to Settings → Secrets
2. Add a new secret: `OPENAI_API_KEY`
3. Click Save

---

### Step 4: Auto-Deploy via GitHub Actions (Optional but Recommended!)
To automatically deploy any changes you push to GitHub directly to your Hugging Face Space!

Follow the setup steps in `GITHUB_ACTIONS_SETUP.md`

---

## Option 2: Deploy to Two Separate Spaces

## Prerequisites
1. A [Hugging Face account (free tier works! https://huggingface.co/join
2. Git installed on your machine
3. (Optional) OpenAI API key if you want LLM explanations

---

## Step 1: Deploy the Backend to Hugging Face Space

### 1.1 Create a New Backend Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `identitylens-backend`
   - **Owner**: your HF username
   - **License**: Choose a license (MIT recommended)
   - **SDK**: Docker
   - **License**: MIT
   - **Hardware**: CPU basic (free)
4. Click "Create Space"

### 1.2 Upload Backend Files
Once your space is created, you have two options:
- **Option A: Use HF Upload Files via HF UI (easier for beginners)
  - Open your new HF Space in the browser
  - Go to the "Files and versions" tab
  - Click "Upload files"
  - Drag and drop the entire `backend/` folder contents (or one by one if needed, preserving directory structure):
    - `app/` folder (and all subfolders/files inside)
    - `data/` folder
    - `models/` folder
    - `scripts/` folder
    - `Dockerfile`
    - `README.md` (rename `README_HF_BACKEND.md` to `README.md`)
    - `requirements.txt`
    - `run_server.py`
- **Option B: Git Push (more advanced)**
  - Clone your space repository locally
  - Copy all `backend/` folder contents
  - Rename `README_HF_BACKEND.md` to `README.md`
  - Add, commit, and push

### 1.3 Set Optional Secrets (Optional)
If you want to use OpenAI for LLM risk explanations:
1. In your backend HF Space, go to "Settings" → "Secrets and variables"
2. Click "New secret"
3. Name: `OPENAI_API_KEY`
4. Value: Your OpenAI API key
5. Click "Save"

### 1.4 Verify Deployment
Once uploaded/pushed, your Space will automatically build and deploy!
You can see the deployment logs in "Logs tab.
Once ready, your backend API docs will be at: `https://<your-hf-username-identitylens-backend.hf.space/docs

---

## Step 2: Deploy the Frontend to Hugging Face Space

### 2.1 Create a New Frontend Space
1. Go back to https://huggingface.co/spaces
2. Click "Create new Space" again
3. Fill in details:
   - **Space name**: `identitylens-frontend`
   - **Owner**: your HF username
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free)
4. Click "Create Space"

### 2.2 Update Frontend Environment Variables
1. First, in your local frontend folder:
   - Copy `.env.local.example` to `.env.local`
   - Replace `http://localhost:8000` with your backend's HF URL (e.g., `https://<your-hf-username-identitylens-backend.hf.space`)
   - **Important:** For HF deployment we will set this as a variable in HF (Step 2.4

### 2.3 Upload Frontend Files
Again, two options:
- **Option A: Upload via UI**:
  - Go to new frontend HF Space → Files and versions
  - Upload entire `frontend/` folder contents, preserving structure:
    - `src/` folder
    - `public/` folder
    - `Dockerfile`
    - `README.md` (rename `README_HF_FRONTEND.md` to `README.md`)
    - `next.config.js`
    - `package-lock.json`
    - `package.json`
    - `tailwind.config.js
    - `postcss.config.js`
- **Option B: Git Push**

### 2.4 Set Frontend Environment Variable in HF
1. In your frontend HF Space:
   - Go to "Settings" → "Secrets and variables"
   - Click "New variable" (NOT "New secret")
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: Your full backend HF URL (without trailing slash, e.g., `https://<your-hf-username-identitylens-backend.hf.space`)
   - Click "Save"

### 2.5 Verify Deployment
Once uploaded/pushed, your frontend space will build and deploy!
It will be available at `https://<your-hf-username-identitylens-frontend.hf.space

---

## Step 3: Test the Full Deployment
1. Open your frontend HF Space URL
2. You should see the IdentityLens AI dashboard!
3. Test out the tabs - all should work!

---

## Troubleshooting Common Issues
- **Backend is not responding: Check HF Space Logs tab for errors
- **Frontend not loading backend calls failing: Make sure `NEXT_PUBLIC_API_URL` is correct and has no trailing slash, and your backend is deployed and running
- **Docker build errors**: Double-check that all files are uploaded correctly

---

## Congratulations! 🎉
Your IdentityLens AI is now deployed on Hugging Face Spaces!
