# 🚀 EAGLE Deployment Guide

## Option 1: Deploy via GitHub Web Interface (No Git CLI needed)

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in (or create an account)
2. Click the **+** icon in the top right → **New repository**
3. Name it: `eagle-appointment-system`
4. Make it **Public**
5. **DO NOT** initialize with README (we already have files)
6. Click **Create repository**

### Step 2: Upload Files to GitHub

1. On your new repository page, click **uploading an existing file**
2. Drag and drop ALL files from the `eagle_app` folder:
   - `app.py`
   - `eagle_database.py`
   - `appointment.py`
   - `notifications.py`
   - `requirements.txt`
   - `packages.txt`
   - `README.md`
   - `.gitignore`
   - The entire `views` folder (with all .py files inside)
   - The entire `.streamlit` folder (with config.toml inside)

3. Write commit message: "Initial commit - EAGLE app"
4. Click **Commit changes**

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **Sign in with GitHub**
3. Authorize Streamlit Cloud to access your repositories
4. Click **New app**
5. Fill in the form:
   - **Repository**: Select `your-username/eagle-appointment-system`
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
6. Click **Deploy!**

### Step 4: Wait for Deployment

- Streamlit Cloud will install dependencies and start your app
- This takes 2-5 minutes
- You'll get a URL like: `https://your-username-eagle-appointment-system.streamlit.app`

### Step 5: Share Your App

Your app is now live! Share the URL with your team.

---

## Option 2: Deploy via Git CLI (If you have Git installed)

### Install Git First

Download and install Git from: [git-scm.com/downloads](https://git-scm.com/downloads)

### Then run these commands:

```bash
cd eagle_app

# Initialize repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - EAGLE app"

# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Then follow Step 3 above to deploy on Streamlit Cloud.

---

## 📝 Important Notes

### Database Persistence

The SQLite database (`eagle.db`) will reset when Streamlit Cloud restarts. For production:

1. Consider using a cloud database (PostgreSQL, MySQL)
2. Or use Streamlit's file storage with proper backup strategy

### Credentials

Default login credentials are in the code. For production:

1. Move credentials to Streamlit secrets
2. Add environment variable support
3. Implement proper authentication

### File Structure for Upload

Make sure your GitHub repository has this structure:

```
eagle-appointment-system/
├── app.py
├── eagle_database.py
├── appointment.py
├── notifications.py
├── requirements.txt
├── packages.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── views/
    ├── __init__.py
    ├── seller_views.py
    ├── ibsc_views.py
    ├── noc_views.py
    ├── admin_views.py
    └── shared_views.py
```

---

## 🆘 Troubleshooting

### "Module not found" error
- Check that all files are uploaded
- Verify `requirements.txt` is present
- Check file paths in import statements

### App won't start
- Check Streamlit Cloud logs
- Verify `app.py` is in the root of your repository
- Ensure all dependencies are in `requirements.txt`

### Database issues
- Remember: SQLite resets on each deployment
- Check file permissions
- Consider cloud database for production

---

## 🎉 Success!

Once deployed, your EAGLE app will be accessible 24/7 at your Streamlit Cloud URL!
