"""
Database initialization script with sample data and vector store setup
"""
import os
import json
from app import create_app, db
from app.models import User, JobRole, Course, SkillTaxonomy, JobStabilityData
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)


def create_sample_data():
    """Create sample data for all tables"""
    
    # Skills Taxonomy (same as before)
    skills_data = {
        "programming_languages": [
            "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust",
            "TypeScript", "PHP", "Swift", "Kotlin", "R", "Scala", "Perl"
        ],
        "web_frameworks": [
            "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI", "Node.js",
            "Express.js", "Spring Boot", "ASP.NET", "Ruby on Rails", "Laravel"
        ],
        "databases": [
            "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Cassandra",
            "Oracle", "SQL Server", "DynamoDB", "Firebase", "Elasticsearch"
        ],
        "cloud_platforms": [
            "AWS", "Azure", "Google Cloud", "Heroku", "DigitalOcean", "IBM Cloud"
        ],
        "devops_tools": [
            "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
            "Terraform", "Ansible", "Puppet", "Chef", "Prometheus", "Grafana"
        ],
        "data_science": [
            "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
            "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "NLP",
            "Computer Vision", "Data Visualization", "Statistical Analysis"
        ],
        "soft_skills": [
            "Communication", "Leadership", "Problem Solving", "Teamwork",
            "Critical Thinking", "Time Management", "Adaptability", "Creativity",
            "Emotional Intelligence", "Conflict Resolution", "Presentation Skills"
        ],
        "tools": [
            "Git", "JIRA", "Confluence", "Slack", "VS Code", "IntelliJ IDEA",
            "Postman", "Swagger", "Linux", "Bash", "PowerShell"
        ]
    }
    
    # Job Roles Data (enhanced with better descriptions)
    job_roles_data = [
        {
            "title": "Data Scientist",
            "industry": "Technology",
            "required_skills": ["Python", "Machine Learning", "Deep Learning", "Statistical Analysis", 
                               "Pandas", "NumPy", "TensorFlow", "SQL", "Data Visualization"],
            "preferred_skills": ["NLP", "Computer Vision", "AWS", "Spark", "Docker"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "6-12 LPA"},
                "mid": {"years": "2-5", "salary_range": "12-25 LPA"},
                "senior": {"years": "5+", "salary_range": "25-50 LPA"}
            },
            "description": "Data Scientists analyze complex data using statistical methods and machine learning to extract insights and build predictive models. They work with large datasets, develop algorithms, and communicate findings to stakeholders."
        },
        {
            "title": "Software Engineer",
            "industry": "Technology",
            "required_skills": ["Python", "Java", "JavaScript", "Git", "SQL", "Data Structures",
                               "Algorithms", "Problem Solving", "REST API"],
            "preferred_skills": ["Docker", "Kubernetes", "AWS", "Microservices", "CI/CD"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "5-10 LPA"},
                "mid": {"years": "2-5", "salary_range": "10-20 LPA"},
                "senior": {"years": "5+", "salary_range": "20-40 LPA"}
            },
            "description": "Software Engineers design, develop, test, and maintain software applications. They write clean, efficient code, collaborate with cross-functional teams, and solve complex technical problems."
        },
        {
            "title": "Machine Learning Engineer",
            "industry": "Technology",
            "required_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
                               "MLOps", "Docker", "SQL", "Linux"],
            "preferred_skills": ["Kubernetes", "AWS SageMaker", "Spark", "Computer Vision", "NLP"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "8-15 LPA"},
                "mid": {"years": "2-5", "salary_range": "15-30 LPA"},
                "senior": {"years": "5+", "salary_range": "30-60 LPA"}
            },
            "description": "Machine Learning Engineers build and deploy ML models at scale. They bridge the gap between data science and software engineering, focusing on model optimization, deployment pipelines, and production systems."
        },
        {
            "title": "Full Stack Developer",
            "industry": "Technology",
            "required_skills": ["JavaScript", "React", "Node.js", "HTML", "CSS", "SQL", "Git",
                               "REST API", "MongoDB"],
            "preferred_skills": ["TypeScript", "Docker", "AWS", "GraphQL", "Redis"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "4-8 LPA"},
                "mid": {"years": "2-5", "salary_range": "8-18 LPA"},
                "senior": {"years": "5+", "salary_range": "18-35 LPA"}
            },
            "description": "Full Stack Developers work on both frontend and backend development. They create complete web applications, from user interfaces to server-side logic and databases."
        },
        {
            "title": "DevOps Engineer",
            "industry": "Technology",
            "required_skills": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "Git",
                               "Terraform", "Python", "Bash"],
            "preferred_skills": ["Ansible", "Prometheus", "Grafana", "Azure", "GCP"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "6-12 LPA"},
                "mid": {"years": "2-5", "salary_range": "12-25 LPA"},
                "senior": {"years": "5+", "salary_range": "25-45 LPA"}
            },
            "description": "DevOps Engineers bridge development and operations, implementing CI/CD pipelines, managing infrastructure, and ensuring system reliability and scalability."
        },
        {
            "title": "Data Analyst",
            "industry": "Technology",
            "required_skills": ["SQL", "Excel", "Python", "Data Visualization", "Tableau",
                               "Statistical Analysis", "Power BI"],
            "preferred_skills": ["R", "Machine Learning", "Pandas", "Google Analytics"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "4-8 LPA"},
                "mid": {"years": "2-5", "salary_range": "8-15 LPA"},
                "senior": {"years": "5+", "salary_range": "15-28 LPA"}
            },
            "description": "Data Analysts interpret data to help organizations make informed decisions. They collect, process, and perform statistical analyses on large datasets."
        },
        {
            "title": "Backend Developer",
            "industry": "Technology",
            "required_skills": ["Python", "Java", "SQL", "REST API", "Git", "Linux",
                               "PostgreSQL", "Redis"],
            "preferred_skills": ["Docker", "Kubernetes", "AWS", "GraphQL", "Microservices"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "5-10 LPA"},
                "mid": {"years": "2-5", "salary_range": "10-20 LPA"},
                "senior": {"years": "5+", "salary_range": "20-38 LPA"}
            },
            "description": "Backend Developers focus on server-side logic, databases, and APIs. They build the core functionality that powers web and mobile applications."
        },
        {
            "title": "Frontend Developer",
            "industry": "Technology",
            "required_skills": ["JavaScript", "React", "HTML", "CSS", "Git", "TypeScript",
                               "Responsive Design"],
            "preferred_skills": ["Vue.js", "Angular", "Webpack", "Jest", "Figma"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "4-8 LPA"},
                "mid": {"years": "2-5", "salary_range": "8-16 LPA"},
                "senior": {"years": "5+", "salary_range": "16-32 LPA"}
            },
            "description": "Frontend Developers create user interfaces and user experiences. They implement visual elements that users see and interact with in web applications."
        },
        {
            "title": "Cloud Architect",
            "industry": "Technology",
            "required_skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
                               "Networking", "Security", "Linux"],
            "preferred_skills": ["Serverless", "Multi-cloud", "Cost Optimization", "Compliance"],
            "experience_levels": {
                "entry": {"years": "0-3", "salary_range": "10-18 LPA"},
                "mid": {"years": "3-7", "salary_range": "18-35 LPA"},
                "senior": {"years": "7+", "salary_range": "35-70 LPA"}
            },
            "description": "Cloud Architects design and oversee cloud computing strategies. They create blueprints for cloud infrastructure and ensure systems are scalable, secure, and cost-effective."
        },
        {
            "title": "Cybersecurity Analyst",
            "industry": "Technology",
            "required_skills": ["Network Security", "Linux", "Python", "SIEM", "Vulnerability Assessment",
                               "Incident Response", "Firewalls"],
            "preferred_skills": ["Penetration Testing", "Cloud Security", "CISSP", "CEH"],
            "experience_levels": {
                "entry": {"years": "0-2", "salary_range": "5-10 LPA"},
                "mid": {"years": "2-5", "salary_range": "10-22 LPA"},
                "senior": {"years": "5+", "salary_range": "22-45 LPA"}
            },
            "description": "Cybersecurity Analysts protect systems and networks from cyber threats. They monitor security events, investigate incidents, and implement security measures."
        }
    ]
    
    # Courses Data (same as before)
    courses_data = [
        {
            "name": "Machine Learning Specialization",
            "provider": "Coursera",
            "skills_covered": ["Machine Learning", "Deep Learning", "TensorFlow", "Python"],
            "duration_hours": 80,
            "difficulty": "intermediate",
            "rating": 4.9,
            "url": "https://www.coursera.org/specializations/machine-learning-introduction",
            "price": "Free/Paid",
            "certificate": True
        },
        {
            "name": "Python for Everybody",
            "provider": "Coursera",
            "skills_covered": ["Python", "Programming", "Data Structures"],
            "duration_hours": 60,
            "difficulty": "beginner",
            "rating": 4.8,
            "url": "https://www.coursera.org/specializations/python",
            "price": "Free/Paid",
            "certificate": True
        },
        {
            "name": "Deep Learning Specialization",
            "provider": "Coursera",
            "skills_covered": ["Deep Learning", "Neural Networks", "TensorFlow", "Computer Vision", "NLP"],
            "duration_hours": 120,
            "difficulty": "advanced",
            "rating": 4.9,
            "url": "https://www.coursera.org/specializations/deep-learning",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "AWS Certified Solutions Architect",
            "provider": "AWS",
            "skills_covered": ["AWS", "Cloud Architecture", "EC2", "S3", "VPC"],
            "duration_hours": 40,
            "difficulty": "intermediate",
            "rating": 4.7,
            "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "Docker and Kubernetes: The Complete Guide",
            "provider": "Udemy",
            "skills_covered": ["Docker", "Kubernetes", "DevOps", "CI/CD"],
            "duration_hours": 35,
            "difficulty": "intermediate",
            "rating": 4.7,
            "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "The Complete JavaScript Course",
            "provider": "Udemy",
            "skills_covered": ["JavaScript", "ES6", "Node.js", "Web Development"],
            "duration_hours": 70,
            "difficulty": "beginner",
            "rating": 4.8,
            "url": "https://www.udemy.com/course/the-complete-javascript-course/",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "React - The Complete Guide",
            "provider": "Udemy",
            "skills_covered": ["React", "Redux", "JavaScript", "Frontend"],
            "duration_hours": 65,
            "difficulty": "intermediate",
            "rating": 4.8,
            "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "SQL for Data Science",
            "provider": "Coursera",
            "skills_covered": ["SQL", "Database", "Data Analysis"],
            "duration_hours": 20,
            "difficulty": "beginner",
            "rating": 4.6,
            "url": "https://www.coursera.org/learn/sql-for-data-science",
            "price": "Free/Paid",
            "certificate": True
        },
        {
            "name": "Data Science Professional Certificate",
            "provider": "IBM",
            "skills_covered": ["Python", "Data Science", "Machine Learning", "SQL", "Data Visualization"],
            "duration_hours": 200,
            "difficulty": "intermediate",
            "rating": 4.6,
            "url": "https://www.coursera.org/professional-certificates/ibm-data-science",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "Google Data Analytics Professional Certificate",
            "provider": "Google",
            "skills_covered": ["Data Analysis", "SQL", "Tableau", "R", "Data Visualization"],
            "duration_hours": 180,
            "difficulty": "beginner",
            "rating": 4.8,
            "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "Natural Language Processing Specialization",
            "provider": "Coursera",
            "skills_covered": ["NLP", "Deep Learning", "Python", "TensorFlow"],
            "duration_hours": 100,
            "difficulty": "advanced",
            "rating": 4.6,
            "url": "https://www.coursera.org/specializations/natural-language-processing",
            "price": "Paid",
            "certificate": True
        },
        {
            "name": "Terraform Associate Certification",
            "provider": "HashiCorp",
            "skills_covered": ["Terraform", "IaC", "Cloud", "DevOps"],
            "duration_hours": 30,
            "difficulty": "intermediate",
            "rating": 4.5,
            "url": "https://www.hashicorp.com/certification/terraform-associate",
            "price": "Paid",
            "certificate": True
        }
    ]
    
    # Job Stability Data (same as before)
    job_stability_data = [
        {
            "job_title": "Data Scientist",
            "industry": "Technology",
            "avg_salary_lpa": 15.5,
            "demand_growth_percent": 35.0,
            "automation_risk_percent": 12.0,
            "layoff_rate_percent": 5.2,
            "skill_obsolescence_rate": 15.0,
            "remote_work_possibility": 85,
            "required_skill_level": 4,
            "industry_growth_percent": 22.0,
            "economic_sensitivity": 3,
            "experience_level": "mid"
        },
        {
            "job_title": "Software Engineer",
            "industry": "Technology",
            "avg_salary_lpa": 12.0,
            "demand_growth_percent": 25.0,
            "automation_risk_percent": 15.0,
            "layoff_rate_percent": 6.5,
            "skill_obsolescence_rate": 18.0,
            "remote_work_possibility": 90,
            "required_skill_level": 3,
            "industry_growth_percent": 22.0,
            "economic_sensitivity": 3,
            "experience_level": "mid"
        },
        {
            "job_title": "Machine Learning Engineer",
            "industry": "Technology",
            "avg_salary_lpa": 20.0,
            "demand_growth_percent": 45.0,
            "automation_risk_percent": 8.0,
            "layoff_rate_percent": 4.0,
            "skill_obsolescence_rate": 20.0,
            "remote_work_possibility": 85,
            "required_skill_level": 5,
            "industry_growth_percent": 25.0,
            "economic_sensitivity": 2,
            "experience_level": "mid"
        },
        {
            "job_title": "Full Stack Developer",
            "industry": "Technology",
            "avg_salary_lpa": 10.0,
            "demand_growth_percent": 20.0,
            "automation_risk_percent": 20.0,
            "layoff_rate_percent": 7.0,
            "skill_obsolescence_rate": 22.0,
            "remote_work_possibility": 90,
            "required_skill_level": 3,
            "industry_growth_percent": 18.0,
            "economic_sensitivity": 4,
            "experience_level": "entry"
        },
        {
            "job_title": "DevOps Engineer",
            "industry": "Technology",
            "avg_salary_lpa": 14.0,
            "demand_growth_percent": 30.0,
            "automation_risk_percent": 18.0,
            "layoff_rate_percent": 5.0,
            "skill_obsolescence_rate": 15.0,
            "remote_work_possibility": 88,
            "required_skill_level": 4,
            "industry_growth_percent": 20.0,
            "economic_sensitivity": 3,
            "experience_level": "mid"
        },
        {
            "job_title": "Data Analyst",
            "industry": "Technology",
            "avg_salary_lpa": 8.0,
            "demand_growth_percent": 20.0,
            "automation_risk_percent": 35.0,
            "layoff_rate_percent": 8.0,
            "skill_obsolescence_rate": 12.0,
            "remote_work_possibility": 80,
            "required_skill_level": 2,
            "industry_growth_percent": 15.0,
            "economic_sensitivity": 4,
            "experience_level": "entry"
        },
        {
            "job_title": "Backend Developer",
            "industry": "Technology",
            "avg_salary_lpa": 11.0,
            "demand_growth_percent": 22.0,
            "automation_risk_percent": 18.0,
            "layoff_rate_percent": 6.0,
            "skill_obsolescence_rate": 16.0,
            "remote_work_possibility": 90,
            "required_skill_level": 3,
            "industry_growth_percent": 18.0,
            "economic_sensitivity": 3,
            "experience_level": "mid"
        },
        {
            "job_title": "Frontend Developer",
            "industry": "Technology",
            "avg_salary_lpa": 9.0,
            "demand_growth_percent": 18.0,
            "automation_risk_percent": 25.0,
            "layoff_rate_percent": 7.5,
            "skill_obsolescence_rate": 25.0,
            "remote_work_possibility": 92,
            "required_skill_level": 3,
            "industry_growth_percent": 16.0,
            "economic_sensitivity": 4,
            "experience_level": "entry"
        },
        {
            "job_title": "Cloud Architect",
            "industry": "Technology",
            "avg_salary_lpa": 28.0,
            "demand_growth_percent": 40.0,
            "automation_risk_percent": 10.0,
            "layoff_rate_percent": 3.5,
            "skill_obsolescence_rate": 18.0,
            "remote_work_possibility": 85,
            "required_skill_level": 5,
            "industry_growth_percent": 28.0,
            "economic_sensitivity": 2,
            "experience_level": "senior"
        },
        {
            "job_title": "Cybersecurity Analyst",
            "industry": "Technology",
            "avg_salary_lpa": 12.0,
            "demand_growth_percent": 32.0,
            "automation_risk_percent": 15.0,
            "layoff_rate_percent": 4.5,
            "skill_obsolescence_rate": 20.0,
            "remote_work_possibility": 75,
            "required_skill_level": 4,
            "industry_growth_percent": 25.0,
            "economic_sensitivity": 2,
            "experience_level": "mid"
        }
    ]
    
    return skills_data, job_roles_data, courses_data, job_stability_data


def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Get sample data
        skills_data, job_roles_data, courses_data, job_stability_data = create_sample_data()
        
        # Create admin user
        admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            email='admin@resumeanalyzer.com',
            password=admin_password,
            full_name='System Administrator',
            role='admin'
        )
        db.session.add(admin)
        
        # Create sample student user
        student_password = bcrypt.generate_password_hash('student123').decode('utf-8')
        student = User(
            email='student@test.com',
            password=student_password,
            full_name='Test Student',
            role='student'
        )
        db.session.add(student)
        
        # Add Skills Taxonomy
        for category, skills in skills_data.items():
            for skill in skills:
                skill_entry = SkillTaxonomy(
                    skill_name=skill,
                    category=category,
                    aliases=json.dumps([skill.lower(), skill.upper()])
                )
                db.session.add(skill_entry)
        
        # Add Job Roles
        for job in job_roles_data:
            job_role = JobRole(
                title=job['title'],
                industry=job['industry'],
                required_skills=json.dumps(job['required_skills']),
                preferred_skills=json.dumps(job['preferred_skills']),
                experience_levels=json.dumps(job['experience_levels']),
                description=job['description']
            )
            db.session.add(job_role)
        
        # Add Courses
        for course in courses_data:
            course_entry = Course(
                name=course['name'],
                provider=course['provider'],
                skills_covered=json.dumps(course['skills_covered']),
                duration_hours=course['duration_hours'],
                difficulty=course['difficulty'],
                rating=course['rating'],
                url=course['url'],
                price=course['price'],
                has_certificate=course['certificate']
            )
            db.session.add(course_entry)
        
        # Add Job Stability Data
        for stability in job_stability_data:
            stability_entry = JobStabilityData(
                job_title=stability['job_title'],
                industry=stability['industry'],
                avg_salary_lpa=stability['avg_salary_lpa'],
                demand_growth_percent=stability['demand_growth_percent'],
                automation_risk_percent=stability['automation_risk_percent'],
                layoff_rate_percent=stability['layoff_rate_percent'],
                skill_obsolescence_rate=stability['skill_obsolescence_rate'],
                remote_work_possibility=stability['remote_work_possibility'],
                required_skill_level=stability['required_skill_level'],
                industry_growth_percent=stability['industry_growth_percent'],
                economic_sensitivity=stability['economic_sensitivity'],
                experience_level=stability['experience_level']
            )
            db.session.add(stability_entry)
        
        db.session.commit()
        print("Database initialized successfully!")
        print("Admin login: admin@resumeanalyzer.com / admin123")
        print("Student login: student@test.com / student123")
        
        # Initialize vector store
        print("\nInitializing vector store for RAG...")
        try:
            from app.services.vector_store_initializer import initialize_vector_store
            if initialize_vector_store():
                print("Vector store initialized successfully!")
            else:
                print("Vector store initialization skipped (embeddings not available)")
        except Exception as e:
            print(f"Vector store initialization failed: {e}")
            print("The application will work with fallback skill matching")


if __name__ == '__main__':
    init_database()