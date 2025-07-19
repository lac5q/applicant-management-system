#!/usr/bin/env python3
"""
Build Site Structure - Create clean site with index.html as main page
"""

import os
import shutil
import json
from datetime import datetime
from applicant_database_manager import ApplicantDatabaseManager

class SiteStructureBuilder:
    """Build clean site structure with index.html as main page"""
    
    def __init__(self):
        self.db_manager = ApplicantDatabaseManager()
        self.site_dir = "../site"
        self.web_dir = "../output/web"
        
        print("🏗️  Site Structure Builder")
        print("=" * 60)
        print("📁 Creating clean site structure")
        print("🏠 Setting up index.html as main page")
        print("🧹 Removing old versions")
    
    def clean_old_files(self):
        """Remove old interface files and clean up"""
        print("\n🧹 Cleaning old files...")
        
        # Remove old web interface files
        if os.path.exists(self.web_dir):
            for filename in os.listdir(self.web_dir):
                if filename.startswith('enhanced_applicant_interface_') or filename.startswith('screenshot_applicants_interface_'):
                    filepath = os.path.join(self.web_dir, filename)
                    os.remove(filepath)
                    print(f"   🗑️  Removed: {filename}")
        
        # Remove old screenshot applicant files
        screenshot_dir = "../output/screenshot_applicants"
        if os.path.exists(screenshot_dir):
            for filename in os.listdir(screenshot_dir):
                if filename.startswith('screenshot_applicants_interface_'):
                    filepath = os.path.join(screenshot_dir, filename)
                    os.remove(filepath)
                    print(f"   🗑️  Removed: {filename}")
        
        print("✅ Cleanup complete")
    
    def create_site_structure(self):
        """Create the main site directory structure"""
        print("\n📁 Creating site structure...")
        
        # Create main site directory
        os.makedirs(self.site_dir, exist_ok=True)
        
        # Create subdirectories
        subdirs = [
            "assets/css",
            "assets/js", 
            "assets/images",
            "assets/profiles",
            "pages",
            "reports"
        ]
        
        for subdir in subdirs:
            os.makedirs(os.path.join(self.site_dir, subdir), exist_ok=True)
            print(f"   📁 Created: {subdir}")
        
        print("✅ Site structure created")
    
    def generate_main_index(self):
        """Generate the main index.html page"""
        print("\n🏠 Generating main index.html...")
        
        # Get data from database
        applicants = self.db_manager.get_all_applicants()
        jobs = self.db_manager.get_jobs()
        stats = self.db_manager.get_statistics()
        
        # Convert to JSON for JavaScript
        applicants_json = json.dumps(applicants, ensure_ascii=False)
        jobs_json = json.dumps(jobs, ensure_ascii=False)
        stats_json = json.dumps(stats, ensure_ascii=False)
        
        index_path = os.path.join(self.site_dir, "index.html")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Applicant Management System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-users"></i> Applicant Management System</h1>
                <p>Comprehensive hiring platform with job-based filtering and portfolio access</p>
                <div class="header-meta">
                    <span><i class="fas fa-calendar"></i> {datetime.now().strftime("%B %d, %Y")}</span>
                    <span><i class="fas fa-clock"></i> {datetime.now().strftime("%I:%M %p")}</span>
                </div>
            </div>
        </header>
        
        <div class="stats-bar" id="stats-bar">
            <!-- Stats will be populated by JavaScript -->
        </div>
        
        <div class="controls">
            <div class="filters">
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" id="search-input" placeholder="Search applicants by name, skills, or overview...">
                </div>
                <div class="filter-group">
                    <label><i class="fas fa-briefcase"></i> Job Position</label>
                    <select id="job-filter">
                        <option value="">All Positions</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label><i class="fas fa-tag"></i> Status</label>
                    <select id="status-filter">
                        <option value="">All Status</option>
                        <option value="pending">Pending Review</option>
                        <option value="interview">Interview</option>
                        <option value="hired">Hired</option>
                        <option value="rejected">Rejected</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label><i class="fas fa-star"></i> Rating</label>
                    <select id="rating-filter">
                        <option value="">All Ratings</option>
                        <option value="5">5 Stars</option>
                        <option value="4">4+ Stars</option>
                        <option value="3">3+ Stars</option>
                        <option value="2">2+ Stars</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label><i class="fas fa-dollar-sign"></i> Hourly Rate</label>
                    <select id="rate-filter">
                        <option value="">All Rates</option>
                        <option value="0-25">$0-$25/hr</option>
                        <option value="25-40">$25-$40/hr</option>
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
        
        <footer class="footer">
            <div class="footer-content">
                <p>&copy; 2025 Applicant Management System. All rights reserved.</p>
                <p>Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            </div>
        </footer>
    </div>

    <script>
        // Load data from database
        const applicantsData = {applicants_json};
        const jobsData = {jobs_json};
        const statsData = {stats_json};
        
        let filteredApplicants = [...applicantsData];
        
        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {{
            updateStats();
            populateJobFilter();
            renderApplicants();
            setupEventListeners();
        }});
        
        function updateStats() {{
            const statsBar = document.getElementById('stats-bar');
            statsBar.innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${{statsData.total_applicants}}</div>
                    <div>Total Applicants</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${{statsData.status_breakdown.pending || 0}}</div>
                    <div>Pending Review</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${{statsData.status_breakdown.interview || 0}}</div>
                    <div>Interview Candidates</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${{statsData.status_breakdown.hired || 0}}</div>
                    <div>Hired</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${{len(jobs)}}</div>
                    <div>Job Positions</div>
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
                        case '0-25': rateMatch = rate <= 25; break;
                        case '25-40': rateMatch = rate > 25 && rate <= 40; break;
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
                        <div class="profile-pic">
                            ${{applicant.name.charAt(0)}}
                        </div>
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
            const applicant = applicantsData.find(a => a.id === applicantId);
            if (applicant) {{
                applicant.status = status;
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
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated main index.html: {index_path}")
        return index_path
    
    def generate_css_styles(self):
        """Generate the main CSS file"""
        print("\n🎨 Generating CSS styles...")
        
        css_path = os.path.join(self.site_dir, "assets/css/style.css")
        
        css_content = """
/* Main Styles for Applicant Management System */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    line-height: 1.6;
}

.container {
    max-width: 1600px;
    margin: 0 auto;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    overflow: hidden;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header Styles */
.header {
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    color: white;
    padding: 40px 30px;
    text-align: center;
}

.header-content h1 {
    font-size: 2.8em;
    margin-bottom: 15px;
    font-weight: 300;
}

.header-content p {
    font-size: 1.2em;
    margin-bottom: 20px;
    opacity: 0.9;
}

.header-meta {
    display: flex;
    justify-content: center;
    gap: 30px;
    font-size: 0.9em;
    opacity: 0.8;
}

.header-meta span {
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Stats Bar */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 25px;
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.stat-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
}

.stat-number {
    font-size: 2.5em;
    font-weight: bold;
    color: #007bff;
    margin-bottom: 8px;
}

.stat-card div:last-child {
    color: #666;
    font-size: 0.9em;
}

/* Controls */
.controls {
    padding: 25px;
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.filters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.filter-group {
    display: flex;
    flex-direction: column;
}

.filter-group label {
    font-weight: 600;
    margin-bottom: 8px;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-group select, .filter-group input {
    padding: 12px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.2s;
}

.filter-group select:focus, .filter-group input:focus {
    outline: none;
    border-color: #007bff;
}

.search-box {
    grid-column: 1 / -1;
    position: relative;
}

.search-box i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #666;
}

.search-box input {
    width: 100%;
    padding: 12px 12px 12px 45px;
    border: 2px solid #007bff;
    border-radius: 25px;
    font-size: 16px;
}

/* Applicants Grid */
.applicants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 25px;
    padding: 30px;
    flex: 1;
    max-height: 70vh;
    overflow-y: auto;
}

.applicant-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    position: relative;
}

.applicant-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.job-badge {
    background: #e9ecef;
    color: #495057;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.8em;
    margin-bottom: 20px;
    display: inline-block;
    font-weight: 500;
}

/* Applicant Header */
.applicant-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.profile-pic {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.8em;
    font-weight: bold;
    margin-right: 20px;
    flex-shrink: 0;
}

.applicant-info {
    flex: 1;
}

.applicant-info h3 {
    color: #333;
    margin-bottom: 8px;
    font-size: 1.4em;
    font-weight: 600;
}

.applicant-info .title {
    color: #666;
    font-size: 1em;
    margin-bottom: 8px;
}

.applicant-info .location {
    color: #999;
    font-size: 0.9em;
    display: flex;
    align-items: center;
    gap: 5px;
}

.rating-badge {
    background: #28a745;
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9em;
    margin-left: auto;
}

/* Metrics */
.metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-bottom: 20px;
}

.metric {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    transition: background-color 0.2s;
}

.metric:hover {
    background: #e9ecef;
}

.metric .label {
    font-size: 0.8em;
    color: #666;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric .value {
    font-weight: bold;
    color: #333;
    font-size: 1.1em;
}

/* Skills */
.skills {
    margin-bottom: 20px;
}

.skill-tag {
    display: inline-block;
    background: #007bff;
    color: white;
    padding: 6px 12px;
    border-radius: 15px;
    font-size: 0.8em;
    margin: 3px;
    transition: background-color 0.2s;
}

.skill-tag:hover {
    background: #0056b3;
}

/* Overview */
.overview {
    color: #666;
    font-size: 0.9em;
    line-height: 1.5;
    margin-bottom: 20px;
    max-height: 60px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

/* Actions */
.actions {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.btn {
    padding: 10px 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9em;
    transition: all 0.2s;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-primary:hover {
    background: #0056b3;
    transform: translateY(-1px);
}

.btn-success {
    background: #28a745;
    color: white;
}

.btn-success:hover {
    background: #1e7e34;
    transform: translateY(-1px);
}

.btn-warning {
    background: #ffc107;
    color: #212529;
}

.btn-warning:hover {
    background: #e0a800;
    transform: translateY(-1px);
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.btn-danger:hover {
    background: #c82333;
    transform: translateY(-1px);
}

/* Status Badge */
.status-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-pending {
    background: #fff3cd;
    color: #856404;
}

.status-interview {
    background: #d1ecf1;
    color: #0c5460;
}

.status-hired {
    background: #d4edda;
    color: #155724;
}

.status-rejected {
    background: #f8d7da;
    color: #721c24;
}

/* Footer */
.footer {
    background: #f8f9fa;
    padding: 20px;
    text-align: center;
    border-top: 1px solid #dee2e6;
    margin-top: auto;
}

.footer-content p {
    color: #666;
    font-size: 0.9em;
    margin: 5px 0;
}

/* Loading and No Results */
.loading, .no-results {
    text-align: center;
    padding: 50px;
    color: #666;
    font-size: 1.2em;
    grid-column: 1 / -1;
}

.loading i {
    margin-right: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .applicants-grid {
        grid-template-columns: 1fr;
        padding: 20px;
    }
    
    .filters {
        grid-template-columns: 1fr;
    }
    
    .header-content h1 {
        font-size: 2em;
    }
    
    .stats-bar {
        grid-template-columns: repeat(2, 1fr);
        padding: 20px;
    }
    
    .actions {
        flex-direction: column;
    }
    
    .btn {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .stats-bar {
        grid-template-columns: 1fr;
    }
    
    .header {
        padding: 30px 20px;
    }
    
    .header-content h1 {
        font-size: 1.8em;
    }
    
    .applicant-header {
        flex-direction: column;
        text-align: center;
    }
    
    .profile-pic {
        margin-right: 0;
        margin-bottom: 15px;
    }
    
    .rating-badge {
        margin-left: 0;
        margin-top: 10px;
    }
}
        """
        
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"✅ Generated CSS styles: {css_path}")
        return css_path
    
    def create_readme(self):
        """Create a README file for the site"""
        print("\n📖 Creating README...")
        
        readme_path = os.path.join(self.site_dir, "README.md")
        
        readme_content = f"""# Applicant Management System

A comprehensive hiring platform with job-based filtering and portfolio access.

## 🚀 Features

- **Job-based filtering** - Filter by Shopify Developer or UX Designer positions
- **Advanced search** - Search across names, skills, and overviews
- **Portfolio access** - Direct links to candidate work samples
- **Profile images** - Visual identification for each applicant
- **Status tracking** - Manage interview and hiring pipeline
- **Real-time statistics** - Live dashboard with applicant metrics

## 📁 Site Structure

```
site/
├── index.html              # Main application interface
├── assets/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/                 # JavaScript files
│   ├── images/             # Site images
│   └── profiles/           # Applicant profile images
├── pages/                  # Additional pages
├── reports/                # Generated reports
└── README.md              # This file
```

## 🎯 Usage

1. **Open index.html** in your browser
2. **Use job filters** to view specific positions
3. **Search applicants** by name, skills, or overview
4. **View portfolios** by clicking portfolio links
5. **Update status** using action buttons
6. **Track progress** with real-time statistics

## 📊 Database

- **SQLite database** with structured applicant data
- **Job categorization** for easy filtering
- **Portfolio links** and work samples
- **Rating system** with detailed breakdowns

## 🛠️ Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python with SQLite database
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome 6.0

## 📅 Generated

{datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## 🔗 Quick Links

- [Main Interface](./index.html)
- [Database Manager](../scripts/applicant_database_manager.py)
- [Processing Scripts](../scripts/)

---

Built with ❤️ for efficient applicant management
        """
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ Created README: {readme_path}")
        return readme_path
    
    def copy_profile_images(self):
        """Copy profile images to the site assets"""
        print("\n📷 Copying profile images...")
        
        source_dir = "../output/screenshot_applicants"
        target_dir = os.path.join(self.site_dir, "assets/profiles")
        
        if os.path.exists(source_dir):
            for filename in os.listdir(source_dir):
                if filename.endswith('.png') and 'profile_' in filename:
                    source_path = os.path.join(source_dir, filename)
                    target_path = os.path.join(target_dir, filename)
                    shutil.copy2(source_path, target_path)
                    print(f"   📷 Copied: {filename}")
        
        print("✅ Profile images copied")
    
    def run(self):
        """Main build workflow"""
        print("🚀 Starting site structure build...")
        
        # Clean old files
        self.clean_old_files()
        
        # Create site structure
        self.create_site_structure()
        
        # Generate main files
        index_file = self.generate_main_index()
        css_file = self.generate_css_styles()
        readme_file = self.create_readme()
        
        # Copy assets
        self.copy_profile_images()
        
        # Final summary
        stats = self.db_manager.get_statistics()
        
        print(f"\n🎉 Site Structure Complete!")
        print(f"🏠 Main Page: {index_file}")
        print(f"🎨 Styles: {css_file}")
        print(f"📖 Documentation: {readme_file}")
        print(f"📊 Total Applicants: {stats['total_applicants']}")
        print(f"💼 Job Positions: {len(stats['jobs_breakdown'])}")
        
        print(f"\n💡 Site Features:")
        print(f"   ✅ Clean, modern design")
        print(f"   ✅ Job-based filtering")
        print(f"   ✅ Responsive layout")
        print(f"   ✅ Professional styling")
        print(f"   ✅ Easy navigation")
        print(f"   ✅ Portfolio access")

def main():
    """Main function"""
    builder = SiteStructureBuilder()
    builder.run()

if __name__ == "__main__":
    main() 