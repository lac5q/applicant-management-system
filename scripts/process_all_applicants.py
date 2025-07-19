#!/usr/bin/env python3
"""
Process All Applicants - Load all applicants from various sources into the database
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from applicant_database_manager import ApplicantDatabaseManager

class AllApplicantsProcessor:
    """Process all applicants from various sources into the database"""
    
    def __init__(self):
        self.db_manager = ApplicantDatabaseManager()
        self.processed_count = 0
        self.skipped_count = 0
        self.errors = []
        
        print("🔄 All Applicants Processor")
        print("=" * 60)
        print("📊 Loading applicants from all available sources")
        print("💾 Adding to SQLite database with full processing")
    
    def load_json_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # If it's a dict, look for common keys that might contain lists
                for key in ['applicants', 'freelancers', 'data', 'results']:
                    if key in data and isinstance(data[key], list):
                        return data[key]
                # If no list found, return the dict as a single item
                return [data]
            else:
                return []
                
        except Exception as e:
            self.errors.append(f"Error loading {filepath}: {str(e)}")
            return []
    
    def normalize_applicant_data(self, raw_data: Dict[str, Any], source_file: str) -> Optional[Dict[str, Any]]:
        """Normalize applicant data from various sources"""
        try:
            # Handle different data structures
            applicant = {}
            
            # Extract basic info with fallbacks
            applicant['id'] = raw_data.get('id') or raw_data.get('upwork_id') or raw_data.get('freelancer_id')
            applicant['name'] = raw_data.get('name') or raw_data.get('full_name') or 'Unknown Name'
            applicant['title'] = raw_data.get('title') or raw_data.get('job_title') or raw_data.get('headline') or 'No Title'
            applicant['location'] = raw_data.get('location') or raw_data.get('country') or 'Unknown Location'
            
            # Handle hourly rate variations
            hourly_rate = raw_data.get('hourly_rate') or raw_data.get('rate') or raw_data.get('price')
            if hourly_rate:
                if isinstance(hourly_rate, (int, float)):
                    applicant['hourly_rate'] = f"${hourly_rate}/hr"
                else:
                    applicant['hourly_rate'] = str(hourly_rate)
            else:
                applicant['hourly_rate'] = "Not specified"
            
            # Handle job success variations
            job_success = raw_data.get('job_success') or raw_data.get('success_rate') or raw_data.get('rating')
            if job_success:
                if isinstance(job_success, (int, float)):
                    applicant['job_success'] = f"{job_success}% Job Success"
                else:
                    applicant['job_success'] = str(job_success)
            else:
                applicant['job_success'] = "Not specified"
            
            # Handle earnings
            total_earned = raw_data.get('total_earned') or raw_data.get('earnings') or raw_data.get('revenue')
            if total_earned:
                if isinstance(total_earned, (int, float)):
                    applicant['total_earned'] = f"${total_earned:,.0f}+ earned"
                else:
                    applicant['total_earned'] = str(total_earned)
            else:
                applicant['total_earned'] = "Not specified"
            
            # Handle hours worked
            hours_worked = raw_data.get('hours_worked') or raw_data.get('total_hours') or raw_data.get('hours')
            if hours_worked:
                if isinstance(hours_worked, (int, float)):
                    applicant['hours_worked'] = f"{hours_worked:,.0f}+ hours"
                else:
                    applicant['hours_worked'] = str(hours_worked)
            else:
                applicant['hours_worked'] = "Not specified"
            
            # Handle jobs completed
            jobs_completed = raw_data.get('jobs_completed') or raw_data.get('total_jobs') or raw_data.get('projects')
            if jobs_completed:
                if isinstance(jobs_completed, (int, float)):
                    applicant['jobs_completed'] = f"{jobs_completed:,.0f}+ jobs"
                else:
                    applicant['jobs_completed'] = str(jobs_completed)
            else:
                applicant['jobs_completed'] = "Not specified"
            
            # Handle overview/description
            applicant['overview'] = (
                raw_data.get('overview') or 
                raw_data.get('description') or 
                raw_data.get('bio') or 
                raw_data.get('summary') or 
                "No overview available"
            )
            
            # Handle proposal text
            applicant['proposal_text'] = (
                raw_data.get('proposal_text') or 
                raw_data.get('proposal') or 
                raw_data.get('cover_letter') or 
                raw_data.get('message') or 
                ""
            )
            
            # Handle skills
            skills = raw_data.get('skills') or raw_data.get('expertise') or raw_data.get('tags') or []
            if isinstance(skills, str):
                # If skills is a string, split by common delimiters
                skills = [s.strip() for s in skills.replace(',', ';').split(';') if s.strip()]
            elif not isinstance(skills, list):
                skills = []
            applicant['skills'] = skills
            
            # Handle job title (try to extract from source file or use default)
            job_title = raw_data.get('job_title') or raw_data.get('position') or raw_data.get('role')
            if not job_title:
                # Try to extract from filename
                if 'shopify' in source_file.lower():
                    job_title = "Shopify Developer Position"
                elif 'ux' in source_file.lower() or 'design' in source_file.lower():
                    job_title = "UX/UI Designer Position"
                else:
                    job_title = "General Position"
            applicant['job_title'] = job_title
            
            # Handle profile URL
            applicant['profile_url'] = raw_data.get('profile_url') or raw_data.get('url') or raw_data.get('link') or ""
            
            # Handle rating data if available
            if 'rating_data' in raw_data:
                applicant['rating_data'] = raw_data['rating_data']
                applicant['rating'] = raw_data['rating_data'].get('ratings', {}).get('overall', 0)
            else:
                applicant['rating'] = raw_data.get('rating', 0)
            
            # Handle status
            applicant['status'] = raw_data.get('status', 'pending')
            
            # Handle notes
            applicant['notes'] = raw_data.get('notes') or raw_data.get('comments') or ""
            
            # Handle applied date
            applied_date = raw_data.get('applied_date') or raw_data.get('date') or raw_data.get('created_at')
            if applied_date:
                if isinstance(applied_date, str):
                    applicant['applied_date'] = applied_date
                else:
                    applicant['applied_date'] = datetime.now().strftime('%Y-%m-%d')
            else:
                applicant['applied_date'] = datetime.now().strftime('%Y-%m-%d')
            
            return applicant
            
        except Exception as e:
            self.errors.append(f"Error normalizing applicant data: {str(e)}")
            return None
    
    def process_file(self, filepath: str) -> int:
        """Process a single file and add applicants to database"""
        print(f"\n📁 Processing: {os.path.basename(filepath)}")
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return 0
        
        # Load data from file
        raw_data = self.load_json_file(filepath)
        if not raw_data:
            print(f"⚠️  No data found in: {filepath}")
            return 0
        
        print(f"📊 Found {len(raw_data)} items in {filepath}")
        
        processed = 0
        for item in raw_data:
            try:
                # Normalize the data
                applicant = self.normalize_applicant_data(item, filepath)
                if applicant:
                    # Add to database
                    self.db_manager.add_applicant(applicant)
                    processed += 1
                    self.processed_count += 1
                else:
                    self.skipped_count += 1
            except Exception as e:
                self.errors.append(f"Error processing item in {filepath}: {str(e)}")
                self.skipped_count += 1
        
        print(f"✅ Processed {processed} applicants from {filepath}")
        return processed
    
    def process_all_sources(self):
        """Process all available applicant sources"""
        print("\n🚀 Starting comprehensive applicant processing...")
        
        # Define all possible source files
        source_files = [
            # Main applicant files
            "../output/applicants/rated_applicants_20250719_015943.json",
            "../output/applicants/upwork_applicants_20250719_015513.json",
            
            # Real jobs data
            "../output/real_jobs/upwork_freelancers_20250719_014553.json",
            "../output/real_jobs/upwork_jobs_20250719_014553.json",
            
            # Any other potential sources
            "../output/final_results/applicants.json",
            "../output/test_results/applicants.json",
            "../output/freelancers/applicants.json",
        ]
        
        total_processed = 0
        
        for filepath in source_files:
            if os.path.exists(filepath):
                processed = self.process_file(filepath)
                total_processed += processed
            else:
                print(f"📁 Skipping (not found): {filepath}")
        
        # Also check for any JSON files in the applicants directory
        applicants_dir = "../output/applicants"
        if os.path.exists(applicants_dir):
            for filename in os.listdir(applicants_dir):
                if filename.endswith('.json') and filename not in ['rated_applicants_20250719_015943.json', 'upwork_applicants_20250719_015513.json']:
                    filepath = os.path.join(applicants_dir, filename)
                    processed = self.process_file(filepath)
                    total_processed += processed
        
        return total_processed
    
    def generate_processing_report(self):
        """Generate a report of the processing results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"../output/reports/applicant_processing_report_{timestamp}.html"
        
        # Get final statistics
        stats = self.db_manager.get_statistics()
        jobs = self.db_manager.get_jobs()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Applicant Processing Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
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
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #007bff;
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
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #007bff;
            color: white;
        }}
        .error {{
            color: #dc3545;
            background: #f8d7da;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }}
        .success {{
            color: #155724;
            background: #d4edda;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Applicant Processing Report</h1>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{self.processed_count}</div>
                <div>Applicants Processed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.skipped_count}</div>
                <div>Items Skipped</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_applicants']}</div>
                <div>Total in Database</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(jobs)}</div>
                <div>Jobs Tracked</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Processing Summary</h2>
            <div class="success">
                ✅ Successfully processed {self.processed_count} applicants from various sources
            </div>
            {f'<div class="error">⚠️ Skipped {self.skipped_count} items due to data issues</div>' if self.skipped_count > 0 else ''}
        </div>
        
        <div class="section">
            <h2>📈 Database Statistics</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Count</th>
                </tr>
                <tr>
                    <td>Total Applicants</td>
                    <td>{stats['total_applicants']}</td>
                </tr>
                <tr>
                    <td>Pending Review</td>
                    <td>{stats['status_breakdown'].get('pending', 0)}</td>
                </tr>
                <tr>
                    <td>Interview Candidates</td>
                    <td>{stats['status_breakdown'].get('interview', 0)}</td>
                </tr>
                <tr>
                    <td>Hired</td>
                    <td>{stats['status_breakdown'].get('hired', 0)}</td>
                </tr>
                <tr>
                    <td>Rejected</td>
                    <td>{stats['status_breakdown'].get('rejected', 0)}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>💼 Jobs Overview</h2>
            <table>
                <tr>
                    <th>Job Title</th>
                    <th>Applicants</th>
                    <th>Created</th>
                </tr>
                {''.join(f'''
                <tr>
                    <td>{job['job_title']}</td>
                    <td>{job['applicant_count']}</td>
                    <td>{job['created_at']}</td>
                </tr>
                ''' for job in jobs)}
            </table>
        </div>
        
        {f'''
        <div class="section">
            <h2>⚠️ Processing Errors</h2>
            {''.join(f'<div class="error">{error}</div>' for error in self.errors)}
        </div>
        ''' if self.errors else ''}
        
        <div class="section">
            <h2>🎯 Next Steps</h2>
            <ul>
                <li>Review the enhanced applicant interface to see all processed applicants</li>
                <li>Use the filtering options to find the best candidates</li>
                <li>Update applicant statuses as you review them</li>
                <li>Schedule interviews with top candidates</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """
        
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Generated processing report: {report_file}")
        return report_file
    
    def run(self):
        """Main processing workflow"""
        print("🔄 Starting comprehensive applicant processing...")
        
        # Process all sources
        total_processed = self.process_all_sources()
        
        # Generate report
        report_file = self.generate_processing_report()
        
        # Final summary
        stats = self.db_manager.get_statistics()
        jobs = self.db_manager.get_jobs()
        
        print(f"\n🎉 Processing Complete!")
        print(f"📊 Total Applicants Processed: {self.processed_count}")
        print(f"⚠️  Items Skipped: {self.skipped_count}")
        print(f"💾 Total in Database: {stats['total_applicants']}")
        print(f"💼 Jobs Tracked: {len(jobs)}")
        print(f"📄 Report: {report_file}")
        
        if self.errors:
            print(f"\n⚠️  Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Open the enhanced interface to review all applicants")
        print(f"   2. Use job filtering to see candidates by position")
        print(f"   3. Update statuses and ratings as you review")
        print(f"   4. Schedule interviews with top candidates")

def main():
    """Main function"""
    processor = AllApplicantsProcessor()
    processor.run()

if __name__ == "__main__":
    main() 