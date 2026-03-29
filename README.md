# 🦅 EAGLE — P3P Interaction Gateway to Engage Online

Category Appointment Management portal for P3P sellers, IBSC, and NOC teams.

## 🚀 Live Demo

[Access EAGLE on Streamlit Cloud](https://your-app-url.streamlit.app) _(Update after deployment)_

## 🛠️ Local Setup

```bash
cd eagle_app
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

## Credentials

| Role   | Username    | Password   |
|--------|-------------|------------|
| Admin  | admin       | admin123   |
| Seller | rk / kkoc / etrade / cocoblu / retailez / clicktech / ohl | vendor123 |
| IBSC   | ibsc        | ibsc123    |
| NOC    | noc         | noc123     |

## Project Structure

```
eagle_app/
├── app.py                  # Entry point
├── eagle_database.py       # SQLite database layer
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
