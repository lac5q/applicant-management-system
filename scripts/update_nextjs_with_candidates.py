#!/usr/bin/env python3
"""
Update Next.js Application with Processed Candidate Data
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def update_nextjs_candidates():
    """Update the Next.js application with processed candidate data."""
    
    # Paths
    workspace_path = Path(".")
    processed_data_path = workspace_path / "output" / "processed_candidates" / "all_processed_candidates_20250719_023841.json"
    nextjs_app_path = workspace_path / "nextjs-app"
    nextjs_public_path = nextjs_app_path / "public"
    nextjs_data_path = nextjs_app_path / "data"
    
    # Create data directory if it doesn't exist
    nextjs_data_path.mkdir(exist_ok=True)
    
    try:
        # Read processed candidate data
        with open(processed_data_path, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
        
        # Transform data for Next.js
        transformed_candidates = []
        for candidate in candidates:
            # Create a clean candidate object for the frontend
            transformed_candidate = {
                "id": candidate.get("id", ""),
                "name": candidate.get("name", ""),
                "title": candidate.get("title", ""),
                "location": candidate.get("location", ""),
                "hourly_rate": candidate.get("hourly_rate", ""),
                "job_success": candidate.get("job_success", ""),
                "total_earned": candidate.get("total_earned", ""),
                "hours_worked": candidate.get("hours_worked", ""),
                "jobs_completed": candidate.get("jobs_completed", ""),
                "skills": candidate.get("skills", []),
                "overview": candidate.get("overview", ""),
                "proposal_text": candidate.get("proposal_text", ""),
                "job_title": candidate.get("job_title", ""),
                "profile_url": candidate.get("profile_url", ""),
                "status": candidate.get("status", "pending"),
                "rating": candidate.get("rating", 0),
                "applied_date": candidate.get("applied_date", ""),
                "notes": candidate.get("notes", ""),
                "profile_image": candidate.get("profile_image", ""),
                "portfolio_links": candidate.get("portfolio_links", []),
                "work_samples": candidate.get("work_samples", []),
                "data_quality_score": candidate.get("data_quality_score", 0.0)
            }
            transformed_candidates.append(transformed_candidate)
        
        # Save to Next.js data directory
        candidates_file = nextjs_data_path / "candidates.json"
        with open(candidates_file, 'w', encoding='utf-8') as f:
            json.dump(transformed_candidates, f, indent=2, ensure_ascii=False)
        
        # Generate statistics
        stats = {
            "total_candidates": len(transformed_candidates),
            "average_hourly_rate": sum([
                float(c.get("hourly_rate", "0").replace("$", "").replace("/hr", "")) 
                for c in transformed_candidates 
                if c.get("hourly_rate") and "$" in c.get("hourly_rate", "")
            ]) / len([c for c in transformed_candidates if c.get("hourly_rate") and "$" in c.get("hourly_rate", "")]),
            "top_skills": get_top_skills(transformed_candidates),
            "locations": get_location_distribution(transformed_candidates),
            "last_updated": datetime.now().isoformat()
        }
        
        # Save statistics
        stats_file = nextjs_data_path / "stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        # Copy HTML report to public directory
        html_report_path = workspace_path / "output" / "processed_candidates" / "candidate_processing_report_20250719_023841.html"
        if html_report_path.exists():
            shutil.copy2(html_report_path, nextjs_public_path / "candidate_report.html")
        
        # Copy summary markdown
        summary_path = workspace_path / "output" / "processed_candidates" / "CANDIDATE_EXTRACTION_SUMMARY.md"
        if summary_path.exists():
            shutil.copy2(summary_path, nextjs_public_path / "candidate_summary.md")
        
        print(f"✅ Successfully updated Next.js application with {len(transformed_candidates)} candidates")
        print(f"📁 Data files saved to: {nextjs_data_path}")
        print(f"📊 Statistics generated: {stats_file}")
        print(f"🌐 HTML report copied to: {nextjs_public_path / 'candidate_report.html'}")
        
        return {
            "candidates_count": len(transformed_candidates),
            "data_file": str(candidates_file),
            "stats_file": str(stats_file),
            "html_report": str(nextjs_public_path / "candidate_report.html")
        }
        
    except Exception as e:
        print(f"❌ Error updating Next.js application: {str(e)}")
        return None

def get_top_skills(candidates, top_n=10):
    """Extract top skills from candidates."""
    skill_counts = {}
    for candidate in candidates:
        skills = candidate.get("skills", [])
        for skill in skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    return sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

def get_location_distribution(candidates):
    """Get location distribution of candidates."""
    location_counts = {}
    for candidate in candidates:
        location = candidate.get("location", "Unknown")
        location_counts[location] = location_counts.get(location, 0) + 1
    
    return location_counts

if __name__ == "__main__":
    result = update_nextjs_candidates()
    if result:
        print(f"\n🎉 Next.js application updated successfully!")
        print(f"📈 Total candidates: {result['candidates_count']}")
    else:
        print("❌ Failed to update Next.js application") 