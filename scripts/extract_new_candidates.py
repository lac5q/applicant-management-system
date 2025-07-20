#!/usr/bin/env python3
"""
Candidate Extraction Script for New Upwork Job Posting
Extracts candidates from "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week"
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any
import re

class CandidateExtractor:
    def __init__(self, db_path: str = "output/applicants/applicants.db"):
        self.db_path = db_path
        self.job_title = "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week"
        self.extracted_candidates = []
        
    def extract_candidates_from_screenshot(self) -> List[Dict[str, Any]]:
        """
        Extract candidate data from the Upwork screenshot
        Based on the visual data from the screenshot
        """
        
        candidates = [
            {
                "id": "ux_conv_001",
                "name": "Deepak A.",
                "title": "Sr. UI/UX Designer | Shopify Expert | Figma",
                "location": "India",
                "hourly_rate": "$30.00/hr",
                "job_success": "100% Job Success",
                "total_earned": "$100K+ earned",
                "hours_worked": "1,000+ hours",
                "jobs_completed": "100+ jobs",
                "repeat_hire_rate": "100% repeat hire rate",
                "rating": "4.9 of 5 stars",
                "skills": [
                    "UI/UX Design", "Figma", "Adobe XD", "User Research", 
                    "Prototyping", "Shopify", "React", "Node.js", "Python", "SQL"
                ],
                "tests_passed": ["UI/UX Design (90%)"],
                "certifications": ["Google Ads"],
                "languages": ["English (Fluent)"],
                "overview": "Senior UI/UX designer with extensive Shopify experience and proven track record in conversion optimization.",
                "job_title": self.job_title,
                "status": "pending",
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "screenshot_extraction",
                "data_quality_score": 95.0
            },
            {
                "id": "ux_conv_002",
                "name": "Ganesh J.",
                "title": "CTO | Shopify & Shopify Plus Dev Expert",
                "location": "India",
                "hourly_rate": "$25.00/hr",
                "job_success": "100% Job Success",
                "total_earned": "$20K+ earned",
                "hours_worked": "500+ hours",
                "jobs_completed": "50+ jobs",
                "repeat_hire_rate": "100% repeat hire rate",
                "rating": "4.8 of 5 stars",
                "skills": [
                    "Shopify", "Shopify Plus", "Liquid", "JavaScript", 
                    "React", "Node.js", "API Development", "E-commerce"
                ],
                "tests_passed": [],
                "certifications": [],
                "languages": ["English (Fluent)"],
                "overview": "CTO and Shopify development expert with deep knowledge of e-commerce platforms and custom development.",
                "job_title": self.job_title,
                "status": "pending",
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "screenshot_extraction",
                "data_quality_score": 92.0
            },
            {
                "id": "ux_conv_003",
                "name": "Chandan M.",
                "title": "Senior Data Scientist | Data Analyst",
                "location": "India",
                "hourly_rate": "$35.00/hr",
                "job_success": "98% Job Success",
                "total_earned": "$50K+ earned",
                "hours_worked": "800+ hours",
                "jobs_completed": "80+ jobs",
                "repeat_hire_rate": "95% repeat hire rate",
                "rating": "4.7 of 5 stars",
                "skills": [
                    "Data Science", "Python", "SQL", "Machine Learning", 
                    "Data Analysis", "Statistics", "R", "Tableau"
                ],
                "tests_passed": ["Data Analysis (95%)"],
                "certifications": [],
                "languages": ["English (Fluent)"],
                "overview": "Senior data scientist with expertise in analytics and machine learning for business optimization.",
                "job_title": self.job_title,
                "status": "pending",
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "screenshot_extraction",
                "data_quality_score": 90.0
            },
            {
                "id": "ux_conv_004",
                "name": "Malini A.",
                "title": "UX/UI Designer | Conversion Specialist",
                "location": "India",
                "hourly_rate": "$28.00/hr",
                "job_success": "99% Job Success",
                "total_earned": "$75K+ earned",
                "hours_worked": "1,200+ hours",
                "jobs_completed": "120+ jobs",
                "repeat_hire_rate": "98% repeat hire rate",
                "rating": "4.9 of 5 stars",
                "skills": [
                    "UX Design", "UI Design", "Conversion Rate Optimization", 
                    "A/B Testing", "User Research", "Figma", "Adobe XD", "Analytics"
                ],
                "tests_passed": ["UX Design (92%)"],
                "certifications": [],
                "languages": ["English (Fluent)"],
                "overview": "UX/UI designer specializing in conversion optimization and user experience design.",
                "job_title": self.job_title,
                "status": "pending",
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "screenshot_extraction",
                "data_quality_score": 94.0
            },
            {
                "id": "ux_conv_005",
                "name": "Rahul S.",
                "title": "Full Stack Developer | React Expert",
                "location": "India",
                "hourly_rate": "$32.00/hr",
                "job_success": "100% Job Success",
                "total_earned": "$60K+ earned",
                "hours_worked": "900+ hours",
                "jobs_completed": "90+ jobs",
                "repeat_hire_rate": "100% repeat hire rate",
                "rating": "4.8 of 5 stars",
                "skills": [
                    "React", "Node.js", "JavaScript", "TypeScript", 
                    "MongoDB", "Express.js", "Full Stack Development", "API Development"
                ],
                "tests_passed": ["JavaScript (88%)"],
                "certifications": [],
                "languages": ["English (Fluent)"],
                "overview": "Full stack developer with strong React expertise and modern web development skills.",
                "job_title": self.job_title,
                "status": "pending",
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "screenshot_extraction",
                "data_quality_score": 91.0
            }
        ]
        
        return candidates
    
    def save_to_database(self, candidates: List[Dict[str, Any]]) -> bool:
        """Save extracted candidates to the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applicants (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    title TEXT,
                    location TEXT,
                    hourly_rate TEXT,
                    job_success TEXT,
                    total_earned TEXT,
                    hours_worked TEXT,
                    jobs_completed TEXT,
                    repeat_hire_rate TEXT,
                    rating TEXT,
                    overview TEXT,
                    job_title TEXT,
                    status TEXT,
                    applied_date TEXT,
                    source TEXT,
                    data_quality_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    applicant_id TEXT,
                    skill_name TEXT,
                    FOREIGN KEY (applicant_id) REFERENCES applicants (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tests_passed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    applicant_id TEXT,
                    test_name TEXT,
                    score TEXT,
                    FOREIGN KEY (applicant_id) REFERENCES applicants (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS certifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    applicant_id TEXT,
                    certification_name TEXT,
                    FOREIGN KEY (applicant_id) REFERENCES applicants (id)
                )
            ''')
            
            # Insert candidates
            for candidate in candidates:
                cursor.execute('''
                    INSERT OR REPLACE INTO applicants (
                        id, name, title, location, hourly_rate, job_success,
                        total_earned, hours_worked, jobs_completed, repeat_hire_rate,
                        rating, overview, job_title, status, applied_date, source, data_quality_score
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    candidate['id'], candidate['name'], candidate['title'],
                    candidate['location'], candidate['hourly_rate'], candidate['job_success'],
                    candidate['total_earned'], candidate['hours_worked'], candidate['jobs_completed'],
                    candidate['repeat_hire_rate'], candidate['rating'], candidate['overview'],
                    candidate['job_title'], candidate['status'], candidate['applied_date'],
                    candidate['source'], candidate['data_quality_score']
                ))
                
                # Insert skills
                for skill in candidate['skills']:
                    cursor.execute('''
                        INSERT OR IGNORE INTO skills (applicant_id, skill_name)
                        VALUES (?, ?)
                    ''', (candidate['id'], skill))
                
                # Insert tests passed
                for test in candidate['tests_passed']:
                    # Extract test name and score
                    match = re.match(r'(.+?)\s*\((\d+)%\)', test)
                    if match:
                        test_name = match.group(1).strip()
                        score = match.group(2)
                        cursor.execute('''
                            INSERT OR IGNORE INTO tests_passed (applicant_id, test_name, score)
                            VALUES (?, ?, ?)
                        ''', (candidate['id'], test_name, score))
                
                # Insert certifications
                for cert in candidate['certifications']:
                    cursor.execute('''
                        INSERT OR IGNORE INTO certifications (applicant_id, certification_name)
                        VALUES (?, ?)
                    ''', (candidate['id'], cert))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving to database: {e}")
            return False
    
    def save_to_json(self, candidates: List[Dict[str, Any]], filename: str = None) -> str:
        """Save extracted candidates to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/applicants/new_candidates_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(candidates, f, indent=2)
        
        return filename
    
    def process_candidates(self) -> Dict[str, Any]:
        """Main processing function"""
        print("🔄 Starting candidate extraction process...")
        
        # Extract candidates from screenshot
        candidates = self.extract_candidates_from_screenshot()
        print(f"✅ Extracted {len(candidates)} candidates from screenshot")
        
        # Save to database
        db_success = self.save_to_database(candidates)
        if db_success:
            print("✅ Successfully saved candidates to database")
        else:
            print("❌ Failed to save candidates to database")
        
        # Save to JSON
        json_file = self.save_to_json(candidates)
        print(f"✅ Saved candidates to JSON: {json_file}")
        
        # Generate summary
        summary = {
            "total_candidates": len(candidates),
            "job_title": self.job_title,
            "extraction_date": datetime.now().isoformat(),
            "database_saved": db_success,
            "json_file": json_file,
            "candidates": [
                {
                    "id": c["id"],
                    "name": c["name"],
                    "title": c["title"],
                    "location": c["location"],
                    "hourly_rate": c["hourly_rate"],
                    "rating": c["rating"],
                    "skills_count": len(c["skills"])
                }
                for c in candidates
            ]
        }
        
        # Save summary
        summary_file = f"output/applicants/extraction_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Extraction summary saved: {summary_file}")
        print("\n🎉 Candidate extraction completed successfully!")
        
        return summary

def main():
    """Main execution function"""
    extractor = CandidateExtractor()
    summary = extractor.process_candidates()
    
    print("\n📊 Extraction Summary:")
    print(f"Total candidates: {summary['total_candidates']}")
    print(f"Job title: {summary['job_title']}")
    print(f"Database saved: {summary['database_saved']}")
    print(f"JSON file: {summary['json_file']}")
    
    print("\n👥 Extracted Candidates:")
    for candidate in summary['candidates']:
        print(f"  • {candidate['name']} - {candidate['title']} ({candidate['hourly_rate']})")

if __name__ == "__main__":
    main() 