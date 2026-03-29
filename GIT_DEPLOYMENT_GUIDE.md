# 🚀 Deploy EAGLE App Using Git Commands

## Step 1: Install Git

### Download and Install Git:
1. Go to: https://git-scm.com/download/win
2. Download "64-bit Git for Windows Setup"
3. Run the installer
4. Use default settings (just keep clicking "Next")
5. Click "Install"
6. Click "Finish"

### Verify Installation:
Open a NEW PowerShell/CMD window and run:
```bash
git --version
```
You should see: `git version 2.x.x`

---

## Step 2: Configure Git (First Time Only)

Open PowerShell/CMD and run these commands (replace with YOUR info):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Example:
```bash
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
```

---

## Step 3: Create GitHub Repository

### Option A: Via GitHub Website (Easier)
1. Go to: https://github.com/new
2. Repository name: `eagle-appointment-system`
3. Make it **Public**
4. **DO NOT** check "Add a README file"
5. Click "Create repository"
6. **COPY the repository URL** (looks like: `https://github.com/YOUR-USERNAME/eagle-appointment-system.git`)

### Option B: Via GitHub CLI (Advanced)
If you have GitHub CLI installed:
```bash
gh repo create eagle-appointment-system --public
```

---

## Step 4: Deploy Using Git Commands

Open PowerShell/CMD and navigate to your project folder:

```bash
cd C:\Users\PC\Desktop\Pigion\pigeon_app
```

### Run these commands ONE BY ONE:

#### 1. Initialize Git repository
```bash
git init
```

#### 2. Add all files
```bash
git add .
```

#### 3. Commit files
```bash
git commit -m "Initial commit - EAGLE appointment system"
```

#### 4. Rename branch to main
```bash
git branch -M main
```

#### 5. Add remote repository (REPLACE with YOUR GitHub URL)
```bash
git remote add origin https://github.com/YOUR-USERNAME/eagle-appointment-system.git
```

**Example:**
```bash
git remote add origin https://github.com/johndoe/eagle-appointment-system.git
```

#### 6. Push to GitHub
```bash
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (NOT your GitHub password)

---

## Step 5: Create GitHub Personal Access Token (If Needed)

If Git asks for a password:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Note: `Git access for EAGLE app`
4. Expiration: 90 days (or your choice)
5. Select scopes: Check **repo** (all sub-options)
6. Click "Generate token"
7. **COPY the token** (you won't see it again!)
8. Use this token as your password when Git asks

---

## Step 6: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository**: `your-username/eagle-appointment-system`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy!"

Wait 2-3 minutes for deployment to complete.

---

## 🔄 Update Your App Later

When you make changes to your code:

```bash
# Navigate to project folder
cd C:\Users\PC\Desktop\Pigion\pigeon_app

# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

Streamlit Cloud will automatically redeploy your app!

---

## 🆘 Troubleshooting

### Error: "git: command not found"
**Solution:** Git is not installed or not in PATH. Restart your terminal after installing Git.

### Error: "fatal: not a git repository"
**Solution:** Run `git init` first in your project folder.

### Error: "remote origin already exists"
**Solution:** Remove and re-add:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/eagle-appointment-system.git
```

### Error: "failed to push some refs"
**Solution:** Pull first, then push:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: "Authentication failed"
**Solution:** Use a Personal Access Token instead of your password.

### Error: "Permission denied"
**Solution:** Make sure you're the owner of the GitHub repository.

---

## 📋 Complete Command Sequence (Copy-Paste)

**After installing Git and creating GitHub repo, run these:**

```bash
# Navigate to project
cd C:\Users\PC\Desktop\Pigion\pigeon_app

# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - EAGLE appointment system"

# Rename branch
git branch -M main

# Add remote (REPLACE with YOUR URL)
git remote add origin https://github.com/YOUR-USERNAME/eagle-appointment-system.git

# Push to GitHub
git push -u origin main
```

---

## ✅ Success Indicators

You've successfully deployed when:
- ✅ Git push completes without errors
- ✅ Files appear on your GitHub repository
- ✅ Streamlit Cloud shows "Your app is live!"
- ✅ You can access your app URL

---

## 🎯 Quick Reference

**Check Git status:**
```bash
git status
```

**View commit history:**
```bash
git log --oneline
```

**View remote URL:**
```bash
git remote -v
```

**Pull latest changes:**
```bash
git pull
```

**Push changes:**
```bash
git push
```

---

## 🔗 Useful Links

- Git Download: https://git-scm.com/download/win
- GitHub: https://github.com
- GitHub Tokens: https://github.com/settings/tokens
- Streamlit Cloud: https://share.streamlit.io
- Git Documentation: https://git-scm.com/doc

---

Your EAGLE app will be live after following these steps! 🦅🎉
