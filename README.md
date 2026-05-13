# 🚀 CAREER-GPS — AI Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Replit](https://img.shields.io/badge/Deployed%20on-Replit-orange.svg)](https://replit.com)

---

## 🌐 Live Demo

🔗 https://career-gps--graceelizabeth6.replit.app

Analyze resumes instantly using the live deployed application.

---

## 📌 About The Project

CAREER-GPS is an AI-powered resume analyzer designed to help students and professionals identify their skills, match with suitable job roles, and receive personalized career recommendations.

The platform uses NLP and AI techniques to extract skills from resumes and provide:
- Job role matching
- Skill gap analysis
- Course recommendations
- Salary insights
- Career growth trends

---

## ✨ Features

- 📄 Resume upload and parsing (PDF, DOCX, TXT)
- 🧠 AI-powered skill extraction using NLP
- 🎯 Smart job role matching
- 📚 Personalized course recommendations
- 📊 Salary insights and market trends
- 🔐 Secure authentication system
- 👨‍🎓 Student and Admin dashboards
- ⚡ Fast and lightweight Flask backend

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Flask, Python |
| Database | SQLite, SQLAlchemy |
| AI/NLP | Gemini API, spaCy |
| Machine Learning | scikit-learn, pandas, numpy |
| PDF Processing | pdfplumber, PyPDF2 |
| OCR | Tesseract |
| Authentication | JWT, bcrypt |
| Deployment | Replit |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Grace1903/CAREER-GPS.git
cd CAREER-GPS
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 5️⃣ Initialize Database

```bash
python init_db.py
```

### 6️⃣ Run Application

```bash
python run.py
```

### 7️⃣ Open Browser

```text
http://127.0.0.1:5000
```

---

## 🔐 Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@resumeanalyzer.com | admin123 |
| Student | student@test.com | student123 |

You can also create a new account using the Register option.

---

## 📁 Project Structure

```text
CAREER-GPS/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── student.py
│   │   └── admin.py
│   ├── services/
│   │   ├── pdf_extractor.py
│   │   ├── skill_extractor.py
│   │   └── skill_matcher.py
│   └── templates/
│
├── uploads/
├── vector_store/
├── run.py
├── init_db.py
├── model.pkl
├── requirements.txt
└── README.md
```

---

## 🔄 Workflow

```text
Upload Resume
        ↓
AI Skill Extraction
        ↓
Job Role Matching
        ↓
Course Recommendations
        ↓
Career Insights & Salary Trends
```

---

## 📊 Supported Job Roles

| Job Role | Entry Salary | Senior Salary | Demand Growth |
|----------|--------------|---------------|---------------|
| Data Scientist | 6–12 LPA | 25–50 LPA | 35% |
| Software Engineer | 5–10 LPA | 20–40 LPA | 25% |
| ML Engineer | 8–15 LPA | 30–60 LPA | 45% |
| Full Stack Developer | 4–8 LPA | 18–35 LPA | 20% |
| DevOps Engineer | 6–12 LPA | 25–45 LPA | 30% |
| Data Analyst | 4–8 LPA | 15–28 LPA | 20% |
| Cloud Architect | 10–18 LPA | 35–70 LPA | 40% |
| Cybersecurity Analyst | 5–10 LPA | 22–45 LPA | 32% |

---

## 📌 Example Output

### Extracted Skills

- Python
- SQL
- Machine Learning
- NLP
- Flask
- Git

### Top Job Matches

| Role | Match Percentage | Missing Skills |
|------|------------------|----------------|
| Data Scientist | 85% | TensorFlow, AWS |
| ML Engineer | 78% | Docker, Kubernetes |
| Software Engineer | 72% | Java, React |

### Recommended Courses

1. Machine Learning Specialization — Coursera
2. Deep Learning Specialization — Coursera
3. AWS Solutions Architect — AWS

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | Run `pip install -r requirements.txt` |
| Database error | Run `python init_db.py` |
| Port already in use | Change port in `run.py` |
| PDF extraction issue | Use text-based PDFs |

---

## 🚀 Deployment

This project is deployed on Replit.

🔗 Live URL:  
https://career-gps--graceelizabeth6.replit.app

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Push to GitHub  
5. Open a Pull Request  

---

## 👩‍💻 Author

Grace Elizabeth Jose

- GitHub: https://github.com/Grace1903
- Project Repository: https://github.com/Grace1903/CAREER-GPS
- Live Demo: https://career-gps--graceelizabeth6.replit.app

---

## 🙏 Acknowledgments

- Google Gemini AI
- spaCy NLP Library
- Flask Community
- Replit Hosting Platform

---

## ⭐ Show Your Support

If you found this project useful:
- ⭐ Star the repository
- 🍴 Fork the project
- 📢 Share the live demo

---

## 📜 Note

This project was developed for learning, career guidance, and resume analysis purposes.

---

Made with ❤️ by Grace Elizabeth Jose
