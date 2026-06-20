
# GitHub Actions Auto-Deploy to Hugging Face Setup

## Step 1: Get a Hugging Face Access Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it something like "GitHub Actions Deploy"
4. Set role to "Write" (required to push to your Space!)
5. Copy the token, we'll use this in Step 2

## Step 2: Add Secrets to Your GitHub Repository
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add the following secrets:
   - **Name**: `HF_TOKEN`
   - **Value**: Paste your Hugging Face access token from Step 1
4. Click "Add secret"

## Step 3: Verify Files are in Place
Make sure your repo has:
- ✅ `.github/workflows/deploy.yml`
- ✅ Root `Dockerfile`
- ✅ `README_SINGLE_SPACE.md` (will be renamed to README.md on deploy)
- ✅ All your backend/frontend files

## Step 4: That's It!
Now any time you push to your main/master branch, GitHub Actions will auto-deploy everything to your Hugging Face Space!

## Troubleshooting
- If deploy fails, check GitHub Actions log in your repo → Actions tab
- Double-check your `HF_TOKEN` has "Write" permissions
- Double-check the Hugging Face Space name in deploy.yml is exactly `aditya-ranjan1234/identitylens-ai`
