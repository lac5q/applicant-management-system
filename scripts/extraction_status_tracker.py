#!/usr/bin/env python3
"""
Candidate Extraction Status Tracker
Tracks the progress of extracting candidates from Upwork screenshots
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ExtractionStatusTracker:
    def __init__(self):
        self.status_file = "output/extraction_status.json"
        self.current_data_file = "output/processed_candidates/all_processed_candidates_20250719_031346.json"
        
    def load_current_status(self) -> Dict[str, Any]:
        """Load current extraction status"""
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as f:
                return json.load(f)
        else:
            return self.initialize_status()
    
    def initialize_status(self) -> Dict[str, Any]:
        """Initialize new extraction status"""
        status = {
            "extraction_summary": {
                "total_screenshots_processed": 0,
                "total_candidates_expected": 60,
                "total_candidates_extracted": 0,
                "total_candidates_saved": 0,
                "total_candidates_rated": 0,
                "extraction_completion_percentage": 0.0,
                "last_updated": datetime.now().isoformat()
            },
            "screenshot_details": [],
            "job_postings": {
                "URGENT: Contract-to-hire Shopify Developer + UX Specialist - Start This Week!": {
                    "expected_candidates": 30,
                    "extracted_candidates": 0,
                    "saved_candidates": 0,
                    "rated_candidates": 0
                },
                "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week": {
                    "expected_candidates": 30,
                    "extracted_candidates": 0,
                    "saved_candidates": 0,
                    "rated_candidates": 0
                }
            },
            "processing_stages": {
                "screenshot_analysis": "pending",
                "candidate_extraction": "in_progress",
                "data_validation": "completed",
                "database_save": "completed",
                "rating_processing": "pending",
                "profile_lookup": "pending"
            }
        }
        return status
    
    def update_from_current_data(self) -> Dict[str, Any]:
        """Update status based on current data files"""
        status = self.load_current_status()
        
        # Count current candidates
        if os.path.exists(self.current_data_file):
            with open(self.current_data_file, 'r') as f:
                data = json.load(f)
                current_candidates = data.get('applicants', [])
                
                status["extraction_summary"]["total_candidates_saved"] = len(current_candidates)
                status["extraction_summary"]["total_candidates_extracted"] = len(current_candidates)
                
                # Count by job posting
                for candidate in current_candidates:
                    job_title = candidate.get('job_title', '')
                    if job_title in status["job_postings"]:
                        status["job_postings"][job_title]["saved_candidates"] += 1
                        status["job_postings"][job_title]["extracted_candidates"] += 1
                
                # Count rated candidates
                rated_count = sum(1 for c in current_candidates if isinstance(c.get('rating'), (int, float)) and c.get('rating', 0) > 0)
                status["extraction_summary"]["total_candidates_rated"] = rated_count
                
                # Update completion percentage
                expected = status["extraction_summary"]["total_candidates_expected"]
                saved = status["extraction_summary"]["total_candidates_saved"]
                status["extraction_summary"]["extraction_completion_percentage"] = (saved / expected) * 100 if expected > 0 else 0
                
                # Update processing stages
                if saved > 0:
                    status["processing_stages"]["candidate_extraction"] = "completed"
                    status["processing_stages"]["database_save"] = "completed"
                    if rated_count > 0:
                        status["processing_stages"]["rating_processing"] = "in_progress"
        
        status["extraction_summary"]["last_updated"] = datetime.now().isoformat()
        return status
    
    def save_status(self, status: Dict[str, Any]):
        """Save current status to file"""
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def generate_status_report(self) -> str:
        """Generate a comprehensive status report"""
        status = self.update_from_current_data()
        
        report = f"""
# CANDIDATE EXTRACTION STATUS REPORT

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status File:** {self.status_file}

## 📊 EXTRACTION SUMMARY

- **Total Candidates Expected:** {status['extraction_summary']['total_candidates_expected']}
- **Total Candidates Extracted:** {status['extraction_summary']['total_candidates_extracted']}
- **Total Candidates Saved:** {status['extraction_summary']['total_candidates_saved']}
- **Total Candidates Rated:** {status['extraction_summary']['total_candidates_rated']}
- **Extraction Completion:** {status['extraction_summary']['extraction_completion_percentage']:.1f}%

## 🎯 JOB POSTING BREAKDOWN

"""
        
        for job_title, details in status['job_postings'].items():
            completion = (details['saved_candidates'] / details['expected_candidates']) * 100 if details['expected_candidates'] > 0 else 0
            report += f"""
### {job_title[:50]}...
- **Expected:** {details['expected_candidates']} candidates
- **Extracted:** {details['extracted_candidates']} candidates
- **Saved:** {details['saved_candidates']} candidates
- **Rated:** {details['rated_candidates']} candidates
- **Completion:** {completion:.1f}%
"""
        
        report += f"""
## 🔄 PROCESSING STAGES

"""
        
        stage_icons = {
            "completed": "✅",
            "in_progress": "🔄",
            "pending": "⏳",
            "failed": "❌"
        }
        
        for stage, status_val in status['processing_stages'].items():
            icon = stage_icons.get(status_val, "❓")
            report += f"- {icon} **{stage.replace('_', ' ').title()}:** {status_val}\n"
        
        report += f"""
## 📈 PROGRESS ANALYSIS

**Current Status:** {'🟢 COMPLETED' if status['extraction_summary']['extraction_completion_percentage'] >= 100 else '🟡 IN PROGRESS' if status['extraction_summary']['extraction_completion_percentage'] > 0 else '🔴 NOT STARTED'}

**Missing Candidates:** {status['extraction_summary']['total_candidates_expected'] - status['extraction_summary']['total_candidates_saved']}

**Next Steps:**
"""
        
        if status['extraction_summary']['total_candidates_saved'] < status['extraction_summary']['total_candidates_expected']:
            report += "- Continue extracting candidates from remaining screenshots\n"
        
        if status['extraction_summary']['total_candidates_rated'] < status['extraction_summary']['total_candidates_saved']:
            report += "- Process remaining candidates for ratings and profile lookup\n"
        
        if status['extraction_summary']['total_candidates_saved'] >= status['extraction_summary']['total_candidates_expected']:
            report += "- All candidates extracted! Focus on rating and profile enhancement\n"
        
        return report
    
    def create_html_status_dashboard(self) -> str:
        """Create an HTML dashboard for status tracking"""
        status = self.update_from_current_data()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Candidate Extraction Status Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
        }}
        .job-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .job-title {{
            font-weight: bold;
            color: #495057;
            margin-bottom: 15px;
        }}
        .stages-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .stage-card {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #dee2e6;
        }}
        .stage-status {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-completed {{ background: #d4edda; color: #155724; }}
        .status-in_progress {{ background: #fff3cd; color: #856404; }}
        .status-pending {{ background: #f8d7da; color: #721c24; }}
        .auto-refresh {{
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {{
            window.location.reload();
        }}, 30000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Candidate Extraction Status</h1>
            <p>Real-time tracking of Upwork screenshot processing</p>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{status['extraction_summary']['total_candidates_expected']}</div>
                    <div class="stat-label">Expected Candidates</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{status['extraction_summary']['total_candidates_extracted']}</div>
                    <div class="stat-label">Extracted Candidates</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{status['extraction_summary']['total_candidates_saved']}</div>
                    <div class="stat-label">Saved to Database</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{status['extraction_summary']['total_candidates_rated']}</div>
                    <div class="stat-label">Rated Candidates</div>
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Overall Progress</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {status['extraction_summary']['extraction_completion_percentage']}%"></div>
                </div>
                <div class="stat-number">{status['extraction_summary']['extraction_completion_percentage']:.1f}%</div>
            </div>
            
            <h2>📋 Job Posting Details</h2>
"""
        
        for job_title, details in status['job_postings'].items():
            completion = (details['saved_candidates'] / details['expected_candidates']) * 100 if details['expected_candidates'] > 0 else 0
            html += f"""
            <div class="job-section">
                <div class="job-title">{job_title[:80]}{'...' if len(job_title) > 80 else ''}</div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{details['expected_candidates']}</div>
                        <div class="stat-label">Expected</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{details['extracted_candidates']}</div>
                        <div class="stat-label">Extracted</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{details['saved_candidates']}</div>
                        <div class="stat-label">Saved</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{details['rated_candidates']}</div>
                        <div class="stat-label">Rated</div>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion}%"></div>
                </div>
                <div style="text-align: center; margin-top: 10px; color: #6c757d;">
                    {completion:.1f}% Complete
                </div>
            </div>
"""
        
        html += f"""
            <h2>🔄 Processing Stages</h2>
            <div class="stages-grid">
"""
        
        stage_icons = {
            "completed": "✅",
            "in_progress": "🔄",
            "pending": "⏳",
            "failed": "❌"
        }
        
        for stage, status_val in status['processing_stages'].items():
            icon = stage_icons.get(status_val, "❓")
            html += f"""
                <div class="stage-card">
                    <div style="font-weight: bold; margin-bottom: 5px;">
                        {icon} {stage.replace('_', ' ').title()}
                    </div>
                    <div class="stage-status status-{status_val}">{status_val}</div>
                </div>
"""
        
        html += f"""
            </div>
            
            <div class="auto-refresh">
                🔄 Auto-refreshing every 30 seconds | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return html

def main():
    tracker = ExtractionStatusTracker()
    
    # Update and save status
    status = tracker.update_from_current_data()
    tracker.save_status(status)
    
    # Generate reports
    report = tracker.generate_status_report()
    html_dashboard = tracker.create_html_status_dashboard()
    
    # Save reports
    os.makedirs("output/reports", exist_ok=True)
    
    with open("output/reports/extraction_status_report.md", "w") as f:
        f.write(report)
    
    with open("output/reports/extraction_status_dashboard.html", "w") as f:
        f.write(html_dashboard)
    
    print("✅ Extraction status updated and reports generated!")
    print(f"📊 Current Status: {status['extraction_summary']['total_candidates_saved']}/{status['extraction_summary']['total_candidates_expected']} candidates ({status['extraction_summary']['extraction_completion_percentage']:.1f}%)")
    print(f"📄 Reports saved to:")
    print(f"   - output/reports/extraction_status_report.md")
    print(f"   - output/reports/extraction_status_dashboard.html")

if __name__ == "__main__":
    main() 