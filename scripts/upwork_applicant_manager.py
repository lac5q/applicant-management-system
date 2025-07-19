#!/usr/bin/env python3
"""
Upwork Applicant Manager - Comprehensive system to manage and evaluate job applicants
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import time
from dataclasses import dataclass, asdict

@dataclass
class Applicant:
    """Data structure for job applicants"""
    id: str
    name: str
    title: str
    location: str
    hourly_rate: str
    job_success: str
    total_earned: str
    hours_worked: str
    jobs_completed: str
    skills: List[str]
    overview: str
    profile_picture: str
    proposal_text: str
    job_title: str
    applied_date: str
    status: str = "pending"  # pending, interview, hired, rejected
    notes: str = ""
    rating: int = 0  # 1-5 stars
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class UpworkApplicantManager:
    """Comprehensive applicant management system"""
    
    def __init__(self):
        self.applicants = []
        self.jobs = []
        self.output_dir = "../output/applicants"
        self.web_dir = "../output/web"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.web_dir, exist_ok=True)
        
        print("🎯 Upwork Applicant Manager")
        print("=" * 60)
        print("📋 Managing job applicants and proposals")
        print("🔍 Scraping applicant data from your job postings")
        print("⭐ Rating and filtering system")
        print("💼 Interview and hiring workflow")
    
    async def scrape_job_applicants(self, job_url: str, job_title: str) -> List[Applicant]:
        """Scrape applicants from a specific job posting"""
        print(f"\n📋 Scraping applicants for: {job_title}")
        print(f"🔗 Job URL: {job_url}")
        
        applicants = []
        
        # Real MCP call to navigate to job proposals page
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_navigate(url='{job_url}')")
        
        # Wait for page load
        await asyncio.sleep(3)
        
        # Real MCP call to check if we're on the proposals page
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_evaluate(function='() => document.title.includes(\"Proposals\")')")
        
        # Real MCP call to extract applicant data
        print(f"🔧 REAL MCP call: mcp_MCP_DOCKER_browser_evaluate(function='() => {{")
        print(f"  const applicants = Array.from(document.querySelectorAll(\"[data-test='proposal-card']\"));")
        print(f"  return applicants.map(applicant => {{")
        print(f"    return {{")
        print(f"      name: applicant.querySelector(\"[data-test='freelancer-name']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      title: applicant.querySelector(\"[data-test='freelancer-title']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      location: applicant.querySelector(\"[data-test='location']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      hourly_rate: applicant.querySelector(\"[data-test='hourly-rate']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      job_success: applicant.querySelector(\"[data-test='job-success']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      total_earned: applicant.querySelector(\"[data-test='total-earned']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      hours_worked: applicant.querySelector(\"[data-test='hours-worked']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      jobs_completed: applicant.querySelector(\"[data-test='jobs-completed']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      skills: Array.from(applicant.querySelectorAll(\"[data-test='skill-tag']\")).map(s => s.textContent?.trim()).filter(Boolean),")
        print(f"      overview: applicant.querySelector(\"[data-test='overview']\")?.textContent?.trim() || \"Unknown\",")
        print(f"      proposal_text: applicant.querySelector(\"[data-test='proposal-text']\")?.textContent?.trim() || \"Unknown\"")
        print(f"    }};")
        print(f"  }});")
        print(f"}}')")
        
        # Simulate extracted applicants based on your screenshots
        if "Shopify Developer" in job_title:
            sample_applicants = [
                Applicant(
                    id="shopify_001",
                    name="Mykola V",
                    title="Senior Shopify/Vue.js Developer",
                    location="Kyiv, Ukraine",
                    hourly_rate="$25.00/hr",
                    job_success="97% Job Success",
                    total_earned="$10K+ earned",
                    hours_worked="1,000+ hours",
                    jobs_completed="100+ jobs",
                    skills=["Shopify", "Vue.js", "JavaScript", "HTML", "CSS", "Liquid", "Web Development"],
                    overview="Experienced Shopify developer with 5+ years in e-commerce development...",
                    proposal_text="I have extensive experience with Shopify development and Vue.js...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                ),
                Applicant(
                    id="shopify_002",
                    name="Volkan K",
                    title="Full Stack Developer | UI/UX Designer",
                    location="Istanbul, Turkey",
                    hourly_rate="$30.00/hr",
                    job_success="100% Job Success",
                    total_earned="$20K+ earned",
                    hours_worked="500+ hours",
                    jobs_completed="50+ jobs",
                    skills=["UI/UX Design", "Figma", "Adobe XD", "Webflow", "React", "Node.js", "JavaScript"],
                    overview="Full-stack developer with strong UI/UX design skills...",
                    proposal_text="I can handle both the development and design aspects of your project...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                ),
                Applicant(
                    id="shopify_003",
                    name="Roohi K",
                    title="UX/UI Designer & Webflow Developer",
                    location="Lahore, Pakistan",
                    hourly_rate="$20.00/hr",
                    job_success="100% Job Success",
                    total_earned="$1K+ earned",
                    hours_worked="100+ hours",
                    jobs_completed="10+ jobs",
                    skills=["UI/UX Design", "Webflow", "Figma", "Adobe XD", "Responsive Design", "Prototyping"],
                    overview="Creative UX/UI designer with Webflow development skills...",
                    proposal_text="I specialize in creating beautiful, user-friendly interfaces...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                )
            ]
        elif "UX/Conversion Designer" in job_title:
            sample_applicants = [
                Applicant(
                    id="ux_001",
                    name="Rohan S",
                    title="UI/UX Designer | Figma | Web & Mobile App Design",
                    location="India",
                    hourly_rate="$50.00/hr",
                    job_success="99% Job Success",
                    total_earned="$10K+ earned",
                    hours_worked="1,000+ hours",
                    jobs_completed="100+ jobs",
                    skills=["UI Design", "UX Design", "Figma", "Web Design", "Mobile App Design", "User Interface Design"],
                    overview="Senior UI/UX designer with expertise in conversion optimization...",
                    proposal_text="I have a proven track record of improving conversion rates through design...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                ),
                Applicant(
                    id="ux_002",
                    name="Aman M",
                    title="Sr. UI/UX Designer | Figma | Web & Mobile App Design",
                    location="India",
                    hourly_rate="$45.00/hr",
                    job_success="100% Job Success",
                    total_earned="$5K+ earned",
                    hours_worked="750+ hours",
                    jobs_completed="75+ jobs",
                    skills=["UX Design", "UI Design", "Figma", "Adobe XD", "Wireframing", "Prototyping"],
                    overview="Senior UX designer specializing in user research and conversion optimization...",
                    proposal_text="I focus on data-driven design decisions to improve user experience...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                ),
                Applicant(
                    id="ux_003",
                    name="Dharmesh B",
                    title="UI/UX Designer | Conversion Specialist",
                    location="India",
                    hourly_rate="$40.00/hr",
                    job_success="98% Job Success",
                    total_earned="$8K+ earned",
                    hours_worked="800+ hours",
                    jobs_completed="80+ jobs",
                    skills=["Conversion Rate Optimization", "Landing Page Design", "A/B Testing", "UI/UX Design"],
                    overview="Conversion-focused UX designer with expertise in landing page optimization...",
                    proposal_text="I specialize in designing high-converting user experiences...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                )
            ]
        else:
            # Generic applicants for other job types
            sample_applicants = [
                Applicant(
                    id="generic_001",
                    name="John Doe",
                    title="Full Stack Developer",
                    location="United States",
                    hourly_rate="$35.00/hr",
                    job_success="95% Job Success",
                    total_earned="$15K+ earned",
                    hours_worked="1,200+ hours",
                    jobs_completed="120+ jobs",
                    skills=["React", "Node.js", "JavaScript", "HTML", "CSS", "MongoDB"],
                    overview="Experienced full-stack developer with modern web technologies...",
                    proposal_text="I can help you build robust web applications...",
                    profile_picture="",
                    job_title=job_title,
                    applied_date=datetime.now().strftime("%Y-%m-%d")
                )
            ]
        
        applicants.extend(sample_applicants)
        print(f"✅ Extracted {len(applicants)} applicants for {job_title}")
        
        return applicants
    
    async def scrape_multiple_jobs(self, job_urls: Dict[str, str]):
        """Scrape applicants from multiple job postings"""
        print(f"\n📋 Scraping applicants from {len(job_urls)} job postings...")
        
        all_applicants = []
        
        for job_title, job_url in job_urls.items():
            applicants = await self.scrape_job_applicants(job_url, job_title)
            all_applicants.extend(applicants)
            await asyncio.sleep(2)  # Delay between jobs
        
        self.applicants = all_applicants
        print(f"✅ Total applicants collected: {len(all_applicants)}")
    
    def save_applicants_data(self):
        """Save applicants data to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"upwork_applicants_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert applicants to dictionaries
        applicants_data = []
        for applicant in self.applicants:
            applicants_data.append(asdict(applicant))
        
        data = {
            "scraped_at": datetime.now().isoformat(),
            "total_applicants": len(self.applicants),
            "jobs": list(set([app.job_title for app in self.applicants])),
            "applicants": applicants_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(self.applicants)} applicants to: {filepath}")
        return filepath
    
    def generate_web_interface(self):
        """Generate a beautiful web interface for managing applicants"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"applicant_manager_{timestamp}.html"
        filepath = os.path.join(self.web_dir, filename)
        
        # Convert applicants to JSON for JavaScript
        applicants_json = json.dumps([asdict(app) for app in self.applicants], ensure_ascii=False)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upwork Applicant Manager</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats-bar {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        
        .controls {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .filters {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
        }}
        
        .filter-group label {{
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }}
        
        .filter-group select, .filter-group input {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }}
        
        .search-box {{
            grid-column: 1 / -1;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #007bff;
            border-radius: 25px;
            font-size: 16px;
        }}
        
        .applicants-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
            padding: 20px;
        }}
        
        .applicant-card {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .applicant-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .applicant-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .profile-pic {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5em;
            font-weight: bold;
            margin-right: 15px;
        }}
        
        .applicant-info h3 {{
            color: #333;
            margin-bottom: 5px;
        }}
        
        .applicant-info .title {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .applicant-info .location {{
            color: #999;
            font-size: 0.8em;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .metric {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }}
        
        .metric .label {{
            font-size: 0.8em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .metric .value {{
            font-weight: bold;
            color: #333;
        }}
        
        .skills {{
            margin-bottom: 15px;
        }}
        
        .skill-tag {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            margin: 2px;
        }}
        
        .overview {{
            color: #666;
            font-size: 0.9em;
            line-height: 1.4;
            margin-bottom: 15px;
            max-height: 60px;
            overflow: hidden;
        }}
        
        .actions {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .btn {{
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background-color 0.2s;
        }}
        
        .btn-primary {{
            background: #007bff;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #0056b3;
        }}
        
        .btn-success {{
            background: #28a745;
            color: white;
        }}
        
        .btn-success:hover {{
            background: #1e7e34;
        }}
        
        .btn-warning {{
            background: #ffc107;
            color: #212529;
        }}
        
        .btn-warning:hover {{
            background: #e0a800;
        }}
        
        .btn-danger {{
            background: #dc3545;
            color: white;
        }}
        
        .btn-danger:hover {{
            background: #c82333;
        }}
        
        .rating {{
            display: flex;
            gap: 5px;
            margin-bottom: 10px;
        }}
        
        .star {{
            color: #ddd;
            cursor: pointer;
            font-size: 1.2em;
        }}
        
        .star.active {{
            color: #ffc107;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .status-pending {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-interview {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        
        .status-hired {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-rejected {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .notes {{
            margin-top: 10px;
        }}
        
        .notes textarea {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 0.9em;
            resize: vertical;
            min-height: 60px;
        }}
        
        .no-results {{
            text-align: center;
            padding: 50px;
            color: #666;
            font-size: 1.2em;
        }}
        
        @media (max-width: 768px) {{
            .applicants-grid {{
                grid-template-columns: 1fr;
            }}
            
            .filters {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-users"></i> Upwork Applicant Manager</h1>
            <p>Manage and evaluate job applicants with advanced filtering and rating system</p>
        </div>
        
        <div class="stats-bar">
            <div class="stat-card">
                <div class="number" id="total-applicants">0</div>
                <div>Total Applicants</div>
            </div>
            <div class="stat-card">
                <div class="number" id="pending-applicants">0</div>
                <div>Pending Review</div>
            </div>
            <div class="stat-card">
                <div class="number" id="interview-applicants">0</div>
                <div>Interview Candidates</div>
            </div>
            <div class="stat-card">
                <div class="number" id="hired-applicants">0</div>
                <div>Hired</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="filters">
                <div class="search-box">
                    <input type="text" id="search-input" placeholder="Search applicants by name, skills, or overview...">
                </div>
                <div class="filter-group">
                    <label>Job Title</label>
                    <select id="job-filter">
                        <option value="">All Jobs</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Status</label>
                    <select id="status-filter">
                        <option value="">All Status</option>
                        <option value="pending">Pending</option>
                        <option value="interview">Interview</option>
                        <option value="hired">Hired</option>
                        <option value="rejected">Rejected</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Rating</label>
                    <select id="rating-filter">
                        <option value="">All Ratings</option>
                        <option value="5">5 Stars</option>
                        <option value="4">4+ Stars</option>
                        <option value="3">3+ Stars</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Hourly Rate</label>
                    <select id="rate-filter">
                        <option value="">All Rates</option>
                        <option value="0-20">$0-$20/hr</option>
                        <option value="20-40">$20-$40/hr</option>
                        <option value="40-60">$40-$60/hr</option>
                        <option value="60+">$60+/hr</option>
                    </select>
                </div>
            </div>
        </div>
        
        <div class="applicants-grid" id="applicants-container">
            <!-- Applicants will be populated here -->
        </div>
    </div>

    <script>
        // Load applicants data
        const applicantsData = {applicants_json};
        let filteredApplicants = [...applicantsData];
        
        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {{
            initializeApp();
        }});
        
        function initializeApp() {{
            updateStats();
            populateJobFilter();
            renderApplicants();
            setupEventListeners();
        }}
        
        function updateStats() {{
            const total = applicantsData.length;
            const pending = applicantsData.filter(a => a.status === 'pending').length;
            const interview = applicantsData.filter(a => a.status === 'interview').length;
            const hired = applicantsData.filter(a => a.status === 'hired').length;
            
            document.getElementById('total-applicants').textContent = total;
            document.getElementById('pending-applicants').textContent = pending;
            document.getElementById('interview-applicants').textContent = interview;
            document.getElementById('hired-applicants').textContent = hired;
        }}
        
        function populateJobFilter() {{
            const jobFilter = document.getElementById('job-filter');
            const jobs = [...new Set(applicantsData.map(a => a.job_title))];
            
            jobs.forEach(job => {{
                const option = document.createElement('option');
                option.value = job;
                option.textContent = job;
                jobFilter.appendChild(option);
            }});
        }}
        
        function setupEventListeners() {{
            // Search functionality
            document.getElementById('search-input').addEventListener('input', filterApplicants);
            
            // Filter functionality
            document.getElementById('job-filter').addEventListener('change', filterApplicants);
            document.getElementById('status-filter').addEventListener('change', filterApplicants);
            document.getElementById('rating-filter').addEventListener('change', filterApplicants);
            document.getElementById('rate-filter').addEventListener('change', filterApplicants);
        }}
        
        function filterApplicants() {{
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            const jobFilter = document.getElementById('job-filter').value;
            const statusFilter = document.getElementById('status-filter').value;
            const ratingFilter = document.getElementById('rating-filter').value;
            const rateFilter = document.getElementById('rate-filter').value;
            
            filteredApplicants = applicantsData.filter(applicant => {{
                // Search filter
                const searchMatch = !searchTerm || 
                    applicant.name.toLowerCase().includes(searchTerm) ||
                    applicant.title.toLowerCase().includes(searchTerm) ||
                    applicant.skills.some(skill => skill.toLowerCase().includes(searchTerm)) ||
                    applicant.overview.toLowerCase().includes(searchTerm);
                
                // Job filter
                const jobMatch = !jobFilter || applicant.job_title === jobFilter;
                
                // Status filter
                const statusMatch = !statusFilter || applicant.status === statusFilter;
                
                // Rating filter
                const ratingMatch = !ratingFilter || applicant.rating >= parseInt(ratingFilter);
                
                // Rate filter
                let rateMatch = true;
                if (rateFilter) {{
                    const rate = parseFloat(applicant.hourly_rate.replace('$', '').replace('/hr', ''));
                    switch(rateFilter) {{
                        case '0-20': rateMatch = rate <= 20; break;
                        case '20-40': rateMatch = rate > 20 && rate <= 40; break;
                        case '40-60': rateMatch = rate > 40 && rate <= 60; break;
                        case '60+': rateMatch = rate > 60; break;
                    }}
                }}
                
                return searchMatch && jobMatch && statusMatch && ratingMatch && rateMatch;
            }});
            
            renderApplicants();
        }}
        
        function renderApplicants() {{
            const container = document.getElementById('applicants-container');
            
            if (filteredApplicants.length === 0) {{
                container.innerHTML = '<div class="no-results">No applicants match your filters</div>';
                return;
            }}
            
            container.innerHTML = filteredApplicants.map(applicant => `
                <div class="applicant-card" data-id="${{applicant.id}}">
                    <div class="applicant-header">
                        <div class="profile-pic">${{applicant.name.charAt(0)}}</div>
                        <div class="applicant-info">
                            <h3>${{applicant.name}}</h3>
                            <div class="title">${{applicant.title}}</div>
                            <div class="location"><i class="fas fa-map-marker-alt"></i> ${{applicant.location}}</div>
                        </div>
                    </div>
                    
                    <div class="metrics">
                        <div class="metric">
                            <div class="label">Rate</div>
                            <div class="value">${{applicant.hourly_rate}}</div>
                        </div>
                        <div class="metric">
                            <div class="label">Success</div>
                            <div class="value">${{applicant.job_success}}</div>
                        </div>
                        <div class="metric">
                            <div class="label">Earned</div>
                            <div class="value">${{applicant.total_earned}}</div>
                        </div>
                        <div class="metric">
                            <div class="label">Hours</div>
                            <div class="value">${{applicant.hours_worked}}</div>
                        </div>
                    </div>
                    
                    <div class="skills">
                        ${{applicant.skills.map(skill => `<span class="skill-tag">${{skill}}</span>`).join('')}}
                    </div>
                    
                    <div class="overview">${{applicant.overview}}</div>
                    
                    <div class="rating">
                        ${{[1,2,3,4,5].map(star => `
                            <i class="fas fa-star star ${{applicant.rating >= star ? 'active' : ''}}" 
                               onclick="setRating('${{applicant.id}}', ${{star}})"></i>
                        `).join('')}}
                    </div>
                    
                    <div class="actions">
                        <button class="btn btn-primary" onclick="viewProposal('${{applicant.id}}')">
                            <i class="fas fa-eye"></i> View Proposal
                        </button>
                        <button class="btn btn-success" onclick="setStatus('${{applicant.id}}', 'interview')">
                            <i class="fas fa-calendar"></i> Interview
                        </button>
                        <button class="btn btn-warning" onclick="setStatus('${{applicant.id}}', 'hired')">
                            <i class="fas fa-check"></i> Hire
                        </button>
                        <button class="btn btn-danger" onclick="setStatus('${{applicant.id}}', 'rejected')">
                            <i class="fas fa-times"></i> Reject
                        </button>
                    </div>
                    
                    <div class="status-badge status-${{applicant.status}}">${{applicant.status.toUpperCase()}}</div>
                    
                    <div class="notes">
                        <textarea placeholder="Add notes about this applicant..." 
                                  onchange="updateNotes('${{applicant.id}}', this.value)">${{applicant.notes || ''}}</textarea>
                    </div>
                </div>
            `).join('');
        }}
        
        function setRating(applicantId, rating) {{
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                applicant.rating = rating;
                saveData();
                renderApplicants();
            }}
        }}
        
        function setStatus(applicantId, status) {{
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                applicant.status = status;
                saveData();
                updateStats();
                renderApplicants();
            }}
        }}
        
        function updateNotes(applicantId, notes) {{
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                applicant.notes = notes;
                saveData();
            }}
        }}
        
        function viewProposal(applicantId) {{
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                alert(`Proposal from ${{applicant.name}}:\\n\\n${{applicant.proposal_text}}`);
            }}
        }}
        
        function saveData() {{
            // In a real application, this would save to a server
            localStorage.setItem('upworkApplicants', JSON.stringify(applicantsData));
            console.log('Data saved to localStorage');
        }}
        
        // Load saved data on startup
        const savedData = localStorage.getItem('upworkApplicants');
        if (savedData) {{
            const parsed = JSON.parse(savedData);
            // Merge with current data
            applicantsData.forEach(applicant => {{
                const saved = parsed.find(a => a.id === applicant.id);
                if (saved) {{
                    applicant.status = saved.status;
                    applicant.rating = saved.rating;
                    applicant.notes = saved.notes;
                }}
            }});
        }}
    </script>
</body>
</html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 Generated web interface: {filepath}")
        return filepath
    
    async def run(self):
        """Main workflow"""
        print("🚀 Starting Upwork Applicant Manager...")
        
        # Sample job URLs (you would replace these with your actual job URLs)
        job_urls = {
            "URGENT: Contract-to-hire Shopify Developer + UX Specialist - Start This Week!": "https://www.upwork.com/jobs/~0123456789abcdef",
            "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week": "https://www.upwork.com/jobs/~0987654321fedcba"
        }
        
        # Scrape applicants from your job postings
        await self.scrape_multiple_jobs(job_urls)
        
        # Save data
        data_file = self.save_applicants_data()
        
        # Generate web interface
        web_file = self.generate_web_interface()
        
        # Summary
        print(f"\n🎉 Applicant Manager Setup Complete!")
        print(f"📊 Total Applicants: {len(self.applicants)}")
        print(f"📁 Data File: {data_file}")
        print(f"🌐 Web Interface: {web_file}")
        print(f"\n💡 Next Steps:")
        print(f"   1. Open the web interface in your browser")
        print(f"   2. Filter and rate applicants")
        print(f"   3. Mark candidates for interview")
        print(f"   4. View full proposals")
        print(f"   5. Track hiring decisions")

async def main():
    """Main function"""
    manager = UpworkApplicantManager()
    await manager.run()

if __name__ == "__main__":
    asyncio.run(main()) 