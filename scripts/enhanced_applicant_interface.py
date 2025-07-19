#!/usr/bin/env python3
"""
Enhanced Applicant Interface - Web interface with database integration and job filtering
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from applicant_database_manager import ApplicantDatabaseManager

class EnhancedApplicantInterface:
    """Enhanced web interface with database integration"""
    
    def __init__(self):
        self.db_manager = ApplicantDatabaseManager()
        self.web_dir = "../output/web"
        os.makedirs(self.web_dir, exist_ok=True)
        
        print("🌐 Enhanced Applicant Interface")
        print("=" * 60)
        print("📊 Database-driven applicant management")
        print("🔍 Advanced filtering and search")
        print("📱 Responsive design with all applicants visible")
    
    def load_sample_data(self):
        """Load sample applicants into the database"""
        print("\n📥 Loading sample applicants into database...")
        
        sample_applicants = [
            # Shopify Developer applicants
            {
                "id": "shopify_001", "name": "Mykola V", "title": "Senior Shopify/Vue.js Developer",
                "location": "Kyiv, Ukraine", "hourly_rate": "$25.00/hr", "job_success": "97% Job Success",
                "total_earned": "$10K+ earned", "hours_worked": "1,000+ hours", "jobs_completed": "100+ jobs",
                "skills": ["Shopify", "Vue.js", "JavaScript", "HTML", "CSS", "Liquid", "Web Development"],
                "overview": "Experienced Shopify developer with 5+ years in e-commerce development...",
                "proposal_text": "I have extensive experience with Shopify development and Vue.js...",
                "job_title": "URGENT: Contract-to-hire Shopify Developer + UX Specialist - Start This Week!",
                "rating": 3, "status": "pending"
            },
            {
                "id": "shopify_002", "name": "Volkan K", "title": "Full Stack Developer | UI/UX Designer",
                "location": "Istanbul, Turkey", "hourly_rate": "$30.00/hr", "job_success": "100% Job Success",
                "total_earned": "$20K+ earned", "hours_worked": "500+ hours", "jobs_completed": "50+ jobs",
                "skills": ["UI/UX Design", "Figma", "Adobe XD", "Webflow", "React", "Node.js", "JavaScript"],
                "overview": "Full-stack developer with strong UI/UX design skills...",
                "proposal_text": "I can handle both the development and design aspects of your project...",
                "job_title": "URGENT: Contract-to-hire Shopify Developer + UX Specialist - Start This Week!",
                "rating": 3, "status": "pending"
            },
            {
                "id": "shopify_003", "name": "Roohi K", "title": "UX/UI Designer & Webflow Developer",
                "location": "Lahore, Pakistan", "hourly_rate": "$20.00/hr", "job_success": "100% Job Success",
                "total_earned": "$1K+ earned", "hours_worked": "100+ hours", "jobs_completed": "10+ jobs",
                "skills": ["UI/UX Design", "Webflow", "Figma", "Adobe XD", "Responsive Design", "Prototyping"],
                "overview": "Creative UX/UI designer with Webflow development skills...",
                "proposal_text": "I specialize in creating beautiful, user-friendly interfaces...",
                "job_title": "URGENT: Contract-to-hire Shopify Developer + UX Specialist - Start This Week!",
                "rating": 3, "status": "pending"
            },
            # UX Designer applicants
            {
                "id": "ux_001", "name": "Rohan S", "title": "UI/UX Designer | Figma | Web & Mobile App Design",
                "location": "India", "hourly_rate": "$50.00/hr", "job_success": "99% Job Success",
                "total_earned": "$10K+ earned", "hours_worked": "1,000+ hours", "jobs_completed": "100+ jobs",
                "skills": ["UI Design", "UX Design", "Figma", "Web Design", "Mobile App Design", "User Interface Design"],
                "overview": "Senior UI/UX designer with expertise in conversion optimization...",
                "proposal_text": "I have a proven track record of improving conversion rates through design...",
                "job_title": "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week",
                "rating": 3, "status": "pending"
            },
            {
                "id": "ux_002", "name": "Aman M", "title": "Sr. UI/UX Designer | Figma | Web & Mobile App Design",
                "location": "India", "hourly_rate": "$45.00/hr", "job_success": "100% Job Success",
                "total_earned": "$5K+ earned", "hours_worked": "750+ hours", "jobs_completed": "75+ jobs",
                "skills": ["UX Design", "UI Design", "Figma", "Adobe XD", "Wireframing", "Prototyping"],
                "overview": "Senior UX designer specializing in user research and conversion optimization...",
                "proposal_text": "I focus on data-driven design decisions to improve user experience...",
                "job_title": "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week",
                "rating": 3, "status": "pending"
            },
            {
                "id": "ux_003", "name": "Dharmesh B", "title": "UI/UX Designer | Conversion Specialist",
                "location": "India", "hourly_rate": "$40.00/hr", "job_success": "98% Job Success",
                "total_earned": "$8K+ earned", "hours_worked": "800+ hours", "jobs_completed": "80+ jobs",
                "skills": ["Conversion Rate Optimization", "Landing Page Design", "A/B Testing", "UI/UX Design"],
                "overview": "Conversion-focused UX designer with expertise in landing page optimization...",
                "proposal_text": "I specialize in designing high-converting user experiences...",
                "job_title": "URGENT Contract-to-Hire UX/Conversion Designer - Start This Week",
                "rating": 3, "status": "pending"
            }
        ]
        
        for applicant in sample_applicants:
            self.db_manager.add_applicant(applicant)
        
        print(f"✅ Loaded {len(sample_applicants)} sample applicants into database")
    
    def generate_enhanced_interface(self):
        """Generate enhanced web interface with database integration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_applicant_interface_{timestamp}.html"
        filepath = os.path.join(self.web_dir, filename)
        
        # Get data from database
        applicants = self.db_manager.get_all_applicants()
        jobs = self.db_manager.get_jobs()
        stats = self.db_manager.get_statistics()
        
        # Convert to JSON for JavaScript
        applicants_json = json.dumps(applicants, ensure_ascii=False)
        jobs_json = json.dumps(jobs, ensure_ascii=False)
        stats_json = json.dumps(stats, ensure_ascii=False)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Applicant Manager</title>
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
            max-width: 1600px;
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
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            padding: 20px;
            max-height: 70vh;
            overflow-y: auto;
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
        
        .rating-badge {{
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            margin-left: auto;
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
        
        .job-badge {{
            background: #e9ecef;
            color: #495057;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            margin-bottom: 10px;
            display: inline-block;
        }}
        
        .no-results {{
            text-align: center;
            padding: 50px;
            color: #666;
            font-size: 1.2em;
        }}
        
        .loading {{
            text-align: center;
            padding: 50px;
            color: #666;
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
            <h1><i class="fas fa-users"></i> Enhanced Applicant Manager</h1>
            <p>Database-driven applicant management with advanced filtering</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="stats-bar" id="stats-bar">
            <!-- Stats will be populated by JavaScript -->
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
                        <option value="2">2+ Stars</option>
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
            <div class="loading">
                <i class="fas fa-spinner fa-spin"></i> Loading applicants...
            </div>
        </div>
    </div>

    <script>
        // Load data from database
        const applicantsData = {applicants_json};
        const jobsData = {jobs_json};
        const statsData = {stats_json};
        
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
            const statsBar = document.getElementById('stats-bar');
            statsBar.innerHTML = `
                <div class="stat-card">
                    <div class="number">${{statsData.total_applicants}}</div>
                    <div>Total Applicants</div>
                </div>
                <div class="stat-card">
                    <div class="number">${{statsData.status_breakdown.pending || 0}}</div>
                    <div>Pending Review</div>
                </div>
                <div class="stat-card">
                    <div class="number">${{statsData.status_breakdown.interview || 0}}</div>
                    <div>Interview Candidates</div>
                </div>
                <div class="stat-card">
                    <div class="number">${{statsData.status_breakdown.hired || 0}}</div>
                    <div>Hired</div>
                </div>
            `;
        }}
        
        function populateJobFilter() {{
            const jobFilter = document.getElementById('job-filter');
            
            jobsData.forEach(job => {{
                const option = document.createElement('option');
                option.value = job.job_title;
                option.textContent = `${{job.job_title}} (${{job.applicant_count}} applicants)`;
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
                    (applicant.skills && applicant.skills.some(skill => skill.toLowerCase().includes(searchTerm))) ||
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
                    <div class="job-badge">${{applicant.job_title}}</div>
                    
                    <div class="applicant-header">
                        <div class="profile-pic">${{applicant.name.charAt(0)}}</div>
                        <div class="applicant-info">
                            <h3>${{applicant.name}}</h3>
                            <div class="title">${{applicant.title}}</div>
                            <div class="location"><i class="fas fa-map-marker-alt"></i> ${{applicant.location}}</div>
                        </div>
                        <div class="rating-badge">${{applicant.rating}}/5</div>
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
                        ${{(applicant.skills || []).map(skill => `<span class="skill-tag">${{skill}}</span>`).join('')}}
                    </div>
                    
                    <div class="overview">${{applicant.overview}}</div>
                    
                    <div class="actions">
                        <button class="btn btn-primary" onclick="viewProposal(${{applicant.id}})">
                            <i class="fas fa-eye"></i> View Proposal
                        </button>
                        <button class="btn btn-success" onclick="setStatus(${{applicant.id}}, 'interview')">
                            <i class="fas fa-calendar"></i> Interview
                        </button>
                        <button class="btn btn-warning" onclick="setStatus(${{applicant.id}}, 'hired')">
                            <i class="fas fa-check"></i> Hire
                        </button>
                        <button class="btn btn-danger" onclick="setStatus(${{applicant.id}}, 'rejected')">
                            <i class="fas fa-times"></i> Reject
                        </button>
                    </div>
                    
                    <div class="status-badge status-${{applicant.status}}">${{applicant.status.toUpperCase()}}</div>
                </div>
            `).join('');
        }}
        
        function setStatus(applicantId, status) {{
            // In a real application, this would update the database
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                applicant.status = status;
                // Update the database via API call
                console.log(`Updating applicant ${{applicantId}} status to ${{status}}`);
                renderApplicants();
            }}
        }}
        
        function viewProposal(applicantId) {{
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                alert(`Proposal from ${{applicant.name}}:\\n\\n${{applicant.proposal_text || 'No proposal text available'}}`);
            }}
        }}
    </script>
</body>
</html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 Generated enhanced interface: {filepath}")
        return filepath
    
    async def run(self):
        """Main workflow"""
        print("🚀 Starting Enhanced Applicant Interface...")
        
        # Load sample data into database
        self.load_sample_data()
        
        # Generate enhanced interface
        interface_file = self.generate_enhanced_interface()
        
        # Get statistics
        stats = self.db_manager.get_statistics()
        
        # Summary
        print(f"\n🎉 Enhanced Interface Complete!")
        print(f"📊 Total Applicants in Database: {stats['total_applicants']}")
        print(f"📋 Jobs: {len(stats['jobs_breakdown'])}")
        print(f"🌐 Interface: {interface_file}")
        
        print(f"\n💡 Features:")
        print(f"   ✅ Database-driven storage")
        print(f"   ✅ All applicants visible on one page")
        print(f"   ✅ Filter by job title")
        print(f"   ✅ Advanced search and filtering")
        print(f"   ✅ Real-time statistics")
        print(f"   ✅ Responsive design")

async def main():
    """Main function"""
    interface = EnhancedApplicantInterface()
    await interface.run()

if __name__ == "__main__":
    asyncio.run(main()) 