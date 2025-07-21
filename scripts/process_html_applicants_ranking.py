#!/usr/bin/env python3
"""
Process HTML Applicants and Create Separate Rankings for Each Job
Extracts applicants from downloaded HTML files and creates separate rankings
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class HTMLApplicantProcessor:
    def __init__(self):
        self.downloads_dir = "context/Applicant Page Downloads"
        self.output_dir = "output/processed_candidates"
        self.web_dir = "output/web"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.web_dir, exist_ok=True)
        
        # Job-specific data
        self.jobs = {
            "ux_conversion_designer": {
                "filename": "__🎨 URGENT_ Contract-to-Hire UX_Conversion Designer - Start This Week__.html",
                "title": "UX Conversion Designer",
                "keywords": ["UX", "UI", "Design", "Conversion", "Figma", "Adobe", "Prototype"]
            },
            "shopify_developer": {
                "filename": "__🚨 URGENT_ Contract-to-Hire Shopify Developer + UX Specialist - Start This Week__.html",
                "title": "Shopify Developer + UX Specialist", 
                "keywords": ["Shopify", "Development", "UX", "UI", "E-commerce", "Liquid", "JavaScript"]
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
        """Extract applicant data from HTML file"""
        applicants = []
        
        try:
            print(f"🔗 Reading HTML file: {os.path.basename(html_file_path)}")
            with open(html_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"🔍 Searching for applicants in {job_type}...")
            # Extract applicant sections using regex
            applicant_pattern = r'data-ev-position_on_page="(\d+)".*?data-ev-contractor_uid="&quot;(\d+)&quot;".*?<span[^>]*>([^<]+)</span>.*?<span[^>]*>([^<]+)</span>'
            matches = re.findall(applicant_pattern, content, re.DOTALL)
            
            print(f"✅ Found {len(matches)} applicants to process")
            
            for i, (position, uid, name, title) in enumerate(matches):
                self.print_progress(f"Processing applicant {i+1}/{len(matches)}: {name}", i+1, len(matches))
                
                # Extract additional data using more specific patterns
                rate_pattern = r'\$(\d+(?:\.\d+)?)/hr'
                success_pattern = r'(\d+)% Job Success'
                earned_pattern = r'\$([\d,]+K?)\+ earned'
                hours_pattern = r'(\d+)\s+total hours'
                jobs_pattern = r'(\d+)\s+completed jobs'
                
                # Find these patterns in the surrounding context
                context_start = max(0, content.find(f'data-ev-position_on_page="{position}"') - 1000)
                context_end = min(len(content), content.find(f'data-ev-position_on_page="{position}"') + 2000)
                context = content[context_start:context_end]
                
                rate_match = re.search(rate_pattern, context)
                success_match = re.search(success_pattern, context)
                earned_match = re.search(earned_pattern, context)
                hours_match = re.search(hours_pattern, context)
                jobs_match = re.search(jobs_pattern, context)
                
                applicant = {
                    "id": f"{job_type}_{uid}_{position}",
                    "name": name.strip(),
                    "title": title.strip(),
                    "position": int(position),
                    "contractor_uid": uid,
                    "job_type": job_type,
                    "hourly_rate": f"${rate_match.group(1)}/hr" if rate_match else "Not specified",
                    "job_success": f"{success_match.group(1)}% Job Success" if success_match else "Not specified",
                    "total_earned": f"${earned_match.group(1)}+ earned" if earned_match else "Not specified",
                    "hours_worked": f"{hours_match.group(1)} total hours" if hours_match else "Not specified",
                    "jobs_completed": f"{jobs_match.group(1)} completed jobs" if jobs_match else "Not specified",
                    "skills": self.extract_skills(context),
                    "overview": self.extract_overview(context),
                    "proposal_text": self.extract_proposal(context),
                    "applied_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "New",
                    "rating": self.calculate_rating(rate_match, success_match, hours_match, jobs_match),
                    "ranking_score": 0,
                    "rank": 0,
                    "notes": "",
                    "profile_image": "",
                    "screenshot_source": html_file_path,
                    "portfolio_links": [],
                    "location": self.extract_location(context)
                }
                
                applicants.append(applicant)
            
            print(f"\n✅ Successfully processed {len(applicants)} applicants for {job_type}")
                
        except Exception as e:
            print(f"❌ Error processing {html_file_path}: {str(e)}")
            
        return applicants
    
    def extract_skills(self, context: str) -> List[str]:
        """Extract skills from context"""
        skills = []
        skill_keywords = [
            "UX", "UI", "Design", "Figma", "Adobe", "Photoshop", "Illustrator", "Sketch",
            "Shopify", "Liquid", "JavaScript", "HTML", "CSS", "React", "Vue", "Angular",
            "E-commerce", "Conversion", "Prototype", "Wireframe", "User Research",
            "Mobile Design", "Web Design", "Branding", "Typography", "Color Theory"
        ]
        
        for skill in skill_keywords:
            if skill.lower() in context.lower():
                skills.append(skill)
                
        return skills[:10]  # Limit to 10 skills
    
    def extract_overview(self, context: str) -> str:
        """Extract overview from context"""
        # Look for overview text patterns
        overview_patterns = [
            r'<p[^>]*>([^<]{50,200})</p>',
            r'<div[^>]*>([^<]{50,200})</div>'
        ]
        
        for pattern in overview_patterns:
            match = re.search(pattern, context)
            if match:
                return match.group(1).strip()
                
        return "Overview not available"
    
    def extract_proposal(self, context: str) -> str:
        """Extract proposal text from context"""
        proposal_patterns = [
            r'proposal[^>]*>([^<]{100,500})</',
            r'cover[^>]*>([^<]{100,500})</'
        ]
        
        for pattern in proposal_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        return "Proposal text not available"
    
    def extract_location(self, context: str) -> str:
        """Extract location from context"""
        location_pattern = r'<span[^>]*>([A-Za-z\s,]+)</span>'
        matches = re.findall(location_pattern, context)
        
        for match in matches:
            if any(country in match for country in ["United States", "India", "Pakistan", "Ukraine", "Philippines", "Canada", "United Kingdom"]):
                return match.strip()
                
        return "Location not specified"
    
    def calculate_rating(self, rate_match, success_match, hours_match, jobs_match) -> float:
        """Calculate a rating based on various factors"""
        rating = 0.0
        
        # Rate factor (lower is better for cost)
        if rate_match:
            rate = float(rate_match.group(1))
            if rate <= 25:
                rating += 5.0
            elif rate <= 50:
                rating += 4.0
            elif rate <= 75:
                rating += 3.0
            else:
                rating += 2.0
        
        # Success rate factor
        if success_match:
            success = int(success_match.group(1))
            if success >= 95:
                rating += 5.0
            elif success >= 90:
                rating += 4.0
            elif success >= 80:
                rating += 3.0
            else:
                rating += 2.0
        
        # Experience factor (hours worked)
        if hours_match:
            hours = int(hours_match.group(1))
            if hours >= 1000:
                rating += 5.0
            elif hours >= 500:
                rating += 4.0
            elif hours >= 100:
                rating += 3.0
            else:
                rating += 2.0
        
        # Jobs completed factor
        if jobs_match:
            jobs = int(jobs_match.group(1))
            if jobs >= 50:
                rating += 5.0
            elif jobs >= 20:
                rating += 4.0
            elif jobs >= 10:
                rating += 3.0
            else:
                rating += 2.0
        
        return min(5.0, rating / 4.0)  # Normalize to 5.0 scale
    
    def calculate_ranking_score(self, applicant: Dict, job_keywords: List[str]) -> float:
        """Calculate ranking score based on job requirements"""
        score = 0.0
        
        # Base rating
        score += applicant.get('rating', 0) * 2
        
        # Skills match
        applicant_skills = [skill.lower() for skill in applicant.get('skills', [])]
        for keyword in job_keywords:
            if keyword.lower() in applicant_skills:
                score += 1.0
        
        # Experience bonus
        hours_text = applicant.get('hours_worked', '')
        if '1000+' in hours_text or '1000' in hours_text:
            score += 2.0
        elif '500+' in hours_text or '500' in hours_text:
            score += 1.5
        elif '100+' in hours_text or '100' in hours_text:
            score += 1.0
        
        # Success rate bonus
        success_text = applicant.get('job_success', '')
        if '100%' in success_text:
            score += 2.0
        elif '95%' in success_text:
            score += 1.5
        elif '90%' in success_text:
            score += 1.0
        
        return score
    
    def rank_applicants(self, applicants: List[Dict], job_keywords: List[str]) -> List[Dict]:
        """Rank applicants based on job requirements"""
        print(f"🏆 Ranking {len(applicants)} applicants...")
        
        # Calculate ranking scores
        for i, applicant in enumerate(applicants):
            self.print_progress(f"Calculating scores", i+1, len(applicants))
            applicant['ranking_score'] = self.calculate_ranking_score(applicant, job_keywords)
        
        # Sort by ranking score (highest first)
        ranked_applicants = sorted(applicants, key=lambda x: x['ranking_score'], reverse=True)
        
        # Assign ranks
        for i, applicant in enumerate(ranked_applicants):
            applicant['rank'] = i + 1
        
        print(f"\n✅ Ranking complete!")
        return ranked_applicants
    
    def process_all_jobs(self):
        """Process all job HTML files and create separate rankings"""
        print("🚀 Starting HTML Applicant Processing and Ranking")
        print("=" * 60)
        
        all_results = {}
        combined_applicants = []
        
        for job_key, job_data in self.jobs.items():
            print(f"\n📋 Processing {job_data['title']}...")
            
            html_file_path = os.path.join(self.downloads_dir, job_data['filename'])
            
            if os.path.exists(html_file_path):
                # Extract applicants
                applicants = self.extract_applicants_from_html(html_file_path, job_key)
                
                if applicants:
                    # Rank applicants for this specific job
                    ranked_applicants = self.rank_applicants(applicants, job_data['keywords'])
                    
                    # Store results
                    all_results[job_key] = {
                        "job_title": job_data['title'],
                        "total_applicants": len(ranked_applicants),
                        "applicants": ranked_applicants,
                        "keywords": job_data['keywords']
                    }
                    
                    # Add to combined list
                    for applicant in ranked_applicants:
                        applicant['job_title'] = job_data['title']
                        combined_applicants.append(applicant)
                    
                    print(f"  ✅ Found {len(ranked_applicants)} applicants")
                    print(f"  🏆 Top 3 ranked:")
                    for i, app in enumerate(ranked_applicants[:3]):
                        print(f"    {i+1}. {app['name']} - Score: {app['ranking_score']:.2f}")
                else:
                    print(f"  ⚠️  No applicants found in {html_file_path}")
            else:
                print(f"  ❌ File not found: {html_file_path}")
        
        # Create output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n💾 Saving results...")
        
        # Save job-specific rankings
        for job_key, job_results in all_results.items():
            filename = f"ranked_applicants_{job_key}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(job_results, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Saved {job_key} rankings to {filepath}")
        
        # Save combined rankings
        combined_filename = f"all_ranked_applicants_{timestamp}.json"
        combined_filepath = os.path.join(self.output_dir, combined_filename)
        
        combined_data = {
            "total_applicants": len(combined_applicants),
            "jobs_processed": list(all_results.keys()),
            "timestamp": timestamp,
            "applicants": combined_applicants
        }
        
        with open(combined_filepath, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Saved combined rankings to {combined_filepath}")
        
        # Update frontend data
        print(f"\n🌐 Updating frontend...")
        self.update_frontend_data(combined_applicants)
        
        return all_results
    
    def update_frontend_data(self, applicants: List[Dict]):
        """Update the frontend with new applicant data"""
        # Update the candidates.json file for the frontend
        frontend_data = []
        
        for applicant in applicants:
            frontend_applicant = {
                "id": applicant['id'],
                "name": applicant['name'],
                "title": applicant['title'],
                "location": applicant['location'],
                "hourly_rate": applicant['hourly_rate'],
                "job_success": applicant['job_success'],
                "total_earned": applicant['total_earned'],
                "hours_worked": applicant['hours_worked'],
                "jobs_completed": applicant['jobs_completed'],
                "skills": applicant['skills'],
                "overview": applicant['overview'],
                "proposal_text": applicant['proposal_text'],
                "job_title": applicant.get('job_title', ''),
                "profile_url": "",
                "status": applicant['status'],
                "rating": applicant['rating'],
                "ranking_score": applicant['ranking_score'],
                "rank": applicant['rank'],
                "applied_date": applicant['applied_date'],
                "notes": applicant['notes'],
                "profile_image": applicant['profile_image'],
                "screenshot_source": applicant['screenshot_source'],
                "portfolio_links": applicant['portfolio_links']
            }
            frontend_data.append(frontend_applicant)
        
        # Save to frontend data directory
        frontend_filepath = os.path.join("nextjs-app", "data", "candidates.json")
        with open(frontend_filepath, 'w', encoding='utf-8') as f:
            json.dump(frontend_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Updated frontend data with {len(frontend_data)} applicants")

def main():
    print("🎯 HTML Applicant Processing and Ranking System")
    print("=" * 60)
    
    processor = HTMLApplicantProcessor()
    results = processor.process_all_jobs()
    
    print("\n" + "="*60)
    print("🎉 PROCESSING COMPLETE!")
    print("="*60)
    
    for job_key, job_results in results.items():
        print(f"\n📊 {job_results['job_title']}:")
        print(f"  📈 Total Applicants: {job_results['total_applicants']}")
        print("  🏆 Top 5 Ranked Applicants:")
        for i, app in enumerate(job_results['applicants'][:5]):
            print(f"    {i+1}. {app['name']} - Score: {app['ranking_score']:.2f} - Rate: {app['hourly_rate']}")
    
    print(f"\n✨ All done! Check the output directory for detailed results.")

if __name__ == "__main__":
    main() 