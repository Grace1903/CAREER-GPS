# 🚀 CAREER-GPS — AI Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-purple.svg)](https://render.com)

---

## 🌐 Live Demo

🔗(https://career-gps-yd3f.onrender.com)

Upload your resume and get instant AI-powered career guidance.

---

## 📌 About The Project

CAREER-GPS is an AI-powered resume analyzer designed to help students and professionals identify their skills, match with suitable job roles, and receive personalized career recommendations.

The platform uses NLP and Generative AI to extract skills from resumes and provide actionable career insights including job role matching, skill gap analysis, course recommendations, and salary trends.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Parsing** | Upload PDF, DOCX, or TXT resumes for instant analysis |
| 🧠 **AI Skill Extraction** | NLP-powered extraction of skills from resume text |
| 🎯 **Job Role Matching** | Smart matching against 8+ in-demand tech roles |
| 📚 **Course Recommendations** | Personalized learning path based on skill gaps |
| 📊 **Salary Insights** | Entry to senior salary ranges and market demand |
| 🔐 **Authentication** | Secure login with JWT and bcrypt |
| 👨‍🎓 **Student Dashboard** | Personalized career analysis view |
| ⚙️ **Admin Dashboard** | Manage users and view analytics |

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| Backend | Flask, Python 3.11 |
| Database | SQLite, SQLAlchemy |
| AI/NLP | Gemini API, spaCy |
| Machine Learning | scikit-learn, pandas, numpy |
| PDF Processing | pdfplumber, PyPDF2 |
| OCR | Tesseract |
| Authentication | JWT, bcrypt |
| Deployment | Render |

---

## 🔄 How It Works

```
Upload Resume (PDF/DOCX/TXT)
        ↓
Text Extraction (pdfplumber + OCR)
        ↓
AI Skill Extraction (spaCy + Gemini)
        ↓
Job Role Matching (scikit-learn)
        ↓
Course & Career Recommendations
        ↓
Salary Insights & Growth Trends
```

---

## 📊 Supported Job Roles

| Job Role | Entry Salary | Senior Salary | Demand Growth |
|----------|-------------|---------------|---------------|
| Data Scientist | 6–12 LPA | 25–50 LPA | 35% |
| Software Engineer | 5–10 LPA | 20–40 LPA | 25% |
| ML Engineer | 8–15 LPA | 30–60 LPA | 45% |
| Full Stack Developer | 4–8 LPA | 18–35 LPA | 20% |
| DevOps Engineer | 6–12 LPA | 25–45 LPA | 30% |
| Data Analyst | 4–8 LPA | 15–28 LPA | 20% |
| Cloud Architect | 10–18 LPA | 35–70 LPA | 40% |
| Cybersecurity Analyst | 5–10 LPA | 22–45 LPA | 32% |

---

## ⚙️ Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/Grace1903/CAREER-GPS.git
cd CAREER-GPS

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Initialize database
python init_db.py

# Run app
python run.py
```

Open `http://127.0.0.1:5000`

---

## 🔐 Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@resumeanalyzer.com | admin123 |
| Student | student@test.com | student123 |

You can also register a new account.

---

## 📁 Project Structure

```
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
├── run.py
├── init_db.py
├── model.pkl
├── requirements.txt
└── README.md
```

---

## 📌 Example Output

**Extracted Skills:** Python, SQL, Machine Learning, NLP, Flask, Git

**Top Job Matches:**

| Role | Match % | Missing Skills |
|------|---------|----------------|
| Data Scientist | 85% | TensorFlow, AWS |
| ML Engineer | 78% | Docker, Kubernetes |
| Software Engineer | 72% | Java, React |

**Recommended Courses:**
- Machine Learning Specialization — Coursera
- Deep Learning Specialization — Coursera
- AWS Solutions Architect — AWS

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | Run `pip install -r requirements.txt` |
| Database error | Run `python init_db.py` |
| Port in use | Change port in `run.py` |
| PDF extraction issue | Use text-based PDFs |

---

## 👩‍💻 Author

**Grace Elizabeth Jose**

- GitHub: [Grace1903](https://github.com/Grace1903)
- Live Demo: [career-gps-yd3f.onrender.com](https://career-gps-yd3f.onrender.com)

---

## 🙏 Acknowledgments

- Google Gemini AI
- spaCy NLP Library
- Flask Community
- Render Hosting Platform

---

> Built to help every student find their right career path using AI.
