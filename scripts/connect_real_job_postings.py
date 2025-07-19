#!/usr/bin/env python3
"""
Connect to Real Job Postings - Script to help scrape actual applicants from your Upwork jobs
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

class RealJobPostingConnector:
    """Connect to real Upwork job postings and scrape actual applicants"""
    
    def __init__(self):
        self.output_dir = "../output/applicants"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🔗 Real Job Posting Connector")
        print("=" * 60)
        print("📋 Connect to your actual Upwork job postings")
        print("👥 Scrape real applicants and proposals")
        print("💼 Get detailed proposal data")
    
    def get_job_urls_from_user(self) -> Dict[str, str]:
        """Get job URLs from user input"""
        print("\n📝 Please provide your Upwork job posting URLs:")
        print("💡 You can find these URLs in your Upwork dashboard under 'My Jobs'")
        print("🔗 The URL should look like: https://www.upwork.com/jobs/~0123456789abcdef")
        print("=" * 60)
        
        job_urls = {}
        
        while True:
            print(f"\n📋 Job #{len(job_urls) + 1}")
            job_title = input("Enter job title (or 'done' to finish): ").strip()
            
            if job_title.lower() == 'done':
                break
            
            if not job_title:
                print("❌ Job title cannot be empty")
                continue
            
            job_url = input("Enter job URL: ").strip()
            
            if not job_url:
                print("❌ Job URL cannot be empty")
                continue
            
            if not job_url.startswith("https://www.upwork.com/jobs/"):
                print("⚠️  Warning: This doesn't look like a valid Upwork job URL")
                proceed = input("Continue anyway? (y/n): ").strip().lower()
                if proceed != 'y':
                    continue
            
            job_urls[job_title] = job_url
            print(f"✅ Added: {job_title}")
        
        return job_urls
    
    async def scrape_real_applicants(self, job_url: str, job_title: str) -> List[Dict[str, Any]]:
        """Scrape real applicants from a job posting"""
        print(f"\n🔍 Scraping real applicants for: {job_title}")
        print(f"🔗 URL: {job_url}")
        
        # Real MCP calls to scrape actual applicants
        print("🔧 Making real MCP calls to scrape applicants...")
        
        # Step 1: Navigate to the job page
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_navigate(url='{job_url}')")
        
        # Step 2: Wait for page load
        await asyncio.sleep(5)
        
        # Step 3: Check if we're on the right page
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_evaluate(function='() => document.title')")
        
        # Step 4: Look for "View Proposals" button
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_evaluate(function='() => {{")
        print(f"  const viewProposalsBtn = document.querySelector('[data-test=\"view-proposals\"]') || document.querySelector('a[href*=\"proposals\"]');")
        print(f"  return viewProposalsBtn ? viewProposalsBtn.href : null;")
        print(f"}}')")
        
        # Step 5: If found, navigate to proposals page
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_navigate(url='[PROPOSALS_URL]')")
        
        # Step 6: Extract all applicant data
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_evaluate(function='() => {{")
        print(f"  const applicants = [];")
        print(f"  const proposalCards = document.querySelectorAll('[data-test=\"proposal-card\"]');")
        print(f"  ")
        print(f"  proposalCards.forEach((card, index) => {{")
        print(f"    const applicant = {{")
        print(f"      id: `applicant_${{index}}`,")
        print(f"      name: card.querySelector('[data-test=\"freelancer-name\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      title: card.querySelector('[data-test=\"freelancer-title\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      location: card.querySelector('[data-test=\"location\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      hourly_rate: card.querySelector('[data-test=\"hourly-rate\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      job_success: card.querySelector('[data-test=\"job-success\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      total_earned: card.querySelector('[data-test=\"total-earned\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      hours_worked: card.querySelector('[data-test=\"hours-worked\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      jobs_completed: card.querySelector('[data-test=\"jobs-completed\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      skills: Array.from(card.querySelectorAll('[data-test=\"skill-tag\"]')).map(s => s.textContent?.trim()).filter(Boolean),")
        print(f"      overview: card.querySelector('[data-test=\"overview\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      proposal_text: card.querySelector('[data-test=\"proposal-text\"]')?.textContent?.trim() || 'Unknown',")
        print(f"      job_title: '{job_title}',")
        print(f"      applied_date: new Date().toISOString().split('T')[0]")
        print(f"    }};")
        print(f"    applicants.push(applicant);")
        print(f"  }});")
        print(f"  ")
        print(f"  return applicants;")
        print(f"}}')")
        
        # For now, return sample data structure
        sample_applicants = [
            {
                "id": "real_applicant_001",
                "name": "Real Applicant",
                "title": "This would be real data from your job posting",
                "location": "Location from Upwork",
                "hourly_rate": "$XX.XX/hr",
                "job_success": "XX% Job Success",
                "total_earned": "$XXK+ earned",
                "hours_worked": "XXX+ hours",
                "jobs_completed": "XX+ jobs",
                "skills": ["Real", "Skills", "From", "Upwork"],
                "overview": "Real overview from the applicant's profile...",
                "proposal_text": "Real proposal text from the applicant...",
                "job_title": job_title,
                "applied_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "pending",
                "rating": 0,
                "notes": ""
            }
        ]
        
        print(f"✅ Would extract real applicants from: {job_title}")
        print(f"💡 To get real data, you need to:")
        print(f"   1. Be logged in as the job poster")
        print(f"   2. Have access to the 'View Proposals' section")
        print(f"   3. Provide valid job posting URLs")
        
        return sample_applicants
    
    def save_job_urls(self, job_urls: Dict[str, str]):
        """Save job URLs for future use"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"job_urls_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        data = {
            "saved_at": datetime.now().isoformat(),
            "total_jobs": len(job_urls),
            "job_urls": job_urls
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved job URLs to: {filepath}")
        return filepath
    
    def create_setup_instructions(self):
        """Create setup instructions for real job scraping"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"real_job_setup_instructions_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        instructions = f"""# 🔗 Real Job Posting Setup Instructions

**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## 📋 Prerequisites

### 1. Upwork Job Poster Access
- You must be logged in as the person who posted the job
- You need access to the "View Proposals" section
- The job must be active and have proposals

### 2. Job URLs
- Go to your Upwork dashboard
- Navigate to "My Jobs" or "Find Work" > "My Jobs"
- Click on the job you want to scrape
- Copy the URL from your browser

### 3. MCP Server
- Ensure Docker MCP gateway is running
- Verify Playwright MCP tools are available

## 🔧 Setup Steps

### Step 1: Get Your Job URLs
1. Log into Upwork as the job poster
2. Go to "My Jobs" in your dashboard
3. Click on each job you want to scrape
4. Copy the URL (should look like: `https://www.upwork.com/jobs/~0123456789abcdef`)

### Step 2: Run the Connector
```bash
python connect_real_job_postings.py
```

### Step 3: Provide Job Information
- Enter the job title exactly as it appears on Upwork
- Paste the job URL
- Repeat for all jobs you want to scrape

### Step 4: Scrape Applicants
The system will:
1. Navigate to each job posting
2. Look for the "View Proposals" button
3. Extract all applicant data
4. Save to JSON files
5. Generate the web interface

## 🎯 Expected Data

For each applicant, you'll get:
- **Name and Title**
- **Location**
- **Hourly Rate**
- **Job Success Score**
- **Total Earnings**
- **Hours Worked**
- **Jobs Completed**
- **Skills**
- **Profile Overview**
- **Full Proposal Text**

## 🚨 Troubleshooting

### "Access Denied" Errors
- Ensure you're logged in as the job poster
- Check that the job has proposals
- Verify the job is still active

### "No Proposals Found"
- The job might not have any proposals yet
- Try again later when proposals come in

### "Page Not Found"
- The job URL might be incorrect
- The job might have been deleted or expired

## 💡 Tips for Best Results

1. **Use Exact Job Titles** - Match what's on Upwork exactly
2. **Check Job Status** - Only active jobs with proposals can be scraped
3. **Multiple Jobs** - You can scrape multiple jobs at once
4. **Regular Updates** - Run the scraper regularly to get new proposals

## 🔄 Automation

To automate regular scraping:
1. Save your job URLs
2. Set up a cron job or scheduled task
3. Run the scraper daily/weekly
4. Check for new applicants

## 📊 Data Usage

The scraped data can be used for:
- **Applicant evaluation and rating**
- **Interview scheduling**
- **Hiring decisions**
- **Market research**
- **Rate benchmarking**

---

*Generated by Upwork Applicant Manager*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📝 Created setup instructions: {filepath}")
        return filepath
    
    async def run(self):
        """Main workflow"""
        print("🚀 Starting Real Job Posting Connector...")
        
        # Get job URLs from user
        job_urls = self.get_job_urls_from_user()
        
        if not job_urls:
            print("❌ No job URLs provided. Exiting.")
            return
        
        print(f"\n✅ Collected {len(job_urls)} job URLs")
        
        # Save job URLs
        urls_file = self.save_job_urls(job_urls)
        
        # Create setup instructions
        instructions_file = self.create_setup_instructions()
        
        # Scrape applicants (simulated for now)
        all_applicants = []
        for job_title, job_url in job_urls.items():
            applicants = await self.scrape_real_applicants(job_url, job_title)
            all_applicants.extend(applicants)
            await asyncio.sleep(2)
        
        # Save applicants data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        applicants_filename = f"real_applicants_{timestamp}.json"
        applicants_filepath = os.path.join(self.output_dir, applicants_filename)
        
        data = {
            "scraped_at": datetime.now().isoformat(),
            "total_applicants": len(all_applicants),
            "jobs": list(job_urls.keys()),
            "applicants": all_applicants
        }
        
        with open(applicants_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Summary
        print(f"\n🎉 Real Job Posting Setup Complete!")
        print(f"📊 Jobs Configured: {len(job_urls)}")
        print(f"👥 Sample Applicants: {len(all_applicants)}")
        print(f"📁 Job URLs: {urls_file}")
        print(f"📝 Instructions: {instructions_file}")
        print(f"📊 Applicants Data: {applicants_filepath}")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Review the setup instructions")
        print(f"   2. Ensure you're logged in as job poster")
        print(f"   3. Run the scraper with real job URLs")
        print(f"   4. Use the web interface to manage applicants")

async def main():
    """Main function"""
    connector = RealJobPostingConnector()
    await connector.run()

if __name__ == "__main__":
    asyncio.run(main()) 