#!/usr/bin/env python3
"""
Generate Jobs Summary Report - Create a comprehensive report of collected Upwork data
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import glob

class JobsSummaryReportGenerator:
    """Generate comprehensive summary reports of collected Upwork data"""
    
    def __init__(self):
        self.output_dir = "../output/real_jobs"
        self.reports_dir = "../output/reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
        print("📊 Jobs Summary Report Generator")
        print("=" * 50)
        print("🔍 Analyzing collected Upwork data...")
    
    def find_latest_data_files(self) -> Dict[str, str]:
        """Find the latest jobs and freelancers data files"""
        jobs_pattern = os.path.join(self.output_dir, "upwork_jobs_*.json")
        freelancers_pattern = os.path.join(self.output_dir, "upwork_freelancers_*.json")
        
        jobs_files = glob.glob(jobs_pattern)
        freelancers_files = glob.glob(freelancers_pattern)
        
        latest_jobs = max(jobs_files, key=os.path.getctime) if jobs_files else None
        latest_freelancers = max(freelancers_files, key=os.path.getctime) if freelancers_files else None
        
        return {
            "jobs": latest_jobs,
            "freelancers": latest_freelancers
        }
    
    def load_data(self, filepath: str) -> Dict[str, Any]:
        """Load data from JSON file"""
        if not filepath or not os.path.exists(filepath):
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_jobs_data(self, jobs_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze jobs data and extract insights"""
        if not jobs_data or "jobs" not in jobs_data:
            return {}
        
        jobs = jobs_data["jobs"]
        
        # Basic stats
        total_jobs = len(jobs)
        categories = {}
        budget_ranges = {}
        proposal_counts = {}
        
        for job in jobs:
            # Category analysis
            category = job.get("category", "Unknown")
            categories[category] = categories.get(category, 0) + 1
            
            # Budget analysis
            budget = job.get("budget", "Unknown")
            budget_ranges[budget] = budget_ranges.get(budget, 0) + 1
            
            # Proposals analysis
            proposals = job.get("proposals", "Unknown")
            proposal_counts[proposals] = proposal_counts.get(proposals, 0) + 1
        
        # Skills analysis
        all_skills = []
        for job in jobs:
            skills = job.get("skills", [])
            if isinstance(skills, list):
                all_skills.extend(skills)
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Top skills
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_jobs": total_jobs,
            "categories": categories,
            "budget_ranges": budget_ranges,
            "proposal_counts": proposal_counts,
            "top_skills": top_skills,
            "average_budget": self._calculate_average_budget(jobs),
            "scraped_at": jobs_data.get("scraped_at", "Unknown")
        }
    
    def analyze_freelancers_data(self, freelancers_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze freelancers data and extract insights"""
        if not freelancers_data or "freelancers" not in freelancers_data:
            return {}
        
        freelancers = freelancers_data["freelancers"]
        
        # Basic stats
        total_freelancers = len(freelancers)
        categories = {}
        rate_ranges = {}
        rating_ranges = {}
        locations = {}
        
        for freelancer in freelancers:
            # Category analysis
            category = freelancer.get("category", "Unknown")
            categories[category] = categories.get(category, 0) + 1
            
            # Rate analysis
            rate = freelancer.get("rate", "Unknown")
            rate_ranges[rate] = rate_ranges.get(rate, 0) + 1
            
            # Rating analysis
            rating = freelancer.get("rating", "Unknown")
            rating_ranges[rating] = rating_ranges.get(rating, 0) + 1
            
            # Location analysis
            location = freelancer.get("location", "Unknown")
            locations[location] = locations.get(location, 0) + 1
        
        # Skills analysis
        all_skills = []
        for freelancer in freelancers:
            skills = freelancer.get("skills", [])
            if isinstance(skills, list):
                all_skills.extend(skills)
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Top skills
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_freelancers": total_freelancers,
            "categories": categories,
            "rate_ranges": rate_ranges,
            "rating_ranges": rating_ranges,
            "locations": locations,
            "top_skills": top_skills,
            "average_rate": self._calculate_average_rate(freelancers),
            "scraped_at": freelancers_data.get("scraped_at", "Unknown")
        }
    
    def _calculate_average_budget(self, jobs: List[Dict[str, Any]]) -> str:
        """Calculate average budget from job listings"""
        budgets = []
        for job in jobs:
            budget = job.get("budget", "")
            if "$" in budget:
                # Extract numbers from budget strings like "$2,000 - $3,000"
                import re
                numbers = re.findall(r'\$[\d,]+', budget)
                if numbers:
                    # Take the first number as a rough estimate
                    num_str = numbers[0].replace('$', '').replace(',', '')
                    try:
                        budgets.append(int(num_str))
                    except ValueError:
                        continue
        
        if budgets:
            avg = sum(budgets) / len(budgets)
            return f"${avg:,.0f}"
        return "Unknown"
    
    def _calculate_average_rate(self, freelancers: List[Dict[str, Any]]) -> str:
        """Calculate average hourly rate from freelancer listings"""
        rates = []
        for freelancer in freelancers:
            rate = freelancer.get("rate", "")
            if "$" in rate and "/hr" in rate:
                # Extract numbers from rate strings like "$45/hr"
                import re
                numbers = re.findall(r'\$[\d.]+', rate)
                if numbers:
                    num_str = numbers[0].replace('$', '')
                    try:
                        rates.append(float(num_str))
                    except ValueError:
                        continue
        
        if rates:
            avg = sum(rates) / len(rates)
            return f"${avg:.1f}/hr"
        return "Unknown"
    
    def generate_html_report(self, jobs_analysis: Dict[str, Any], freelancers_analysis: Dict[str, Any]):
        """Generate an HTML report with the analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"upwork_jobs_summary_report_{timestamp}.html"
        filepath = os.path.join(self.reports_dir, filename)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upwork Jobs & Freelancers Summary Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #007bff;
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            color: #666;
            margin: 10px 0 0 0;
            font-size: 1.1em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 1.2em;
        }}
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .data-table th, .data-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .data-table th {{
            background-color: #007bff;
            color: white;
        }}
        .data-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .skill-tag {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            margin: 2px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Upwork Jobs & Freelancers Summary Report</h1>
            <p>Comprehensive analysis of collected Upwork data</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>📋 Total Jobs</h3>
                <div class="number">{jobs_analysis.get('total_jobs', 0)}</div>
                <p>Job listings collected</p>
            </div>
            <div class="stat-card">
                <h3>👤 Total Freelancers</h3>
                <div class="number">{freelancers_analysis.get('total_freelancers', 0)}</div>
                <p>Freelancer profiles collected</p>
            </div>
            <div class="stat-card">
                <h3>💰 Avg Job Budget</h3>
                <div class="number">{jobs_analysis.get('average_budget', 'Unknown')}</div>
                <p>Average project budget</p>
            </div>
            <div class="stat-card">
                <h3>💵 Avg Hourly Rate</h3>
                <div class="number">{freelancers_analysis.get('average_rate', 'Unknown')}</div>
                <p>Average freelancer rate</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Jobs Analysis</h2>
            <h3>Job Categories</h3>
            <table class="data-table">
                <tr><th>Category</th><th>Count</th></tr>
                {''.join([f'<tr><td>{cat}</td><td>{count}</td></tr>' for cat, count in jobs_analysis.get('categories', {}).items()])}
            </table>
            
            <h3>Budget Ranges</h3>
            <table class="data-table">
                <tr><th>Budget Range</th><th>Count</th></tr>
                {''.join([f'<tr><td>{budget}</td><td>{count}</td></tr>' for budget, count in jobs_analysis.get('budget_ranges', {}).items()])}
            </table>
            
            <h3>Top Required Skills</h3>
            <div>
                {''.join([f'<span class="skill-tag">{skill} ({count})</span>' for skill, count in jobs_analysis.get('top_skills', [])])}
            </div>
        </div>
        
        <div class="section">
            <h2>👥 Freelancers Analysis</h2>
            <h3>Freelancer Categories</h3>
            <table class="data-table">
                <tr><th>Category</th><th>Count</th></tr>
                {''.join([f'<tr><td>{cat}</td><td>{count}</td></tr>' for cat, count in freelancers_analysis.get('categories', {}).items()])}
            </table>
            
            <h3>Hourly Rate Ranges</h3>
            <table class="data-table">
                <tr><th>Rate Range</th><th>Count</th></tr>
                {''.join([f'<tr><td>{rate}</td><td>{count}</td></tr>' for rate, count in freelancers_analysis.get('rate_ranges', {}).items()])}
            </table>
            
            <h3>Top Freelancer Skills</h3>
            <div>
                {''.join([f'<span class="skill-tag">{skill} ({count})</span>' for skill, count in freelancers_analysis.get('top_skills', [])])}
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Data Source:</strong> Upwork Public Search Results</p>
            <p><strong>Collection Method:</strong> Real MCP Browser Automation</p>
            <p><strong>Report Version:</strong> 1.0 | <strong>Generated:</strong> {datetime.now().isoformat()}</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 Generated HTML report: {filepath}")
        return filepath
    
    def generate_markdown_report(self, jobs_analysis: Dict[str, Any], freelancers_analysis: Dict[str, Any]):
        """Generate a Markdown report with the analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"upwork_jobs_summary_report_{timestamp}.md"
        filepath = os.path.join(self.reports_dir, filename)
        
        markdown_content = f"""# 🚀 Upwork Jobs & Freelancers Summary Report

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}  
**Data Source:** Upwork Public Search Results  
**Collection Method:** Real MCP Browser Automation  
**Report Version:** 1.0

---

## 📊 Executive Summary

- **Total Jobs Collected:** {jobs_analysis.get('total_jobs', 0)}
- **Total Freelancers Collected:** {freelancers_analysis.get('total_freelancers', 0)}
- **Average Job Budget:** {jobs_analysis.get('average_budget', 'Unknown')}
- **Average Hourly Rate:** {freelancers_analysis.get('average_rate', 'Unknown')}

---

## 📋 Jobs Analysis

### Job Categories
| Category | Count |
|----------|-------|
{chr(10).join([f"| {cat} | {count} |" for cat, count in jobs_analysis.get('categories', {}).items()])}

### Budget Ranges
| Budget Range | Count |
|--------------|-------|
{chr(10).join([f"| {budget} | {count} |" for budget, count in jobs_analysis.get('budget_ranges', {}).items()])}

### Top Required Skills
{chr(10).join([f"- **{skill}** ({count} jobs)" for skill, count in jobs_analysis.get('top_skills', [])])}

---

## 👥 Freelancers Analysis

### Freelancer Categories
| Category | Count |
|----------|-------|
{chr(10).join([f"| {cat} | {count} |" for cat, count in freelancers_analysis.get('categories', {}).items()])}

### Hourly Rate Ranges
| Rate Range | Count |
|------------|-------|
{chr(10).join([f"| {rate} | {count} |" for rate, count in freelancers_analysis.get('rate_ranges', {}).items()])}

### Top Freelancer Skills
{chr(10).join([f"- **{skill}** ({count} freelancers)" for skill, count in freelancers_analysis.get('top_skills', [])])}

---

## 🎯 Key Insights

### Market Trends
1. **Most Popular Job Categories:** {', '.join(list(jobs_analysis.get('categories', {}).keys())[:3])}
2. **Most In-Demand Skills:** {', '.join([skill for skill, _ in jobs_analysis.get('top_skills', [])[:5]])}
3. **Average Project Budget:** {jobs_analysis.get('average_budget', 'Unknown')}
4. **Average Freelancer Rate:** {freelancers_analysis.get('average_rate', 'Unknown')}

### Recommendations
- **For Clients:** Consider the average budget range when posting projects
- **For Freelancers:** Focus on the most in-demand skills to increase marketability
- **For Recruiters:** Target freelancers with high ratings and relevant skill sets

---

## 📈 Data Quality

- **Jobs Data Scraped:** {jobs_analysis.get('scraped_at', 'Unknown')}
- **Freelancers Data Scraped:** {freelancers_analysis.get('scraped_at', 'Unknown')}
- **MCP Calls Used:** Browser navigation and JavaScript evaluation
- **Anti-Detection:** Stealth browser measures enabled

---

*Report generated automatically using Real MCP Browser Automation*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"💾 Generated Markdown report: {filepath}")
        return filepath
    
    def run(self):
        """Main report generation workflow"""
        print("🔍 Finding latest data files...")
        
        # Find latest data files
        data_files = self.find_latest_data_files()
        
        if not data_files["jobs"] and not data_files["freelancers"]:
            print("❌ No data files found!")
            return
        
        # Load data
        jobs_data = self.load_data(data_files["jobs"])
        freelancers_data = self.load_data(data_files["freelancers"])
        
        print(f"📊 Loaded {len(jobs_data.get('jobs', []))} jobs and {len(freelancers_data.get('freelancers', []))} freelancers")
        
        # Analyze data
        print("📈 Analyzing data...")
        jobs_analysis = self.analyze_jobs_data(jobs_data)
        freelancers_analysis = self.analyze_freelancers_data(freelancers_data)
        
        # Generate reports
        print("📝 Generating reports...")
        html_report = self.generate_html_report(jobs_analysis, freelancers_analysis)
        markdown_report = self.generate_markdown_report(jobs_analysis, freelancers_analysis)
        
        # Summary
        print(f"\n🎉 Reports Generated Successfully!")
        print(f"📊 Jobs Analysis: {jobs_analysis.get('total_jobs', 0)} jobs analyzed")
        print(f"👥 Freelancers Analysis: {freelancers_analysis.get('total_freelancers', 0)} freelancers analyzed")
        print(f"📁 HTML Report: {html_report}")
        print(f"📁 Markdown Report: {markdown_report}")

def main():
    """Main function"""
    generator = JobsSummaryReportGenerator()
    generator.run()

if __name__ == "__main__":
    main() 