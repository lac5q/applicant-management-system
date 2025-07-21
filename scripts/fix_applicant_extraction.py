#!/usr/bin/env python3
"""
Fix Applicant Extraction - Extract ALL applicants from HTML downloads
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class FixedApplicantExtractor:
    def __init__(self):
        self.downloads_dir = "context/Applicant Page Downloads"
        self.output_dir = "output/processed_candidates"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Job configurations
        self.jobs = {
            "ux_conversion_designer": {
                "filename": "__🎨 URGENT_ Contract-to-Hire UX_Conversion Designer - Start This Week__.html",
                "title": "UX Conversion Designer",
                "keywords": ["UX", "UI", "Design", "Conversion", "Figma", "Adobe", "Prototype", "Wireframe"]
            },
            "shopify_developer": {
                "filename": "__🚨 URGENT_ Contract-to-Hire Shopify Developer + UX Specialist - Start This Week__.html",
                "title": "Shopify Developer + UX Specialist",
                "keywords": ["Shopify", "Development", "UX", "UI", "E-commerce", "Liquid", "JavaScript", "CSS"]
            }
        }
        
    def print_progress(self, message: str, current: int = None, total: int = None):
        """Print progress message with optional progress bar"""
        if current is not None and total is not None:
            percentage = (current / total) * 100
            bar_length = 30
            filled_length = int(bar_length * current // total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            print(f"\r{message} [{bar}] {percentage:.1f}% ({current}/{total})", end='', flush=True)
        else:
            print(f"🔄 {message}")
            
    def extract_applicants_from_html(self, html_file_path: str, job_type: str) -> List[Dict]:
        """Extract ALL applicants from HTML file using improved patterns"""
        applicants = []
        
        try:
            print(f"🔗 Reading HTML file: {os.path.basename(html_file_path)}")
            with open(html_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"🔍 Searching for applicants in {job_type}...")
            
            # Find all applicant rows - look for the table rows with applicant data
            # Pattern: <tr ... data-ev-position_on_page="X" ... data-ev-contractor_uid="&quot;Y&quot;" ...
            applicant_rows = re.findall(
                r'<tr[^>]*data-ev-position_on_page="(\d+)"[^>]*data-ev-contractor_uid="&quot;(\d+)&quot;"[^>]*>(.*?)</tr>',
                content,
                re.DOTALL
            )
            
            print(f"✅ Found {len(applicant_rows)} applicant rows to process")
            
            for i, (position, uid, row_content) in enumerate(applicant_rows):
                self.print_progress(f"Processing applicant {i+1}/{len(applicant_rows)}", i+1, len(applicant_rows))
                
                # Extract applicant data from the row content
                applicant = self.extract_applicant_from_row(row_content, position, uid, job_type)
                if applicant:
                    applicants.append(applicant)
            
            print(f"\n✅ Successfully processed {len(applicants)} applicants for {job_type}")
            return applicants
            
        except Exception as e:
            print(f"❌ Error reading HTML file: {e}")
            return []
    
    def extract_applicant_from_row(self, row_content: str, position: str, uid: str, job_type: str) -> Optional[Dict]:
        """Extract applicant data from a table row"""
        try:
            # Extract name - look for the name span
            name_match = re.search(r'<span[^>]*class="[^"]*h6[^"]*"[^>]*>([^<]+)</span>', row_content)
            name = name_match.group(1).strip() if name_match else f"Applicant {position}"
            
            # Extract title/overview - look for the line-clamp div
            title_match = re.search(r'<div[^>]*class="[^"]*air3-line-clamp[^"]*"[^>]*>([^<]+)</div>', row_content)
            title = title_match.group(1).strip() if title_match else "Not specified"
            
            # Extract location
            location_match = re.search(r'<div[^>]*class="[^"]*font-weight-base[^"]*"[^>]*>([^<]+)</div>', row_content)
            location = location_match.group(1).strip() if location_match else "Location not specified"
            
            # Extract stats
            rate_match = re.search(r'\$(\d+(?:\.\d+)?)/hr', row_content)
            success_match = re.search(r'(\d+)%\s+Job Success', row_content)
            earned_match = re.search(r'\$([\d,]+K?)\+?\s+earned', row_content)
            hours_match = re.search(r'(\d+)\s+total hours', row_content)
            jobs_match = re.search(r'(\d+)\s+completed jobs', row_content)
            
            # Extract skills
            skills = self.extract_skills_from_row(row_content)
            
            # Extract proposal text
            proposal = self.extract_proposal_from_row(row_content)
            
            # Calculate rating
            rating = self.calculate_rating(rate_match, success_match, hours_match, jobs_match, skills, job_type)
            
            return {
                "id": f"{job_type}_{uid}_{position}",
                "name": name,
                "title": title,
                "position": int(position),
                "contractor_uid": uid,
                "job_type": job_type,
                "job_title": self.jobs[job_type]["title"],
                "hourly_rate": f"${rate_match.group(1)}/hr" if rate_match else "Not specified",
                "job_success": f"{success_match.group(1)}% Job Success" if success_match else "Not specified",
                "total_earned": f"${earned_match.group(1)}+ earned" if earned_match else "Not specified",
                "hours_worked": f"{hours_match.group(1)} total hours" if hours_match else "Not specified",
                "jobs_completed": f"{jobs_match.group(1)} completed jobs" if jobs_match else "Not specified",
                "skills": skills,
                "overview": title,
                "proposal_text": proposal,
                "location": location,
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "New",
                "rating": rating,
                "ranking_score": 0.0,
                "rank": 0,
                "notes": "",
                "profile_image": "",
                "screenshot_source": f"context/Applicant Page Downloads/{self.jobs[job_type]['filename']}",
                "portfolio_links": [],
                "profile_url": f"https://www.upwork.com/freelancers/{uid}",
                "lookup_status": "pending",
                "lookup_data": {},
                "is_rated": False
            }
            
        except Exception as e:
            print(f"\n⚠️ Error processing applicant {position}: {e}")
            return None
    
    def extract_skills_from_row(self, row_content: str) -> List[str]:
        """Extract skills from row content"""
        skills = []
        
        # Look for skill tokens
        skill_matches = re.findall(r'<span[^>]*class="[^"]*ellipsis[^"]*"[^>]*>\s*([^<]+)\s*</span>', row_content)
        
        for skill in skill_matches:
            skill_text = skill.strip()
            if skill_text and len(skill_text) > 2 and skill_text not in skills:
                skills.append(skill_text)
        
        return skills[:10]  # Limit to 10 skills
    
    def extract_proposal_from_row(self, row_content: str) -> str:
        """Extract proposal text from row content"""
        # Look for proposal text in the details cell
        proposal_match = re.search(r'Cover letter[^<]*<span[^>]*>([^<]+)</span>', row_content)
        
        if proposal_match:
            proposal = proposal_match.group(1).strip()
            return proposal[:500] + "..." if len(proposal) > 500 else proposal
        
        return "Proposal text not available"
    
    def calculate_rating(self, rate_match, success_match, hours_match, jobs_match, skills: List[str], job_type: str) -> float:
        """Calculate rating based on multiple factors"""
        rating = 0.0
        
        # Job success rate (0-100)
        if success_match:
            try:
                success_rate = float(success_match.group(1))
                rating += (success_rate / 100) * 2.0  # Max 2 points
            except:
                pass
        
        # Hours worked (experience)
        if hours_match:
            try:
                hours = float(hours_match.group(1))
                if hours > 1000:
                    rating += 1.0
                elif hours > 500:
                    rating += 0.5
            except:
                pass
        
        # Jobs completed
        if jobs_match:
            try:
                jobs = float(jobs_match.group(1))
                if jobs > 50:
                    rating += 1.0
                elif jobs > 20:
                    rating += 0.5
            except:
                pass
        
        # Skills match
        job_keywords = self.jobs[job_type]["keywords"]
        skill_matches = sum(1 for skill in skills if any(keyword.lower() in skill.lower() for keyword in job_keywords))
        rating += min(skill_matches * 0.3, 1.0)  # Max 1 point
        
        # Hourly rate (reasonable range)
        if rate_match:
            try:
                rate = float(rate_match.group(1))
                if 20 <= rate <= 100:  # Reasonable range
                    rating += 0.5
            except:
                pass
        
        return min(rating, 5.0)  # Cap at 5.0
    
    def calculate_ranking_score(self, applicant: Dict, job_type: str) -> float:
        """Calculate comprehensive ranking score"""
        score = 0.0
        job_config = self.jobs[job_type]
        
        # Job success rate (30% weight)
        if applicant.get("job_success") != "Not specified":
            try:
                success_rate = float(re.search(r'(\d+)', applicant["job_success"]).group(1))
                score += (success_rate / 100) * 0.3
            except:
                pass
        
        # Hours worked (20% weight)
        if applicant.get("hours_worked") != "Not specified":
            try:
                hours = float(re.search(r'(\d+)', applicant["hours_worked"]).group(1))
                score += min(hours / 10000, 1.0) * 0.2
            except:
                pass
        
        # Jobs completed (15% weight)
        if applicant.get("jobs_completed") != "Not specified":
            try:
                jobs = float(re.search(r'(\d+)', applicant["jobs_completed"]).group(1))
                score += min(jobs / 500, 1.0) * 0.15
            except:
                pass
        
        # Skills match (25% weight)
        skills = applicant.get("skills", [])
        job_keywords = job_config["keywords"]
        skill_matches = sum(1 for skill in skills if any(keyword.lower() in skill.lower() for keyword in job_keywords))
        score += min(skill_matches / len(job_keywords), 1.0) * 0.25
        
        # Hourly rate (10% weight)
        if applicant.get("hourly_rate") != "Not specified":
            try:
                rate = float(re.search(r'(\d+)', applicant["hourly_rate"]).group(1))
                if 20 <= rate <= 80:  # Sweet spot
                    score += 0.1
                elif 15 <= rate <= 100:  # Acceptable range
                    score += 0.05
            except:
                pass
        
        return min(score * 5.0, 5.0)  # Scale to 0-5
    
    def rank_applicants(self, applicants: List[Dict], job_type: str) -> List[Dict]:
        """Rank applicants for a specific job"""
        print(f"🏆 Ranking {len(applicants)} applicants...")
        
        for applicant in applicants:
            applicant["ranking_score"] = self.calculate_ranking_score(applicant, job_type)
            applicant["is_rated"] = True
        
        # Sort by ranking score (descending)
        ranked_applicants = sorted(applicants, key=lambda x: x["ranking_score"], reverse=True)
        
        # Assign ranks
        for i, applicant in enumerate(ranked_applicants):
            applicant["rank"] = i + 1
        
        print(f"✅ Ranking complete!")
        print(f"  ✅ Found {len(ranked_applicants)} applicants")
        print(f"  🏆 Top 3 ranked:")
        for i in range(min(3, len(ranked_applicants))):
            applicant = ranked_applicants[i]
            print(f"    {i+1}. {applicant['name']} - Score: {applicant['ranking_score']:.2f} - Rate: {applicant['hourly_rate']}")
        
        return ranked_applicants
    
    def process_all_jobs(self):
        """Process all jobs and extract ALL applicants"""
        print("🎯 Fixed Applicant Extraction System")
        print("=" * 60)
        print("🚀 Starting comprehensive applicant extraction")
        print("=" * 60)
        
        all_applicants = []
        job_results = {}
        
        for job_type, job_config in self.jobs.items():
            print(f"\n📋 Processing {job_config['title']}...")
            
            html_file = os.path.join(self.downloads_dir, job_config['filename'])
            if not os.path.exists(html_file):
                print(f"❌ HTML file not found: {html_file}")
                continue
            
            # Extract applicants
            applicants = self.extract_applicants_from_html(html_file, job_type)
            
            if applicants:
                # Rank applicants
                ranked_applicants = self.rank_applicants(applicants, job_type)
                
                # Save job-specific results
                job_results[job_type] = ranked_applicants
                all_applicants.extend(ranked_applicants)
                
                # Save individual job results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                job_filename = f"ranked_applicants_{job_type}_{timestamp}.json"
                job_path = os.path.join(self.output_dir, job_filename)
                
                with open(job_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "job_type": job_type,
                        "job_title": self.jobs[job_type]["title"],
                        "total_applicants": len(ranked_applicants),
                        "timestamp": timestamp,
                        "applicants": ranked_applicants
                    }, f, indent=2, ensure_ascii=False)
                
                print(f"  ✅ Saved {job_type} rankings to {job_path}")
        
        # Save combined results
        if all_applicants:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            combined_filename = f"all_ranked_applicants_{timestamp}.json"
            combined_path = os.path.join(self.output_dir, combined_filename)
            
            with open(combined_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_applicants": len(all_applicants),
                    "jobs_processed": list(self.jobs.keys()),
                    "timestamp": timestamp,
                    "applicants": all_applicants
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saving results...")
            print(f"  ✅ Saved combined rankings to {combined_path}")
            
            # Update frontend data
            frontend_path = "nextjs-app/data/candidates.json"
            with open(frontend_path, 'w', encoding='utf-8') as f:
                json.dump(all_applicants, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Updated frontend data with {len(all_applicants)} applicants")
        
        print("\n" + "=" * 60)
        print("🎉 EXTRACTION COMPLETE!")
        print("=" * 60)
        
        for job_type, applicants in job_results.items():
            print(f"\n📊 {self.jobs[job_type]['title']}:")
            print(f"  📈 Total Applicants: {len(applicants)}")
            print(f"  🏆 Top 5 Ranked Applicants:")
            for i in range(min(5, len(applicants))):
                applicant = applicants[i]
                print(f"    {i+1}. {applicant['name']} - Score: {applicant['ranking_score']:.2f} - Rate: {applicant['hourly_rate']}")
        
        print(f"\n✨ All done! Extracted {len(all_applicants)} total applicants.")

def main():
    extractor = FixedApplicantExtractor()
    extractor.process_all_jobs()

if __name__ == "__main__":
    main()
