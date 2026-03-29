# ⚡ Quick Start - Deploy EAGLE in 5 Minutes

## What You Need
- GitHub account (free at [github.com](https://github.com))
- All files in the `eagle_app` folder

## 🎯 Fastest Way to Deploy

### 1️⃣ Create GitHub Repository (2 minutes)

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `eagle-appointment-system`
3. Make it **Public**
4. Click **Create repository**

### 2️⃣ Upload Files (2 minutes)

On the repository page, click **"uploading an existing file"**

**Drag these files from your `eagle_app` folder:**

Core files:
- ✅ `app.py`
- ✅ `eagle_database.py`
- ✅ `appointment.py`
- ✅ `notifications.py`
- ✅ `requirements.txt`
- ✅ `README.md`

Folders (upload entire folders):
- ✅ `views/` folder (contains 6 Python files)
- ✅ `.streamlit/` folder (contains config.toml)

Optional:
- ✅ `.gitignore`
- ✅ `packages.txt`

Click **Commit changes**

### 3️⃣ Deploy to Streamlit Cloud (1 minute)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select:
   - Repository: `your-username/eagle-appointment-system`
   - Branch: `main`
   - Main file: `app.py`
5. Click **Deploy!**

### 4️⃣ Done! 🎉

Wait 2-3 minutes for deployment. You'll get a URL like:
```
https://your-username-eagle-appointment-system.streamlit.app
```

---

## 🔐 Login Credentials

**Sellers:**
- Username: `rk`, `kkoc`, `etrade`, `cocoblu`, `retailez`, `clicktech`, `ohl`
- Password: `vendor123`

**IBSC Team:**
- Username: `ibsc`
- Password: `ibsc123`

**NOC Team:**
- Username: `noc`
- Password: `noc123`

**Admin:**
- Username: `admin`
- Password: `admin123`

---

## 📁 Files Checklist

Before uploading, verify you have these files:

```
eagle_app/
├── ✅ app.py (main entry point)
├── ✅ eagle_database.py (database layer)
├── ✅ appointment.py (business logic)
├── ✅ notifications.py (notifications)
├── ✅ requirements.txt (dependencies)
├── ✅ README.md (documentation)
├── ✅ .gitignore (git ignore rules)
├── ✅ packages.txt (system packages)
├── ✅ .streamlit/
│   └── ✅ config.toml (theme config)
└── ✅ views/
    ├── ✅ __init__.py
    ├── ✅ seller_views.py
    ├── ✅ ibsc_views.py
    ├── ✅ noc_views.py
    ├── ✅ admin_views.py
    └── ✅ shared_views.py
```

---

## 🆘 Need Help?

**Can't find files?**
- All files are in: `C:\Users\PC\Desktop\Pigion\eagle_app\`

**Upload failed?**
- Try uploading files in smaller batches
- Make sure to upload the `views` folder as a folder (not individual files)

**Deployment error?**
- Check Streamlit Cloud logs
- Verify all files were uploaded
- Make sure `app.py` is in the root (not in a subfolder)

---

## 🎊 You're All Set!

Your EAGLE app will be live and accessible worldwide!
