# 🚀 CAREER-GPS — AI Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-green)
![ML](https://img.shields.io/badge/NLP-AI%20Powered-orange)

---

## 📌 About the Project

CAREER-GPS is an AI-powered resume analyzer that extracts skills from resumes, matches them with suitable job roles, and provides personalized career recommendations including courses, salary insights, and job market trends.

---

## ✨ Features

- Resume upload and parsing (PDF, DOCX, TXT)
- AI-based skill extraction using NLP
- Smart job role matching system
- Personalized learning recommendations
- Salary and demand insights
- Secure login system (Student & Admin)

---

## 🛠️ Tech Stack

Flask, Python, SQLite, SQLAlchemy, spaCy, scikit-learn, pandas, numpy, pdfplumber, JWT, bcrypt

---

## ⚙️ Installation & Setup

git clone https://github.com/Grace1903/CAREER-GPS.git  
cd CAREER-GPS  

python -m venv venv  

venv\Scripts\activate   (Windows)  
source venv/bin/activate   (Mac/Linux)  

pip install -r requirements.txt  
python -m spacy download en_core_web_sm  

python init_db.py  
python run.py  

Open browser: http://127.0.0.1:5000  

---

## 🔐 Login Credentials

Admin  
Email: admin@resumeanalyzer.com  
Password: admin123  

Student  
Email: student@test.com  
Password: student123  

---

## 📁 Project Structure

CAREER-GPS/  
├── app/  
│   ├── routes/  
│   ├── services/  
│   ├── models.py  
│   └── templates/  
├── uploads/  
├── vector_store/  
├── run.py  
├── init_db.py  
├── model.pkl  
├── requirements.txt  
└── README.md  

---

## 🔄 Workflow

Upload Resume → Extract Skills → Match Job Roles → Get Recommendations → View Career Insights  

---

## 📊 Supported Job Roles

Data Scientist, Software Engineer, ML Engineer, Full Stack Developer, DevOps Engineer, Data Analyst, Cloud Architect, Cybersecurity Analyst  

---

## ⚠️ Common Issues

- Module not found → install requirements  
- DB error → run init_db.py  
- Port issue → change port in run.py  
- PDF not reading → use text-based PDF  

---

## 🤝 Contribution

Fork repo → create branch → commit changes → push → pull request  

---

## 👩‍💻 Author

Grace Elizabeth Jose  
GitHub: https://github.com/Grace1903  

---
