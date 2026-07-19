# CRUD Web Application

A clean, modular CRUD (Create, Read, Update, Delete) web application built using Flask and Firebase Firestore.

## Features

- User Authentication (Custom Registration, Login, settings password changes, and Recovery Security Questions)
- Student Details CRUD (Add, View, Update, Delete)
- Firebase Firestore Database Backend
- Modular & Deployment-Ready Code Architecture

## Technologies Used

- Python (Flask, Firebase Admin SDK)
- Firebase Firestore
- HTML
- CSS
- JavaScript

## Project Structure

```plaintext
CRUD-web-application/
├── app.py                            # Flask server (routes and controllers only)
├── db_service.py                     # Database abstraction services (CRUD operations)
├── firebase_config.py                # Firebase Admin SDK initialization helper
├── requirement.txt                   # Project dependencies (Flask & firebase-admin)
├── firebase-service-account.json.example  # Template for Firebase credentials JSON
├── static/                           # Client static files (UI - Unchanged)
│   ├── app.js
│   ├── style.css
│   └── srec.jpg
└── templates/                        # Client HTML views (UI - Unchanged)
    └── index.html
```

## Setup & Running the Project

### 1. Clone the Repository

```bash
git clone <your-github-repository-link>
cd CRUD-web-application
```

### 2. Install Dependencies

```bash
pip install -r requirement.txt
```

### 3. Firebase Configuration

#### A. Local Development
1. Go to your [Firebase Console](https://console.firebase.google.com/).
2. Create/select a project (e.g. `smart-caching-system-86cc2`).
3. Click the gear icon next to Project Overview -> **Project Settings**.
4. Go to the **Service accounts** tab.
5. Click **Generate new private key** to download your credentials JSON.
6. Save the downloaded file as `firebase-service-account.json` in the root folder of this project.

#### B. Production Deployment (e.g., Render, Heroku)
To keep your credentials secure:
1. Add an Environment Variable named `FIREBASE_CREDENTIALS_JSON`.
2. Copy the entire raw JSON text content of your downloaded service account key file and paste it as the value of the environment variable.

### 4. Run the Flask Application

```bash
python app.py
```

### 5. Open in Browser

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Deployment Guide

### Deploying to Vercel (Recommended - Faster & Free)
1. Install Vercel CLI locally or connect your project on [Vercel Dashboard](https://vercel.com).
2. Connect your GitHub repository to Vercel.
3. Vercel will automatically detect `vercel.json` and configure the Python serverless environment.
4. **Environment Variables**: In your Vercel project settings, add an environment variable:
   - **Key**: `FIREBASE_CREDENTIALS_JSON`
   - **Value**: Copy/paste the entire content of your downloaded private key JSON file from Firebase.
5. Deploy!

### Deploying to Render
1. Go to [Render](https://render.com) and create a **New Web Service**.
2. Connect your GitHub repository.
3. Configure the following service settings:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. **Environment Variables**: Under the "Environment" tab, click **Add Environment Variable**:
   - **Key**: `FIREBASE_CREDENTIALS_JSON`
   - **Value**: Copy/paste the entire content of your Firebase service account private key JSON file.
5. Click **Create Web Service**.


## Author

AKHILESH CHAKALI
Reg No: 23X51A0503
Email: [23x51a0503@srecnandyal.edu.in](mailto:23x51a0503@srecnandyal.edu.in)

