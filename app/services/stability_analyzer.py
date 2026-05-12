import numpy as np
from app.models import JobStabilityData
import pickle


class StabilityAnalyzer:
    def __init__(self):
        with open('model.pkl', 'rb') as file:
            self.model = pickle.load(file)
        self.weights = {
            'demand_growth': 0.20,
            'automation_risk': -0.15,  # Negative impact
            'layoff_rate': -0.15,      # Negative impact
            'skill_obsolescence': -0.10,  # Negative impact
            'remote_work': 0.10,
            'skill_level': 0.10,
            'industry_growth': 0.15,
            'economic_sensitivity': -0.05  # Negative impact
        }

    def analyze(self, job_title):
    
        stability_data = self._get_stability_data(job_title)
        
        if not stability_data:
            return self._generate_default_analysis(job_title)
        
        stability_score = self._calculate_stability_score(stability_data)
        
        risk_classification = self._classify_risk(stability_score)
        
        detailed_analysis = self._generate_detailed_analysis(stability_data, stability_score)
        
        return {
            'job_title': job_title,
            'stability_score': round(stability_score, 1),
            'risk_classification': risk_classification,
            'metrics': {
                'demand_growth': stability_data.demand_growth_percent,
                'automation_risk': stability_data.automation_risk_percent,
                'layoff_rate': stability_data.layoff_rate_percent,
                'skill_obsolescence_rate': stability_data.skill_obsolescence_rate,
                'remote_work_possibility': stability_data.remote_work_possibility,
                'required_skill_level': stability_data.required_skill_level,
                'industry_growth': stability_data.industry_growth_percent,
                'economic_sensitivity': stability_data.economic_sensitivity,
                'avg_salary_lpa': stability_data.avg_salary_lpa
            },
            'analysis': detailed_analysis,
            'recommendations': self._generate_recommendations(stability_data, risk_classification)
        }
    
    def _get_stability_data(self, job_title):
        try:
            from flask import current_app
            with current_app.app_context():
                return JobStabilityData.query.filter_by(job_title=job_title).first()
        except Exception as e:
            print(f"Error fetching stability data: {e}")
            return None
    
    def _calculate_stability_score(self, data):
        try:

            p=self.model.predict([data.demand_growth_percent,data.automation_risk_percent,data.remote_work_possibility,data.skill_obsolescence_rate,data.required_skill_level,data.industry_growth_percent,data.economic_sensitivity])
            score=100-p
        except:
            normalized = {
                'demand_growth': min(data.demand_growth_percent / 50, 1),  # 50% is max
                'automation_risk': data.automation_risk_percent / 100,
                'layoff_rate': min(data.layoff_rate_percent / 20, 1),  # 20% is max
                'skill_obsolescence': min(data.skill_obsolescence_rate / 30, 1),  # 30% is max
                'remote_work': data.remote_work_possibility / 100,
                'skill_level': data.required_skill_level / 5,  # 1-5 scale
                'industry_growth': min(data.industry_growth_percent / 30, 1),  # 30% is max
                'economic_sensitivity': data.economic_sensitivity / 5  # 1-5 scale
            }
            
            score = 50  # Base score
            
            score += normalized['demand_growth'] * self.weights['demand_growth'] * 100
            score += normalized['automation_risk'] * self.weights['automation_risk'] * 100
            score += normalized['layoff_rate'] * self.weights['layoff_rate'] * 100
            score += normalized['skill_obsolescence'] * self.weights['skill_obsolescence'] * 100
            score += normalized['remote_work'] * self.weights['remote_work'] * 100
            score += normalized['skill_level'] * self.weights['skill_level'] * 100
            score += normalized['industry_growth'] * self.weights['industry_growth'] * 100
            score += normalized['economic_sensitivity'] * self.weights['economic_sensitivity'] * 100
        
        return max(0, min(100, score))
    
    def _classify_risk(self, score):
        if score >= 75:
            return 'Low Risk'
        elif score >= 60:
            return 'Moderate Risk'
        elif score >= 40:
            return 'Medium Risk'
        elif score >= 25:
            return 'High Risk'
        else:
            return 'Very High Risk'
    
    def _generate_detailed_analysis(self, data, score):
        analysis = {
            'summary': '',
            'strengths': [],
            'concerns': [],
            'market_outlook': ''
        }
        
        if score >= 70:
            analysis['summary'] = f"{data.job_title} shows strong stability indicators with positive growth trends."
        elif score >= 50:
            analysis['summary'] = f"{data.job_title} has moderate stability with some areas requiring attention."
        else:
            analysis['summary'] = f"{data.job_title} shows concerning stability metrics that warrant careful consideration."
        
        if data.demand_growth_percent > 20:
            analysis['strengths'].append(f"High demand growth ({data.demand_growth_percent}%)")
        if data.automation_risk_percent < 20:
            analysis['strengths'].append(f"Low automation risk ({data.automation_risk_percent}%)")
        if data.remote_work_possibility > 70:
            analysis['strengths'].append(f"High remote work potential ({data.remote_work_possibility}%)")
        if data.industry_growth_percent > 15:
            analysis['strengths'].append(f"Growing industry ({data.industry_growth_percent}% growth)")
        if data.avg_salary_lpa > 15:
            analysis['strengths'].append(f"Competitive salary (₹{data.avg_salary_lpa} LPA)")
        
        if data.automation_risk_percent > 30:
            analysis['concerns'].append(f"Significant automation risk ({data.automation_risk_percent}%)")
        if data.layoff_rate_percent > 7:
            analysis['concerns'].append(f"Higher than average layoff rate ({data.layoff_rate_percent}%)")
        if data.skill_obsolescence_rate > 20:
            analysis['concerns'].append(f"Skills may become outdated quickly ({data.skill_obsolescence_rate}%)")
        if data.economic_sensitivity > 3:
            analysis['concerns'].append("Sensitive to economic downturns")
        
        if data.demand_growth_percent > 25 and data.industry_growth_percent > 15:
            analysis['market_outlook'] = "Positive long-term outlook with strong demand"
        elif data.demand_growth_percent > 10:
            analysis['market_outlook'] = "Stable outlook with moderate growth expected"
        else:
            analysis['market_outlook'] = "Uncertain outlook - consider diversifying skills"
        
        return analysis
    
    def _generate_recommendations(self, data, risk_classification):
        recommendations = []
        
        if data.skill_obsolescence_rate > 15:
            recommendations.append("Continuously update skills to stay relevant")
            recommendations.append("Follow industry trends and emerging technologies")
        
        if data.automation_risk_percent > 25:
            recommendations.append("Focus on skills that are harder to automate")
            recommendations.append("Develop leadership and strategic thinking abilities")
        
        if data.economic_sensitivity > 3:
            recommendations.append("Build emergency fund for potential downturns")
            recommendations.append("Consider roles in more stable industries")
        
        if risk_classification in ['High Risk', 'Very High Risk']:
            recommendations.append("Consider transitioning to more stable roles")
            recommendations.append("Develop transferable skills")
        
        if data.required_skill_level >= 4:
            recommendations.append("Pursue advanced certifications")
            recommendations.append("Consider specialization in niche areas")
        
        if not recommendations:
            recommendations = [
                "Continue professional development",
                "Build a strong professional network",
                "Keep skills up to date with market demands"
            ]
        
        return recommendations
    
    def _generate_default_analysis(self, job_title):
        return {
            'job_title': job_title,
            'stability_score': 50.0,
            'risk_classification': 'Unknown',
            'metrics': {
                'demand_growth': 'N/A',
                'automation_risk': 'N/A',
                'layoff_rate': 'N/A',
                'skill_obsolescence_rate': 'N/A',
                'remote_work_possibility': 'N/A',
                'required_skill_level': 'N/A',
                'industry_growth': 'N/A',
                'economic_sensitivity': 'N/A',
                'avg_salary_lpa': 'N/A'
            },
            'analysis': {
                'summary': f'Stability data for {job_title} is not available in our database.',
                'strengths': [],
                'concerns': ['Limited data available for analysis'],
                'market_outlook': 'Unable to determine without data'
            },
            'recommendations': [
                'Research current market trends for this role',
                'Connect with professionals in this field',
                'Monitor job postings and industry news'
            ]
        }