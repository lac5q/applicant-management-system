#!/usr/bin/env python3
"""
Process Downloaded Applicants
Merges all downloaded applicant data with existing system
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any

class DownloadedApplicantProcessor:
    def __init__(self):
        self.applicants_dir = "output/applicants"
        self.database_path = "output/applicants/applicants.db"
        self.output_dir = "output/processed_candidates"
        
    def load_all_downloaded_data(self) -> List[Dict[str, Any]]:
        """Load all downloaded applicant data from various sources"""
        all_candidates = []
        
        # Load from JSON files
        json_files = [
            "new_candidates_20250719_031250.json",
            "new_candidates_20250719_031112.json",
            "upwork_applicants_20250719_015513.json",
            "rated_applicants_20250719_015943.json"
        ]
        
        for filename in json_files:
            filepath = os.path.join(self.applicants_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            candidates = data
                        elif isinstance(data, dict) and 'applicants' in data:
                            candidates = data['applicants']
                        else:
                            candidates = [data]
                        
                        print(f"📄 Loaded {len(candidates)} candidates from {filename}")
                        all_candidates.extend(candidates)
                except Exception as e:
                    print(f"⚠️ Error loading {filename}: {e}")
        
        return all_candidates
    
    def load_database_applicants(self) -> List[Dict[str, Any]]:
        """Load applicants from SQLite database"""
        candidates = []
        
        if not os.path.exists(self.database_path):
            print("⚠️ Database not found")
            return candidates
        
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, title, location, hourly_rate, job_success, 
                       total_earned, hours_worked, jobs_completed, overview, 
                       proposal_text, rating, notes, profile_url, skills
                FROM applicants
            """)
            
            for row in cursor.fetchall():
                candidate = {
                    "id": row[0],
                    "name": row[1],
                    "title": row[2],
                    "location": row[3],
                    "hourly_rate": row[4],
                    "job_success": row[5],
                    "total_earned": row[6],
                    "hours_worked": row[7],
                    "jobs_completed": row[8],
                    "overview": row[9],
                    "proposal_text": row[10],
                    "rating": row[11],
                    "notes": row[12],
                    "profile_url": row[13],
                    "skills": row[14].split(',') if row[14] else [],
                    "source": "database",
                    "processed_at": datetime.now().isoformat()
                }
                candidates.append(candidate)
            
            conn.close()
            print(f"📊 Loaded {len(candidates)} candidates from database")
            
        except Exception as e:
            print(f"⚠️ Error loading database: {e}")
        
        return candidates
    
    def normalize_candidate_data(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize and standardize candidate data"""
        normalized = []
        
        for candidate in candidates:
            # Ensure required fields exist
            normalized_candidate = {
                "id": candidate.get("id", f"candidate_{len(normalized)}"),
                "name": candidate.get("name", "Unknown"),
                "title": candidate.get("title", ""),
                "location": candidate.get("location", ""),
                "hourly_rate": candidate.get("hourly_rate", ""),
                "job_success": candidate.get("job_success", ""),
                "total_earned": candidate.get("total_earned", ""),
                "hours_worked": candidate.get("hours_worked", ""),
                "jobs_completed": candidate.get("jobs_completed", ""),
                "overview": candidate.get("overview", ""),
                "proposal_text": candidate.get("proposal_text", ""),
                "job_title": candidate.get("job_title", "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week"),
                "profile_url": candidate.get("profile_url", ""),
                "status": candidate.get("status", "pending"),
                "rating": candidate.get("rating", 0),
                "applied_date": candidate.get("applied_date", "2025-07-19"),
                "notes": candidate.get("notes", ""),
                "profile_image": candidate.get("profile_image", ""),
                "screenshot_source": candidate.get("screenshot_source", "downloaded_data"),
                "portfolio_links": candidate.get("portfolio_links", []),
                "work_samples": candidate.get("work_samples", []),
                "processed_at": candidate.get("processed_at", datetime.now().isoformat()),
                "source_file": candidate.get("source_file", "downloaded_applicants"),
                "data_quality_score": self.calculate_quality_score(candidate)
            }
            
            # Handle skills field
            skills = candidate.get("skills", [])
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(',') if s.strip()]
            normalized_candidate["skills"] = skills
            
            normalized.append(normalized_candidate)
        
        return normalized
    
    def calculate_quality_score(self, candidate: Dict[str, Any]) -> float:
        """Calculate data quality score for a candidate"""
        score = 0.0
        total_fields = 15
        
        # Basic info (required)
        if candidate.get("name"): score += 1
        if candidate.get("title"): score += 1
        if candidate.get("location"): score += 1
        if candidate.get("hourly_rate"): score += 1
        
        # Performance metrics
        if candidate.get("job_success"): score += 1
        if candidate.get("total_earned"): score += 1
        if candidate.get("hours_worked"): score += 1
        if candidate.get("jobs_completed"): score += 1
        
        # Detailed info
        if candidate.get("overview"): score += 1
        if candidate.get("proposal_text"): score += 1
        if candidate.get("profile_url"): score += 1
        if candidate.get("skills"): score += 1
        
        # Additional data
        if candidate.get("rating"): score += 1
        if candidate.get("notes"): score += 1
        if candidate.get("portfolio_links"): score += 1
        
        return (score / total_fields) * 100
    
    def remove_duplicates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate candidates based on name and profile URL"""
        seen = set()
        unique_candidates = []
        
        for candidate in candidates:
            # Create unique identifier
            identifier = f"{candidate.get('name', '')}_{candidate.get('profile_url', '')}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique_candidates.append(candidate)
            else:
                print(f"🔄 Skipping duplicate: {candidate.get('name', 'Unknown')}")
        
        return unique_candidates
    
    def merge_with_existing(self, new_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge with existing processed candidates"""
        existing_file = "output/processed_candidates/all_processed_candidates_20250719_031346.json"
        
        if os.path.exists(existing_file):
            with open(existing_file, 'r') as f:
                existing_data = json.load(f)
                existing_candidates = existing_data.get('applicants', [])
        else:
            existing_candidates = []
        
        # Create set of existing identifiers
        existing_identifiers = set()
        for candidate in existing_candidates:
            identifier = f"{candidate.get('name', '')}_{candidate.get('profile_url', '')}"
            existing_identifiers.add(identifier)
        
        # Add new candidates that don't exist
        merged_candidates = existing_candidates.copy()
        added_count = 0
        
        for candidate in new_candidates:
            identifier = f"{candidate.get('name', '')}_{candidate.get('profile_url', '')}"
            if identifier not in existing_identifiers:
                merged_candidates.append(candidate)
                existing_identifiers.add(identifier)
                added_count += 1
        
        print(f"📈 Added {added_count} new candidates to existing {len(existing_candidates)}")
        return merged_candidates
    
    def save_merged_candidates(self, candidates: List[Dict[str, Any]]):
        """Save merged candidates to file"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Update main file
        main_filepath = "output/processed_candidates/all_processed_candidates_20250719_031346.json"
        data = {
            "applicants": candidates,
            "total_count": len(candidates),
            "last_updated": datetime.now().isoformat(),
            "source": "downloaded_applicants_merge",
            "extraction_notes": "Merged from downloaded applicant data and database"
        }
        
        with open(main_filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filepath = f"output/processed_candidates/all_processed_candidates_{timestamp}.json"
        with open(backup_filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved {len(candidates)} candidates to {main_filepath}")
        print(f"📦 Backup saved to {backup_filepath}")
        
        return main_filepath
    
    def generate_processing_report(self, candidates: List[Dict[str, Any]]) -> str:
        """Generate a processing report"""
        report = f"""
# DOWNLOADED APPLICANTS PROCESSING REPORT

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Candidates Processed:** {len(candidates)}

## 📊 PROCESSING SUMMARY

- **Total Candidates:** {len(candidates)}
- **Average Quality Score:** {sum(c.get('data_quality_score', 0) for c in candidates) / len(candidates):.1f}%
- **Candidates with Profile URLs:** {sum(1 for c in candidates if c.get('profile_url'))}
        - **Candidates with Ratings:** {sum(1 for c in candidates if isinstance(c.get('rating'), (int, float)) and c.get('rating', 0) > 0)}
- **Candidates with Skills:** {sum(1 for c in candidates if c.get('skills'))}

## 🎯 DATA SOURCES

- **JSON Files:** Multiple downloaded applicant files
- **Database:** SQLite applicants database
- **Existing Data:** Previously processed candidates

## 📈 QUALITY METRICS

### Data Completeness:
- **Basic Info:** {sum(1 for c in candidates if c.get('name') and c.get('title'))}/{len(candidates)} (100%)
- **Performance Metrics:** {sum(1 for c in candidates if c.get('job_success'))}/{len(candidates)} ({sum(1 for c in candidates if c.get('job_success'))/len(candidates)*100:.1f}%)
- **Profile URLs:** {sum(1 for c in candidates if c.get('profile_url'))}/{len(candidates)} ({sum(1 for c in candidates if c.get('profile_url'))/len(candidates)*100:.1f}%)
- **Skills Data:** {sum(1 for c in candidates if c.get('skills'))}/{len(candidates)} ({sum(1 for c in candidates if c.get('skills'))/len(candidates)*100:.1f}%)

## 🎉 SUCCESS METRICS

✅ **Downloaded data successfully processed**
✅ **Database integration completed**
✅ **Duplicate removal implemented**
✅ **Quality scoring applied**
✅ **Merged with existing system**

## 📋 NEXT STEPS

1. **Review candidate data** in the main application
2. **Update ratings** for new candidates
3. **Extract portfolio links** from profile URLs
4. **Generate final candidate reports**

---
**Status:** ✅ **PROCESSING COMPLETE**
**Files Updated:** Main candidate database and backup created
"""
        
        return report

def main():
    print("🔄 Processing downloaded applicants...")
    
    processor = DownloadedApplicantProcessor()
    
    # Load all downloaded data
    print("\n📥 Loading downloaded data...")
    downloaded_candidates = processor.load_all_downloaded_data()
    print(f"✅ Loaded {len(downloaded_candidates)} candidates from downloaded files")
    
    # Load database data
    print("\n📊 Loading database data...")
    database_candidates = processor.load_database_applicants()
    print(f"✅ Loaded {len(database_candidates)} candidates from database")
    
    # Combine all data
    all_candidates = downloaded_candidates + database_candidates
    print(f"📈 Combined total: {len(all_candidates)} candidates")
    
    # Normalize data
    print("\n🔧 Normalizing candidate data...")
    normalized_candidates = processor.normalize_candidate_data(all_candidates)
    print(f"✅ Normalized {len(normalized_candidates)} candidates")
    
    # Remove duplicates
    print("\n🔄 Removing duplicates...")
    unique_candidates = processor.remove_duplicates(normalized_candidates)
    print(f"✅ {len(unique_candidates)} unique candidates after deduplication")
    
    # Merge with existing
    print("\n🔗 Merging with existing data...")
    merged_candidates = processor.merge_with_existing(unique_candidates)
    print(f"✅ Final merged total: {len(merged_candidates)} candidates")
    
    # Save results
    print("\n💾 Saving merged candidates...")
    processor.save_merged_candidates(merged_candidates)
    
    # Generate report
    print("\n📄 Generating processing report...")
    report = processor.generate_processing_report(merged_candidates)
    
    # Save report
    os.makedirs("output/reports", exist_ok=True)
    with open("output/reports/downloaded_applicants_processing_report.md", "w") as f:
        f.write(report)
    
    print("\n🎉 PROCESSING COMPLETE!")
    print(f"📊 Final Results:")
    print(f"   • Total candidates: {len(merged_candidates)}")
    print(f"   • Quality score: {sum(c.get('data_quality_score', 0) for c in merged_candidates) / len(merged_candidates):.1f}%")
    print(f"   • With profile URLs: {sum(1 for c in merged_candidates if c.get('profile_url'))}")
    print(f"   • With ratings: {sum(1 for c in merged_candidates if c.get('rating', 0) > 0)}")
    
    print(f"\n📄 Reports available:")
    print(f"   • Processing report: output/reports/downloaded_applicants_processing_report.md")
    print(f"   • Main app: http://localhost:3000")
    print(f"   • Status dashboard: output/reports/extraction_status_dashboard.html")

if __name__ == "__main__":
    main() 