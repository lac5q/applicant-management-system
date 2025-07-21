#!/usr/bin/env python3
"""
Final Perfected Candidate Extractor
Extracts ALL candidates with PERFECT data extraction
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class FinalPerfectedExtractor:
    def __init__(self):
        self.downloads_dir = "context/Applicant Page Downloads"
        self.output_dir = "output/processed_candidates"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Job configurations
        self.jobs = {
            "ux_conversion_designer": {
                "filename": "__🎨 URGENT_ Contract-to-Hire UX_Conversion Designer - Start This Week__.html",
                "title": "UX Conversion Designer",
                "keywords": ["UX", "UI", "Design", "Conversion", "Figma", "Adobe", "Prototype", "Wireframe", "CRO", "Landing Page"]
            },
            "shopify_developer": {
                "filename": "__🚨 URGENT_ Contract-to-Hire Shopify Developer + UX Specialist - Start This Week__.html",
                "title": "Shopify Developer + UX Specialist",
                "keywords": ["Shopify", "Development", "UX", "UI", "E-commerce", "Liquid", "JavaScript", "CSS", "Web Development"]
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
    
    def extract_perfected_applicant_data(self, html_file_path: str, job_type: str) -> List[Dict]:
        """Extract PERFECTED applicant data from HTML file"""
        applicants = []
        
        try:
            print(f"🔗 Reading HTML file: {os.path.basename(html_file_path)}")
            with open(html_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"🔍 Extracting perfected data for {job_type}...")
            
            # Find all applicant rows using the position markers
            position_matches = re.findall(r'data-ev-position_on_page="(\d+)"', content)
            contractor_matches = re.findall(r'data-ev-contractor_uid="&quot;(\d+)&quot;"', content)
            
            print(f"✅ Found {len(position_matches)} applicants to process")
            
            # Create pairs and extract perfected data
            applicant_pairs = []
            for i in range(min(len(position_matches), len(contractor_matches))):
                applicant_pairs.append((position_matches[i], contractor_matches[i]))
            
            for i, (position, uid) in enumerate(applicant_pairs):
                self.print_progress(f"Processing applicant {i+1}/{len(applicant_pairs)}", i+1, len(applicant_pairs))
                
                # Extract perfected applicant data
                applicant = self.extract_perfected_applicant_from_html(content, position, uid, job_type)
                if applicant:
                    applicants.append(applicant)
            
            print(f"\n✅ Successfully extracted {len(applicants)} applicants with perfected data")
            return applicants
            
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return []
    
    def extract_perfected_applicant_from_html(self, content: str, position: str, uid: str, job_type: str) -> Optional[Dict]:
        """Extract PERFECTED applicant data from HTML content"""
        try:
            # Find the section around this applicant
            position_pattern = f'data-ev-position_on_page="{position}"'
            start_idx = content.find(position_pattern)
            
            if start_idx == -1:
                return None
            
            # Extract a larger chunk to get all data
            chunk_start = max(0, start_idx - 4000)
            chunk_end = min(len(content), start_idx + 10000)
            chunk = content[chunk_start:chunk_end]
            
            # PERFECTED name extraction - look for the actual name in the alt attribute
            name = self.extract_perfected_name(chunk, position)
            
            # Extract title/overview
            title = self.extract_perfected_title(chunk)
            
            # Extract location
            location = self.extract_perfected_location(chunk)
            
            # Extract PERFECTED stats
            rate_match = re.search(r'\$(\d+(?:\.\d+)?)/hr', chunk)
            success_match = re.search(r'(\d+)%\s+Job Success', chunk)
            earned_match = re.search(r'\$([\d,]+K?)\+?\s+earned', chunk)
            hours_match = re.search(r'(\d+)\s+total hours', chunk)
            jobs_match = re.search(r'(\d+)\s+completed jobs', chunk)
            
            # Extract perfected skills
            skills = self.extract_perfected_skills(chunk)
            
            # Extract perfected proposal text
            proposal = self.extract_perfected_proposal(chunk)
            
            # Extract portfolio links
            portfolio_links = self.extract_perfected_portfolio_links(chunk)
            
            # Calculate perfected rating
            rating = self.calculate_perfected_rating(rate_match, success_match, hours_match, jobs_match, skills, job_type)
            
            # Create perfected applicant record
            applicant = {
                "id": f"{job_type}_{uid}_{position}",
                "name": name,
                "title": title,
                "position": int(position),
                "contractor_uid": uid,
                "job_type": job_type,
                "job_title": self.jobs[job_type]["title"],
                "hourly_rate": f"${rate_match.group(1)}/hr" if rate_match else "Rate not specified",
                "job_success": f"{success_match.group(1)}% Job Success" if success_match else "Success rate not specified",
                "total_earned": f"${earned_match.group(1)}+ earned" if earned_match else "Earnings not specified",
                "hours_worked": f"{hours_match.group(1)} total hours" if hours_match else "Hours not specified",
                "jobs_completed": f"{jobs_match.group(1)} completed jobs" if jobs_match else "Jobs not specified",
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
                "portfolio_links": portfolio_links,
                "profile_url": f"https://www.upwork.com/freelancers/{uid}",
                "lookup_status": "pending",
                "lookup_data": {},
                "is_rated": False,
                "processing_date": datetime.now().isoformat(),
                "data_quality_score": self.calculate_data_quality_score(rate_match, success_match, hours_match, jobs_match, skills, proposal),
                "extraction_method": "perfected_html_parser"
            }
            
            return applicant
            
        except Exception as e:
            print(f"\n⚠️ Error processing applicant {position}: {e}")
            return None
    
    def extract_perfected_name(self, chunk: str, position: str) -> str:
        """Extract PERFECTED name from chunk"""
        # Look for the name in the alt attribute of the profile image
        name_patterns = [
            r'alt="([^"]+)"[^>]*height="60"',
            r'alt="([^"]+)"[^>]*class="[^"]*air3-avatar[^"]*"',
            r'aria-label="[^"]*([^"]+)"[^>]*data-test="[^"]*MessageButton"',
            r'aria-label="Shortlist ([^"]+)"',
            r'aria-label="Archive ([^"]+)"'
        ]
        
        for pattern in name_patterns:
            name_match = re.search(pattern, chunk)
            if name_match:
                name = name_match.group(1).strip()
                if name and len(name) > 2 and not name.startswith('$') and not name.isdigit():
                    return name
        
        # Fallback to position-based name
        return f"Applicant {position}"
    
    def extract_perfected_title(self, chunk: str) -> str:
        """Extract PERFECTED title from chunk"""
        title_patterns = [
            r'id="air3-line-clamp-\d+"[^>]*>([^<]+)</div>',
            r'class="air3-line-clamp[^"]*"[^>]*>([^<]+)</div>',
            r'class="air3-line-clamp-wrapper[^"]*"[^>]*>.*?<div[^>]*>([^<]+)</div>'
        ]
        
        for pattern in title_patterns:
            title_match = re.search(pattern, chunk)
            if title_match:
                title = title_match.group(1).strip()
                if title and len(title) > 5:
                    return title
        
        return "Professional title not specified"
    
    def extract_perfected_location(self, chunk: str) -> str:
        """Extract PERFECTED location from chunk"""
        location_patterns = [
            r'class="font-weight-base[^"]*"[^>]*>([^<]+)</div>',
            r'text-light-on-inverse[^>]*>([^<]+)</div>',
            r'class="[^"]*text-light[^"]*"[^>]*>([^<]+)</div>'
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, chunk)
            if location_match:
                location = location_match.group(1).strip()
                if location and len(location) > 2 and not location.isdigit() and not location.startswith('$'):
                    return location
        
        return "Location not specified"
    
    def extract_perfected_skills(self, chunk: str) -> List[str]:
        """Extract PERFECTED skills list"""
        skills = []
        
        # Look for skills in the skill tokens
        skill_patterns = [
            r'<li[^>]*class="[^"]*air3-token[^"]*"[^>]*>\s*<span[^>]*>\s*([^<]+)\s*</span>',
            r'<span[^>]*class="[^"]*ellipsis[^"]*"[^>]*>\s*([^<]+)\s*</span>'
        ]
        
        for pattern in skill_patterns:
            skill_matches = re.findall(pattern, chunk)
            for skill in skill_matches:
                skill_text = skill.strip()
                if (skill_text and len(skill_text) > 2 and 
                    not skill_text.isdigit() and 
                    skill_text not in skills and
                    not skill_text.startswith('+') and
                    skill_text not in ['Best match', 'NEW', 'Shortlist', 'Archive'] and
                    not skill_text.startswith('$')):
                    skills.append(skill_text)
        
        # Remove duplicates and limit
        skills = list(dict.fromkeys(skills))[:15]
        return skills
    
    def extract_perfected_proposal(self, chunk: str) -> str:
        """Extract PERFECTED proposal text"""
        proposal_patterns = [
            r'Cover letter[^<]*<span[^>]*>([^<]+)</span>',
            r'class="air3-line-clamp[^"]*"[^>]*>\s*<span[^>]*>([^<]+)</span>',
            r'id="air3-line-clamp-\d+"[^>]*>\s*<span[^>]*>([^<]+)</span>'
        ]
        
        for pattern in proposal_patterns:
            proposal_match = re.search(pattern, chunk)
            if proposal_match:
                proposal = proposal_match.group(1).strip()
                if proposal and len(proposal) > 20:
                    return proposal[:1000] + "..." if len(proposal) > 1000 else proposal
        
        return "Proposal text not available"
    
    def extract_perfected_portfolio_links(self, chunk: str) -> List[str]:
        """Extract PERFECTED portfolio and work links"""
        links = []
        
        # Look for various link patterns
        link_patterns = [
            r'https://[^\s<>"]+',
            r'www\.[^\s<>"]+',
            r'figma\.com[^\s<>"]*',
            r'behance\.net[^\s<>"]*',
            r'dribbble\.com[^\s<>"]*',
            r'github\.com[^\s<>"]*',
            r'linkedin\.com[^\s<>"]*'
        ]
        
        for pattern in link_patterns:
            link_matches = re.findall(pattern, chunk)
            for link in link_matches:
                if link not in links and len(link) > 10 and not link.endswith('.js') and not link.endswith('.css'):
                    links.append(link)
        
        return links[:5]  # Limit to 5 links
    
    def calculate_perfected_rating(self, rate_match, success_match, hours_match, jobs_match, skills: List[str], job_type: str) -> float:
        """Calculate PERFECTED rating based on multiple factors"""
        rating = 0.0
        
        # Job success rate (0-100) - 25% weight
        if success_match:
            try:
                success_rate = float(success_match.group(1))
                rating += (success_rate / 100) * 1.25
            except:
                pass
        
        # Hours worked (experience) - 20% weight
        if hours_match:
            try:
                hours = float(hours_match.group(1))
                if hours > 2000:
                    rating += 1.0
                elif hours > 1000:
                    rating += 0.8
                elif hours > 500:
                    rating += 0.6
                elif hours > 100:
                    rating += 0.4
            except:
                pass
        
        # Jobs completed - 15% weight
        if jobs_match:
            try:
                jobs = float(jobs_match.group(1))
                if jobs > 100:
                    rating += 0.75
                elif jobs > 50:
                    rating += 0.6
                elif jobs > 20:
                    rating += 0.45
                elif jobs > 5:
                    rating += 0.3
            except:
                pass
        
        # Skills match - 25% weight
        job_keywords = self.jobs[job_type]["keywords"]
        skill_matches = sum(1 for skill in skills if any(keyword.lower() in skill.lower() for keyword in job_keywords))
        rating += min(skill_matches * 0.25, 1.25)  # Max 1.25 points
        
        # Hourly rate (reasonable range) - 15% weight
        if rate_match:
            try:
                rate = float(rate_match.group(1))
                if 25 <= rate <= 75:  # Sweet spot
                    rating += 0.75
                elif 15 <= rate <= 100:  # Acceptable range
                    rating += 0.45
                elif rate < 15:  # Too low
                    rating += 0.2
            except:
                pass
        
        return min(rating, 5.0)  # Cap at 5.0
    
    def calculate_data_quality_score(self, rate_match, success_match, hours_match, jobs_match, skills: List[str], proposal: str) -> float:
        """Calculate data quality score (0-1)"""
        score = 0.0
        total_fields = 6
        
        if rate_match:
            score += 1.0
        if success_match:
            score += 1.0
        if hours_match:
            score += 1.0
        if jobs_match:
            score += 1.0
        if skills and len(skills) > 0:
            score += 1.0
        if proposal and len(proposal) > 20:
            score += 1.0
        
        return score / total_fields
    
    def calculate_perfected_ranking_score(self, applicant: Dict, job_type: str) -> float:
        """Calculate PERFECTED ranking score"""
        score = 0.0
        job_config = self.jobs[job_type]
        
        # Job success rate (25% weight)
        if applicant.get("job_success") != "Success rate not specified":
            try:
                success_rate = float(re.search(r'(\d+)', applicant["job_success"]).group(1))
                score += (success_rate / 100) * 0.25
            except:
                pass
        
        # Hours worked (20% weight)
        if applicant.get("hours_worked") != "Hours not specified":
            try:
                hours = float(re.search(r'(\d+)', applicant["hours_worked"]).group(1))
                score += min(hours / 10000, 1.0) * 0.2
            except:
                pass
        
        # Jobs completed (15% weight)
        if applicant.get("jobs_completed") != "Jobs not specified":
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
        
        # Hourly rate (15% weight)
        if applicant.get("hourly_rate") != "Rate not specified":
            try:
                rate = float(re.search(r'(\d+)', applicant["hourly_rate"]).group(1))
                if 25 <= rate <= 75:  # Sweet spot
                    score += 0.15
                elif 15 <= rate <= 100:  # Acceptable range
                    score += 0.1
                elif rate < 15:  # Too low
                    score += 0.05
            except:
                pass
        
        return min(score * 5.0, 5.0)  # Scale to 0-5
    
    def rank_applicants_perfected(self, applicants: List[Dict], job_type: str) -> List[Dict]:
        """Rank applicants with PERFECTED scoring"""
        print(f"🏆 Perfected ranking of {len(applicants)} applicants...")
        
        for applicant in applicants:
            applicant["ranking_score"] = self.calculate_perfected_ranking_score(applicant, job_type)
            applicant["is_rated"] = True
        
        # Sort by ranking score (descending)
        ranked_applicants = sorted(applicants, key=lambda x: x["ranking_score"], reverse=True)
        
        # Assign ranks
        for i, applicant in enumerate(ranked_applicants):
            applicant["rank"] = i + 1
        
        print(f"✅ Perfected ranking complete!")
        print(f"  ✅ Ranked {len(ranked_applicants)} applicants")
        print(f"  🏆 Top 5 ranked:")
        for i in range(min(5, len(ranked_applicants))):
            applicant = ranked_applicants[i]
            print(f"    {i+1}. {applicant['name']} - Score: {applicant['ranking_score']:.2f} - Rate: {applicant['hourly_rate']}")
        
        return ranked_applicants
    
    def process_all_candidates_perfected(self):
        """Process ALL candidates with PERFECTED data extraction"""
        print("🎯 Final Perfected Candidate Processing System")
        print("=" * 70)
        print("🚀 Starting PERFECTED processing of ALL candidates")
        print("=" * 70)
        
        all_applicants = []
        job_results = {}
        
        for job_type, job_config in self.jobs.items():
            print(f"\n📋 Processing {job_config['title']} with PERFECTED extraction...")
            
            html_file = os.path.join(self.downloads_dir, job_config['filename'])
            if not os.path.exists(html_file):
                print(f"❌ HTML file not found: {html_file}")
                continue
            
            # Extract perfected applicant data
            applicants = self.extract_perfected_applicant_data(html_file, job_type)
            
            if applicants:
                # Rank applicants with perfected scoring
                ranked_applicants = self.rank_applicants_perfected(applicants, job_type)
                
                # Save job-specific results
                job_results[job_type] = ranked_applicants
                all_applicants.extend(ranked_applicants)
                
                # Save individual job results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                job_filename = f"perfected_ranked_applicants_{job_type}_{timestamp}.json"
                job_path = os.path.join(self.output_dir, job_filename)
                
                with open(job_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "job_type": job_type,
                        "job_title": self.jobs[job_type]["title"],
                        "total_applicants": len(ranked_applicants),
                        "timestamp": timestamp,
                        "processing_method": "perfected_extraction",
                        "applicants": ranked_applicants
                    }, f, indent=2, ensure_ascii=False)
                
                print(f"  ✅ Saved perfected {job_type} rankings to {job_path}")
        
        # Save combined results
        if all_applicants:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            combined_filename = f"perfected_all_applicants_{timestamp}.json"
            combined_path = os.path.join(self.output_dir, combined_filename)
            
            with open(combined_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_applicants": len(all_applicants),
                    "jobs_processed": list(self.jobs.keys()),
                    "timestamp": timestamp,
                    "processing_method": "perfected_extraction",
                    "data_quality_summary": self.calculate_overall_data_quality(all_applicants),
                    "applicants": all_applicants
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saving perfected results...")
            print(f"  ✅ Saved perfected rankings to {combined_path}")
            
            # Update frontend data
            frontend_path = "nextjs-app/data/candidates.json"
            with open(frontend_path, 'w', encoding='utf-8') as f:
                json.dump(all_applicants, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Updated frontend data with {len(all_applicants)} perfected applicants")
        
        print("\n" + "=" * 70)
        print("🎉 PERFECTED PROCESSING COMPLETE!")
        print("=" * 70)
        
        for job_type, applicants in job_results.items():
            print(f"\n📊 {self.jobs[job_type]['title']}:")
            print(f"  📈 Total Applicants: {len(applicants)}")
            print(f"  🏆 Top 5 Ranked Applicants:")
            for i in range(min(5, len(applicants))):
                applicant = applicants[i]
                print(f"    {i+1}. {applicant['name']} - Score: {applicant['ranking_score']:.2f} - Rate: {applicant['hourly_rate']}")
        
        print(f"\n✨ All done! Perfected processing of {len(all_applicants)} total applicants.")
    
    def calculate_overall_data_quality(self, applicants: List[Dict]) -> Dict:
        """Calculate overall data quality metrics"""
        total_applicants = len(applicants)
        if total_applicants == 0:
            return {}
        
        quality_scores = [app.get("data_quality_score", 0) for app in applicants]
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        complete_profiles = sum(1 for app in applicants if app.get("data_quality_score", 0) > 0.8)
        partial_profiles = sum(1 for app in applicants if 0.4 <= app.get("data_quality_score", 0) <= 0.8)
        incomplete_profiles = sum(1 for app in applicants if app.get("data_quality_score", 0) < 0.4)
        
        return {
            "average_quality_score": round(avg_quality, 2),
            "complete_profiles": complete_profiles,
            "partial_profiles": partial_profiles,
            "incomplete_profiles": incomplete_profiles,
            "total_applicants": total_applicants
        }

def main():
    extractor = FinalPerfectedExtractor()
    extractor.process_all_candidates_perfected()

if __name__ == "__main__":
    main()
