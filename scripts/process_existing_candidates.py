#!/usr/bin/env python3
"""
Simplified Candidate Processing Script
Processes existing candidate data from JSON files and generates reports.
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import re

class CandidateDataProcessor:
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.output_dir = self.workspace_path / "output"
        self.processed_dir = self.output_dir / "processed_candidates"
        self.processed_dir.mkdir(exist_ok=True)
        
        # Database setup
        self.db_path = self.output_dir / "applicants" / "applicants.db"
        self.setup_database()
        
        # Timestamp for processing
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def setup_database(self):
        """Setup SQLite database for storing processed candidate data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create candidates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_candidates (
                id TEXT PRIMARY KEY,
                name TEXT,
                title TEXT,
                location TEXT,
                hourly_rate TEXT,
                job_success TEXT,
                total_earned TEXT,
                hours_worked TEXT,
                jobs_completed TEXT,
                skills TEXT,
                overview TEXT,
                proposal_text TEXT,
                job_title TEXT,
                profile_url TEXT,
                status TEXT DEFAULT 'pending',
                rating INTEGER DEFAULT 0,
                applied_date TEXT,
                notes TEXT,
                profile_image TEXT,
                screenshot_source TEXT,
                portfolio_links TEXT,
                work_samples TEXT,
                processed_at TEXT,
                source_file TEXT,
                data_quality_score REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def save_candidate_to_db(self, candidate: Dict[str, Any], source_file: str):
        """Save candidate data to SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert lists to JSON strings
        skills_json = json.dumps(candidate.get("skills", []))
        portfolio_links_json = json.dumps(candidate.get("portfolio_links", []))
        work_samples_json = json.dumps(candidate.get("work_samples", []))
        
        # Calculate data quality score
        data_quality_score = self.calculate_data_quality(candidate)
        
        cursor.execute('''
            INSERT OR REPLACE INTO processed_candidates (
                id, name, title, location, hourly_rate, job_success, total_earned,
                hours_worked, jobs_completed, skills, overview, proposal_text,
                job_title, profile_url, status, rating, applied_date, notes,
                profile_image, screenshot_source, portfolio_links, work_samples,
                processed_at, source_file, data_quality_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate.get("id", ""), candidate.get("name", ""), candidate.get("title", ""), 
            candidate.get("location", ""), candidate.get("hourly_rate", ""), 
            candidate.get("job_success", ""), candidate.get("total_earned", ""),
            candidate.get("hours_worked", ""), candidate.get("jobs_completed", ""), 
            skills_json, candidate.get("overview", ""), candidate.get("proposal_text", ""),
            candidate.get("job_title", ""), candidate.get("profile_url", ""), 
            candidate.get("status", "pending"), candidate.get("rating", 0),
            candidate.get("applied_date", datetime.now().strftime("%Y-%m-%d")), 
            candidate.get("notes", ""), candidate.get("profile_image", ""),
            candidate.get("screenshot_source", ""), portfolio_links_json, work_samples_json,
            datetime.now().isoformat(), source_file, data_quality_score
        ))
        
        conn.commit()
        conn.close()
    
    def calculate_data_quality(self, candidate: Dict[str, Any]) -> float:
        """Calculate a data quality score for the candidate."""
        score = 0.0
        total_fields = 0
        
        # Check required fields
        required_fields = ["name", "title", "location", "hourly_rate"]
        for field in required_fields:
            total_fields += 1
            if candidate.get(field):
                score += 1.0
        
        # Check optional but valuable fields
        optional_fields = ["skills", "overview", "proposal_text", "profile_url", "portfolio_links"]
        for field in optional_fields:
            total_fields += 1
            if candidate.get(field):
                if isinstance(candidate[field], list) and len(candidate[field]) > 0:
                    score += 1.0
                elif isinstance(candidate[field], str) and len(candidate[field].strip()) > 0:
                    score += 1.0
        
        # Check job success rate
        if candidate.get("job_success"):
            job_success = candidate["job_success"]
            if "%" in job_success:
                try:
                    rate = int(re.search(r'(\d+)', job_success).group(1))
                    if rate >= 90:
                        score += 1.0
                    elif rate >= 80:
                        score += 0.8
                    elif rate >= 70:
                        score += 0.6
                    else:
                        score += 0.3
                    total_fields += 1
                except:
                    pass
        
        return (score / total_fields) * 100 if total_fields > 0 else 0.0
    
    def process_json_file(self, json_file: Path) -> List[Dict[str, Any]]:
        """Process a single JSON file and extract candidates."""
        processed_candidates = []
        
        try:
            print(f"Processing: {json_file}")
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                candidates = data
            elif isinstance(data, dict) and "applicants" in data:
                candidates = data["applicants"]
            elif isinstance(data, dict) and "candidates" in data:
                candidates = data["candidates"]
            else:
                print(f"Unknown data structure in {json_file}")
                return []
            
            print(f"Found {len(candidates)} candidates in {json_file.name}")
            
            for i, candidate in enumerate(candidates):
                if isinstance(candidate, dict):
                    # Ensure candidate has an ID
                    if not candidate.get("id"):
                        candidate["id"] = f"{json_file.stem}_{i:03d}"
                    
                    # Save to database
                    self.save_candidate_to_db(candidate, json_file.name)
                    processed_candidates.append(candidate)
            
            return processed_candidates
            
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
            return []
    
    def process_all_json_files(self) -> Dict[str, List[Dict[str, Any]]]:
        """Process all JSON files containing candidate data."""
        json_files = [
            self.output_dir / "screenshot_applicants" / "screenshot_applicants_20250719_021451.json",
            self.output_dir / "applicants" / "rated_applicants_20250719_015943.json",
            self.output_dir / "applicants" / "upwork_applicants_20250719_015513.json"
        ]
        
        all_candidates = {}
        
        for json_file in json_files:
            if json_file.exists():
                candidates = self.process_json_file(json_file)
                all_candidates[json_file.name] = candidates
            else:
                print(f"File not found: {json_file}")
        
        return all_candidates
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report of all processed candidates."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total candidates
        cursor.execute("SELECT COUNT(*) FROM processed_candidates")
        total_candidates = cursor.fetchone()[0]
        
        # Get candidates by source file
        cursor.execute("SELECT source_file, COUNT(*) FROM processed_candidates GROUP BY source_file")
        source_stats = dict(cursor.fetchall())
        
        # Get candidates by status
        cursor.execute("SELECT status, COUNT(*) FROM processed_candidates GROUP BY status")
        status_stats = dict(cursor.fetchall())
        
        # Get average data quality score
        cursor.execute("SELECT AVG(data_quality_score) FROM processed_candidates")
        avg_quality = cursor.fetchone()[0] or 0.0
        
        # Get top skills
        cursor.execute("SELECT skills FROM processed_candidates WHERE skills IS NOT NULL AND skills != '[]'")
        all_skills = []
        for row in cursor.fetchall():
            try:
                skills = json.loads(row[0])
                all_skills.extend(skills)
            except:
                continue
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Get hourly rate distribution
        cursor.execute("SELECT hourly_rate FROM processed_candidates WHERE hourly_rate IS NOT NULL AND hourly_rate != ''")
        hourly_rates = []
        for row in cursor.fetchall():
            rate = row[0]
            if rate and '$' in rate:
                try:
                    rate_value = float(re.search(r'\$(\d+(?:\.\d{2})?)', rate).group(1))
                    hourly_rates.append(rate_value)
                except:
                    continue
        
        rate_stats = {
            "min": min(hourly_rates) if hourly_rates else 0,
            "max": max(hourly_rates) if hourly_rates else 0,
            "avg": sum(hourly_rates) / len(hourly_rates) if hourly_rates else 0,
            "count": len(hourly_rates)
        }
        
        # Get location distribution
        cursor.execute("SELECT location, COUNT(*) FROM processed_candidates WHERE location IS NOT NULL AND location != '' GROUP BY location ORDER BY COUNT(*) DESC LIMIT 10")
        top_locations = dict(cursor.fetchall())
        
        conn.close()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_candidates": total_candidates,
            "source_breakdown": source_stats,
            "status_breakdown": status_stats,
            "average_data_quality": round(avg_quality, 2),
            "top_skills": top_skills,
            "hourly_rate_stats": rate_stats,
            "top_locations": top_locations,
            "processing_timestamp": self.timestamp
        }
        
        return report
    
    def export_all_candidates(self) -> str:
        """Export all candidates to JSON file."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM processed_candidates")
        columns = [description[0] for description in cursor.description]
        
        candidates = []
        for row in cursor.fetchall():
            candidate = dict(zip(columns, row))
            # Parse JSON fields
            for field in ['skills', 'portfolio_links', 'work_samples']:
                if candidate[field]:
                    try:
                        candidate[field] = json.loads(candidate[field])
                    except:
                        candidate[field] = []
                else:
                    candidate[field] = []
            candidates.append(candidate)
        
        conn.close()
        
        # Save to file
        export_path = self.processed_dir / f"all_processed_candidates_{self.timestamp}.json"
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
        
        return str(export_path)
    
    def generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate an HTML report of the processing results."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Candidate Processing Report - {self.timestamp}</title>
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
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .summary-card {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-card h3 {{
            color: #2c3e50;
            margin: 0 0 10px 0;
        }}
        .summary-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .skill-tag {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 10px;
            margin: 2px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        .location-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }}
        .timestamp {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Candidate Processing Report</h1>
        <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Candidates</h3>
                <div class="number">{report['total_candidates']}</div>
            </div>
            <div class="summary-card">
                <h3>Average Data Quality</h3>
                <div class="number">{report['average_data_quality']}%</div>
            </div>
            <div class="summary-card">
                <h3>Data Sources</h3>
                <div class="number">{len(report['source_breakdown'])}</div>
            </div>
            <div class="summary-card">
                <h3>Average Hourly Rate</h3>
                <div class="number">${report['hourly_rate_stats']['avg']:.2f}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Data Sources</h2>
            <ul>
                {''.join([f'<li><strong>{source}:</strong> {count} candidates</li>' for source, count in report['source_breakdown'].items()])}
            </ul>
        </div>
        
        <div class="section">
            <h2>Top Skills</h2>
            <div>
                {''.join([f'<span class="skill-tag">{skill} ({count})</span>' for skill, count in report['top_skills'][:20]])}
            </div>
        </div>
        
        <div class="section">
            <h2>Top Locations</h2>
            <div>
                {''.join([f'<div class="location-item"><span>{location}</span><span>{count} candidates</span></div>' for location, count in report['top_locations'].items()])}
            </div>
        </div>
        
        <div class="section">
            <h2>Hourly Rate Statistics</h2>
            <ul>
                <li><strong>Minimum:</strong> ${report['hourly_rate_stats']['min']:.2f}/hr</li>
                <li><strong>Maximum:</strong> ${report['hourly_rate_stats']['max']:.2f}/hr</li>
                <li><strong>Average:</strong> ${report['hourly_rate_stats']['avg']:.2f}/hr</li>
                <li><strong>Candidates with rates:</strong> {report['hourly_rate_stats']['count']}</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Status Distribution</h2>
            <ul>
                {''.join([f'<li><strong>{status}:</strong> {count} candidates</li>' for status, count in report['status_breakdown'].items()])}
            </ul>
        </div>
    </div>
</body>
</html>
        """
        
        html_path = self.processed_dir / f"candidate_processing_report_{self.timestamp}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)
    
    def run_processing(self):
        """Run the complete candidate processing pipeline."""
        print("Starting candidate data processing...")
        
        # Step 1: Process all JSON files
        print("Step 1: Processing JSON files...")
        all_candidates = self.process_all_json_files()
        
        total_processed = sum(len(candidates) for candidates in all_candidates.values())
        print(f"Processed {total_processed} candidates from {len(all_candidates)} files")
        
        # Step 2: Generate comprehensive report
        print("Step 2: Generating comprehensive report...")
        report = self.generate_comprehensive_report()
        
        # Step 3: Export all candidates
        print("Step 3: Exporting all candidates...")
        export_path = self.export_all_candidates()
        
        # Step 4: Generate HTML report
        print("Step 4: Generating HTML report...")
        html_path = self.generate_html_report(report)
        
        print(f"\nProcessing complete!")
        print(f"Total candidates processed: {report['total_candidates']}")
        print(f"Average data quality: {report['average_data_quality']}%")
        print(f"JSON export: {export_path}")
        print(f"HTML report: {html_path}")
        
        return {
            "report": report,
            "export_path": export_path,
            "html_path": html_path,
            "total_processed": total_processed
        }

def main():
    """Main function to run the candidate processor."""
    processor = CandidateDataProcessor()
    
    try:
        results = processor.run_processing()
        
        # Print summary
        print("\n" + "="*60)
        print("CANDIDATE DATA PROCESSING SUMMARY")
        print("="*60)
        print(f"Total Candidates Processed: {results['report']['total_candidates']}")
        print(f"Average Data Quality Score: {results['report']['average_data_quality']}%")
        print(f"Data Sources: {len(results['report']['source_breakdown'])}")
        print(f"Top Skills: {', '.join([skill for skill, _ in results['report']['top_skills'][:5]])}")
        print(f"Average Hourly Rate: ${results['report']['hourly_rate_stats']['avg']:.2f}/hr")
        print(f"Export File: {results['export_path']}")
        print(f"HTML Report: {results['html_path']}")
        print("="*60)
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 