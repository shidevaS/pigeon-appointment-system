# 🕊️ PIGEON — P3P Interaction Gateway to Engage Online

Category Appointment Management portal for P3P sellers, IBSC, and NOC teams.

## 🚀 Live Demo

[Access PIGEON on Streamlit Cloud](https://pigeon-sims.streamlit.app)

## 🛠️ Local Setup

```bash
cd pigeon_app
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository, branch (`main`), and main file path (`app.py`)
6. Click "Deploy"

## 🔐 Login Credentials

**Admin:**
- Username: `admin`
- Password: `Admin@SIMS2026!`

**Sellers:**
- Username: `rk` | Password: `RK#Vendor2026$`
- Username: `kkoc` | Password: `KKOC@Secure2026!`
- Username: `etrade` | Password: `Etrade#Pass2026$`
- Username: `cocoblu` | Password: `CoCoblu@2026!Secure`
- Username: `retailez` | Password: `RetailEz#2026$Pass`
- Username: `clicktech` | Password: `ClickTech@Secure26!`
- Username: `ohl` | Password: `OHL#Vendor2026$`

**IBSC Team:**
- Username: `ibsc`
- Password: `IBSC@Team2026!Secure`

**NOC Team:**
- Username: `noc`
- Password: `NOC#Operations2026$`

## Project Structure

```
pigeon_app/
├── app.py                  # Entry point
├── pigeon_database.py      # SQLite database layer
├── appointment.py          # Appointment business logic
├── notifications.py        # Notification & activity log helpers
├── requirements.txt
└── views/
    ├── seller_views.py     # Seller UI
    ├── ibsc_views.py       # IBSC team UI
    ├── noc_views.py        # NOC team UI
    ├── admin_views.py      # Admin UI
    └── shared_views.py     # Shared dashboard & all-appointments view
```
