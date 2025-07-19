#!/usr/bin/env python3
"""
Candidate Processing Script
Extracts, looks up, and processes all candidates from screenshots and existing data files.
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path
import cv2
import pytesseract
from PIL import Image
import numpy as np
import re
from typing import Dict, List, Any, Optional
import requests
from urllib.parse import urlparse
import hashlib

class CandidateProcessor:
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.output_dir = self.workspace_path / "output"
        self.processed_dir = self.output_dir / "processed_candidates"
        self.processed_dir.mkdir(exist_ok=True)
        
        # Database setup
        self.db_path = self.output_dir / "applicants" / "applicants.db"
        self.setup_database()
        
        # Timestamp for processing
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def setup_database(self):
        """Setup SQLite database for storing processed candidate data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create candidates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id TEXT PRIMARY KEY,
                name TEXT,
                title TEXT,
                location TEXT,
                hourly_rate TEXT,
                job_success TEXT,
                total_earned TEXT,
                hours_worked TEXT,
                jobs_completed TEXT,
                skills TEXT,
                overview TEXT,
                proposal_text TEXT,
                job_title TEXT,
                profile_url TEXT,
                status TEXT DEFAULT 'pending',
                rating INTEGER DEFAULT 0,
                applied_date TEXT,
                notes TEXT,
                profile_image TEXT,
                screenshot_source TEXT,
                portfolio_links TEXT,
                work_samples TEXT,
                processed_at TEXT,
                extracted_from_screenshot BOOLEAN DEFAULT FALSE,
                ocr_confidence REAL DEFAULT 0.0
            )
        ''')
        
        # Create processing_log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processing_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                details TEXT,
                success BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_processing(self, action: str, details: str, success: bool = True):
        """Log processing actions to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO processing_log (timestamp, action, details, success)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), action, details, success))
        conn.commit()
        conn.close()
        
    def extract_text_from_image(self, image_path: str) -> Dict[str, Any]:
        """Extract text from screenshot using OCR."""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return {"text": "", "confidence": 0.0, "error": "Could not load image"}
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing
            # Remove noise
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply threshold
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(thresh)
            
            # Get confidence data
            data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "text": text,
                "confidence": avg_confidence,
                "error": None
            }
            
        except Exception as e:
            return {"text": "", "confidence": 0.0, "error": str(e)}
    
    def parse_candidate_from_text(self, text: str, image_path: str) -> Dict[str, Any]:
        """Parse candidate information from extracted text."""
        candidate = {
            "id": f"extracted_{hashlib.md5(image_path.encode()).hexdigest()[:8]}",
            "name": "",
            "title": "",
            "location": "",
            "hourly_rate": "",
            "job_success": "",
            "total_earned": "",
            "hours_worked": "",
            "jobs_completed": "",
            "skills": [],
            "overview": "",
            "proposal_text": "",
            "job_title": "",
            "profile_url": "",
            "status": "pending",
            "rating": 0,
            "applied_date": datetime.now().strftime("%Y-%m-%d"),
            "notes": "",
            "profile_image": image_path,
            "screenshot_source": os.path.basename(image_path),
            "portfolio_links": [],
            "work_samples": [],
            "processed_at": datetime.now().isoformat(),
            "extracted_from_screenshot": True,
            "ocr_confidence": 0.0
        }
        
        # Extract name (usually appears first)
        name_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+)'
        name_match = re.search(name_pattern, text)
        if name_match:
            candidate["name"] = name_match.group(1)
        
        # Extract title
        title_patterns = [
            r'(Senior|Junior|Full Stack|Frontend|Backend|UI/UX|Shopify|React|Vue|Angular)[\s\w/]+(Developer|Designer|Engineer)',
            r'([A-Z][a-z\s]+(Developer|Designer|Engineer|Specialist))'
        ]
        for pattern in title_patterns:
            title_match = re.search(pattern, text)
            if title_match:
                candidate["title"] = title_match.group(0).strip()
                break
        
        # Extract location
        location_pattern = r'([A-Z][a-z]+,\s*[A-Z][a-z]+)'
        location_match = re.search(location_pattern, text)
        if location_match:
            candidate["location"] = location_match.group(1)
        
        # Extract hourly rate
        rate_pattern = r'\$(\d+(?:\.\d{2})?)/hr'
        rate_match = re.search(rate_pattern, text)
        if rate_match:
            candidate["hourly_rate"] = f"${rate_match.group(1)}/hr"
        
        # Extract job success
        success_pattern = r'(\d+%) Job Success'
        success_match = re.search(success_pattern, text)
        if success_match:
            candidate["job_success"] = success_match.group(0)
        
        # Extract total earned
        earned_pattern = r'\$(\d+K?\+?) earned'
        earned_match = re.search(earned_pattern, text)
        if earned_match:
            candidate["total_earned"] = f"${earned_match.group(1)} earned"
        
        # Extract hours worked
        hours_pattern = r'(\d+(?:,\d+)?\+?) hours'
        hours_match = re.search(hours_pattern, text)
        if hours_match:
            candidate["hours_worked"] = f"{hours_match.group(1)} hours"
        
        # Extract jobs completed
        jobs_pattern = r'(\d+\+) jobs'
        jobs_match = re.search(jobs_pattern, text)
        if jobs_match:
            candidate["jobs_completed"] = jobs_match.group(0)
        
        # Extract skills (common tech skills)
        skills_patterns = [
            r'\b(Shopify|React|Vue|Angular|JavaScript|TypeScript|HTML|CSS|Node\.js|Python|PHP|Java|C#|Ruby|Go|Rust|Swift|Kotlin|Flutter|React Native|WordPress|Drupal|Magento|WooCommerce|Figma|Adobe XD|Sketch|InVision|Zeplin|Webflow|Bubble|Airtable|Zapier|Shopify Liquid|GraphQL|REST API|MongoDB|PostgreSQL|MySQL|Firebase|AWS|Google Cloud|Azure|Docker|Kubernetes|Git|GitHub|GitLab|Bitbucket|Jira|Trello|Asana|Slack|Discord|Zoom|Teams|Figma|Canva|Photoshop|Illustrator|InDesign|Premiere Pro|After Effects|Blender|Unity|Unreal Engine|Maya|3ds Max|AutoCAD|SketchUp|Revit|SolidWorks|Fusion 360|Tinkercad|Arduino|Raspberry Pi|IoT|Machine Learning|AI|Data Science|Analytics|SEO|SEM|PPC|Google Ads|Facebook Ads|Instagram Ads|TikTok Ads|LinkedIn Ads|Email Marketing|SMS Marketing|Push Notifications|Chatbots|Voice Assistants|Blockchain|Cryptocurrency|NFT|Web3|DeFi|Smart Contracts|Ethereum|Bitcoin|Solana|Polygon|Arbitrum|Optimism|Layer 2|Rollups|Zero Knowledge|Privacy|Security|Penetration Testing|Ethical Hacking|Cybersecurity|Compliance|GDPR|CCPA|HIPAA|SOC 2|ISO 27001|PCI DSS|OWASP|NIST|MITRE|Threat Modeling|Risk Assessment|Vulnerability Assessment|Incident Response|Forensics|Malware Analysis|Reverse Engineering|Exploit Development|Bug Bounty|CTF|HackTheBox|TryHackMe|VulnHub|Metasploit|Burp Suite|Wireshark|Nmap|Nessus|Qualys|Rapid7|Tenable|CrowdStrike|SentinelOne|Carbon Black|Cylance|Bitdefender|Kaspersky|Norton|McAfee|Trend Micro|Sophos|ESET|Avast|AVG|Malwarebytes|Windows Defender|Firewall|IDS|IPS|SIEM|SOAR|EDR|XDR|MDR|SOC|NOC|ITIL|Agile|Scrum|Kanban|Lean|Six Sigma|DevOps|CI/CD|Jenkins|GitHub Actions|GitLab CI|CircleCI|Travis CI|TeamCity|Bamboo|Ansible|Chef|Puppet|Salt|Terraform|CloudFormation|Pulumi|Kubernetes|Docker|OpenShift|Rancher|Istio|Linkerd|Consul|Vault|Nomad|Mesos|Marathon|Swarm|Compose|Buildah|Podman|Skopeo|Kaniko|BuildKit|Dockerfile|docker-compose|Helm|Kustomize|Operator|CRD|Custom Resource|API Server|Controller|Reconciler|Admission Controller|Webhook|RBAC|Service Account|Secret|ConfigMap|PersistentVolume|StorageClass|Ingress|Service|Pod|Deployment|StatefulSet|DaemonSet|Job|CronJob|ReplicaSet|HorizontalPodAutoscaler|VerticalPodAutoscaler|PodDisruptionBudget|NetworkPolicy|PodSecurityPolicy|PodSecurityStandards|SecurityContext|ResourceQuota|LimitRange|PriorityClass|Taint|Toleration|NodeSelector|Affinity|Anti-affinity|TopologySpread|PodTopologySpread|PodAntiAffinity|PodAffinity|NodeAffinity|NodeAntiAffinity|TopologyKey|Label|Annotation|OwnerReference|Finalizer|Garbage Collection|Orphan|Cascade|Background|Foreground|Graceful|Force|Preemption|Eviction|OOM|CPU|Memory|Storage|Network|GPU|TPU|FPGA|ASIC|Custom Hardware|Edge Computing|Fog Computing|Cloud Computing|Hybrid Cloud|Multi Cloud|Private Cloud|Public Cloud|Community Cloud|Infrastructure as Code|Platform as a Service|Software as a Service|Function as a Service|Container as a Service|Backend as a Service|Database as a Service|Storage as a Service|Network as a Service|Security as a Service|Monitoring as a Service|Logging as a Service|Analytics as a Service|AI as a Service|ML as a Service|Data as a Service|API as a Service|Integration as a Service|Process as a Service|Business Process as a Service|Workflow as a Service|Orchestration as a Service|Scheduling as a Service|Load Balancing as a Service|Caching as a Service|CDN|Content Delivery Network|Edge Network|Global Load Balancer|Regional Load Balancer|Local Load Balancer|Application Load Balancer|Network Load Balancer|Gateway Load Balancer|Classic Load Balancer|Target Group|Listener|Rule|Action|Condition|Health Check|Auto Scaling|Scaling Policy|Cooldown|Warm-up|Scale-in|Scale-out|Horizontal Scaling|Vertical Scaling|Elastic Scaling|Predictive Scaling|Scheduled Scaling|Step Scaling|Target Tracking|Custom Metric|CloudWatch|Monitoring|Logging|Tracing|Distributed Tracing|OpenTelemetry|Jaeger|Zipkin|Prometheus|Grafana|Kibana|Elasticsearch|Logstash|Beats|Fluentd|Fluent Bit|Vector|Telegraf|InfluxDB|TimescaleDB|VictoriaMetrics|Thanos|Cortex|Mimir|Loki|Tempo|Jaeger|Zipkin|X-Ray|Datadog|New Relic|AppDynamics|Dynatrace|Splunk|Sumo Logic|Loggly|Papertrail|Sentry|Bugsnag|Rollbar|Airbrake|Honeybadger|Raygun|Crashlytics|Firebase Crashlytics|Microsoft App Center|HockeyApp|TestFlight|Google Play Console|App Store Connect|CodePush|Expo|React Native|Flutter|Ionic|Cordova|PhoneGap|Xamarin|Unity|Unreal Engine|Godot|LÖVE|MonoGame|LibGDX|Cocos2d|SpriteKit|SceneKit|Metal|Vulkan|OpenGL|DirectX|WebGL|Canvas|SVG|WebAssembly|Web Workers|Service Workers|Progressive Web App|Single Page Application|Multi Page Application|Server Side Rendering|Static Site Generation|Incremental Static Regeneration|Client Side Rendering|Hydration|Streaming|Suspense|Concurrent Features|Fiber|Reconciliation|Virtual DOM|Shadow DOM|Web Components|Custom Elements|Shadow Root|Slot|Template|HTML Templates|CSS-in-JS|Styled Components|Emotion|Styled JSX|CSS Modules|PostCSS|Sass|Less|Stylus|Tailwind CSS|Bootstrap|Foundation|Bulma|Semantic UI|Material-UI|Ant Design|Chakra UI|Mantine|NextUI|Radix UI|Headless UI|Reach UI|Ariakit|React Aria|React Hook Form|Formik|React Final Form|React Query|SWR|Apollo Client|Relay|Redux|MobX|Zustand|Jotai|Recoil|Valtio|XState|React Router|Next.js Router|Gatsby Router|Remix Router|TanStack Router|React Navigation|React Native Router|Flutter Router|Ionic Router|Vue Router|Angular Router|Svelte Router|Solid Router|Qwik Router|Astro Router|Nuxt Router|Gatsby|Next.js|Remix|SvelteKit|SolidStart|Qwik|Astro|Nuxt|Vite|Webpack|Rollup|Parcel|esbuild|SWC|Babel|TypeScript|Flow|PropTypes|ESLint|Prettier|Husky|lint-staged|Commitizen|Conventional Commits|Semantic Release|Release It|Changesets|Lerna|Nx|Turborepo|Yarn Workspaces|npm Workspaces|pnpm Workspaces|Monorepo|Microservices|Micro Frontends|Module Federation|Webpack Module Federation|Vite Module Federation|Rollup Module Federation|esbuild Module Federation|SWC Module Federation|Babel Module Federation|TypeScript Module Federation|Flow Module Federation|PropTypes Module Federation|ESLint Module Federation|Prettier Module Federation|Husky Module Federation|lint-staged Module Federation|Commitizen Module Federation|Conventional Commits Module Federation|Semantic Release Module Federation|Release It Module Federation|Changesets Module Federation|Lerna Module Federation|Nx Module Federation|Turborepo Module Federation|Yarn Workspaces Module Federation|npm Workspaces Module Federation|pnpm Workspaces Module Federation|Monorepo Module Federation|Microservices Module Federation|Micro Frontends Module Federation|Module Federation Module Federation|Webpack Module Federation Module Federation|Vite Module Federation Module Federation|Rollup Module Federation Module Federation|esbuild Module Federation Module Federation|SWC Module Federation Module Federation|Babel Module Federation Module Federation|TypeScript Module Federation Module Federation|Flow Module Federation Module Federation|PropTypes Module Federation Module Federation|ESLint Module Federation Module Federation|Prettier Module Federation Module Federation|Husky Module Federation Module Federation|lint-staged Module Federation Module Federation|Commitizen Module Federation Module Federation|Conventional Commits Module Federation Module Federation|Semantic Release Module Federation Module Federation|Release It Module Federation Module Federation|Changesets Module Federation Module Federation|Lerna Module Federation Module Federation|Nx Module Federation Module Federation|Turborepo Module Federation Module Federation|Yarn Workspaces Module Federation Module Federation|npm Workspaces Module Federation Module Federation|pnpm Workspaces Module Federation Module Federation|Monorepo Module Federation Module Federation|Microservices Module Federation Module Federation|Micro Frontends Module Federation Module Federation|Module Federation Module Federation Module Federation)\b'
        ]
        
        for pattern in skills_patterns:
            skills = re.findall(pattern, text, re.IGNORECASE)
            candidate["skills"].extend(skills)
        
        # Remove duplicates and clean up
        candidate["skills"] = list(set([skill.strip() for skill in candidate["skills"] if skill.strip()]))
        
        return candidate
    
    def process_screenshot_file(self, image_path: str) -> Dict[str, Any]:
        """Process a single screenshot file and extract candidate information."""
        try:
            # Extract text from image
            ocr_result = self.extract_text_from_image(image_path)
            
            if ocr_result["error"]:
                self.log_processing("ocr_error", f"Failed to extract text from {image_path}: {ocr_result['error']}", False)
                return None
            
            # Parse candidate information from text
            candidate = self.parse_candidate_from_text(ocr_result["text"], image_path)
            candidate["ocr_confidence"] = ocr_result["confidence"]
            
            # Save to database
            self.save_candidate_to_db(candidate)
            
            self.log_processing("screenshot_processed", f"Successfully processed {image_path}")
            return candidate
            
        except Exception as e:
            self.log_processing("screenshot_error", f"Error processing {image_path}: {str(e)}", False)
            return None
    
    def save_candidate_to_db(self, candidate: Dict[str, Any]):
        """Save candidate data to SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert lists to JSON strings
        skills_json = json.dumps(candidate.get("skills", []))
        portfolio_links_json = json.dumps(candidate.get("portfolio_links", []))
        work_samples_json = json.dumps(candidate.get("work_samples", []))
        
        cursor.execute('''
            INSERT OR REPLACE INTO candidates (
                id, name, title, location, hourly_rate, job_success, total_earned,
                hours_worked, jobs_completed, skills, overview, proposal_text,
                job_title, profile_url, status, rating, applied_date, notes,
                profile_image, screenshot_source, portfolio_links, work_samples,
                processed_at, extracted_from_screenshot, ocr_confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate["id"], candidate["name"], candidate["title"], candidate["location"],
            candidate["hourly_rate"], candidate["job_success"], candidate["total_earned"],
            candidate["hours_worked"], candidate["jobs_completed"], skills_json,
            candidate["overview"], candidate["proposal_text"], candidate["job_title"],
            candidate["profile_url"], candidate["status"], candidate["rating"],
            candidate["applied_date"], candidate["notes"], candidate["profile_image"],
            candidate["screenshot_source"], portfolio_links_json, work_samples_json,
            candidate["processed_at"], candidate["extracted_from_screenshot"],
            candidate["ocr_confidence"]
        ))
        
        conn.commit()
        conn.close()
    
    def process_existing_json_data(self):
        """Process existing JSON data files and import to database."""
        json_files = [
            self.output_dir / "screenshot_applicants" / "screenshot_applicants_20250719_021451.json",
            self.output_dir / "applicants" / "rated_applicants_20250719_015943.json",
            self.output_dir / "applicants" / "upwork_applicants_20250719_015513.json"
        ]
        
        processed_candidates = []
        
        for json_file in json_files:
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if isinstance(data, list):
                        candidates = data
                    elif isinstance(data, dict) and "applicants" in data:
                        candidates = data["applicants"]
                    else:
                        continue
                    
                    for candidate in candidates:
                        if isinstance(candidate, dict):
                            # Ensure candidate has required fields
                            candidate.setdefault("id", f"imported_{len(processed_candidates)}")
                            candidate.setdefault("extracted_from_screenshot", False)
                            candidate.setdefault("ocr_confidence", 0.0)
                            candidate.setdefault("processed_at", datetime.now().isoformat())
                            
                            self.save_candidate_to_db(candidate)
                            processed_candidates.append(candidate)
                    
                    self.log_processing("json_imported", f"Imported {len(candidates)} candidates from {json_file.name}")
                    
                except Exception as e:
                    self.log_processing("json_import_error", f"Error importing {json_file.name}: {str(e)}", False)
        
        return processed_candidates
    
    def find_screenshot_files(self) -> List[str]:
        """Find all screenshot files in the workspace."""
        screenshot_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        screenshot_files = []
        
        for root, dirs, files in os.walk(self.workspace_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in screenshot_extensions):
                    # Skip files in node_modules, .git, and other system directories
                    if any(skip_dir in root for skip_dir in ['node_modules', '.git', '__pycache__', '.next', 'venv', '.venv']):
                        continue
                    screenshot_files.append(os.path.join(root, file))
        
        return screenshot_files
    
    def process_all_screenshots(self) -> List[Dict[str, Any]]:
        """Process all screenshot files found in the workspace."""
        screenshot_files = self.find_screenshot_files()
        processed_candidates = []
        
        print(f"Found {len(screenshot_files)} screenshot files")
        
        for screenshot_file in screenshot_files:
            print(f"Processing: {screenshot_file}")
            candidate = self.process_screenshot_file(screenshot_file)
            if candidate:
                processed_candidates.append(candidate)
        
        return processed_candidates
    
    def generate_processing_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report of all processed candidates."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total candidates
        cursor.execute("SELECT COUNT(*) FROM candidates")
        total_candidates = cursor.fetchone()[0]
        
        # Get candidates by source
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN extracted_from_screenshot = 1 THEN 'Screenshot OCR'
                    ELSE 'JSON Import'
                END as source,
                COUNT(*) as count
            FROM candidates 
            GROUP BY extracted_from_screenshot
        """)
        source_stats = dict(cursor.fetchall())
        
        # Get candidates by status
        cursor.execute("SELECT status, COUNT(*) FROM candidates GROUP BY status")
        status_stats = dict(cursor.fetchall())
        
        # Get top skills
        cursor.execute("SELECT skills FROM candidates WHERE skills IS NOT NULL AND skills != '[]'")
        all_skills = []
        for row in cursor.fetchall():
            try:
                skills = json.loads(row[0])
                all_skills.extend(skills)
            except:
                continue
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Get average OCR confidence
        cursor.execute("SELECT AVG(ocr_confidence) FROM candidates WHERE extracted_from_screenshot = 1")
        avg_confidence = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_candidates": total_candidates,
            "source_breakdown": source_stats,
            "status_breakdown": status_stats,
            "top_skills": top_skills,
            "average_ocr_confidence": avg_confidence,
            "processing_timestamp": self.timestamp
        }
        
        # Save report
        report_path = self.processed_dir / f"candidate_processing_report_{self.timestamp}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def export_candidates_to_json(self) -> str:
        """Export all candidates to JSON file."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM candidates")
        columns = [description[0] for description in cursor.description]
        
        candidates = []
        for row in cursor.fetchall():
            candidate = dict(zip(columns, row))
            # Parse JSON fields
            for field in ['skills', 'portfolio_links', 'work_samples']:
                if candidate[field]:
                    try:
                        candidate[field] = json.loads(candidate[field])
                    except:
                        candidate[field] = []
                else:
                    candidate[field] = []
            candidates.append(candidate)
        
        conn.close()
        
        # Save to file
        export_path = self.processed_dir / f"all_candidates_{self.timestamp}.json"
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
        
        return str(export_path)
    
    def run_full_processing(self):
        """Run the complete candidate processing pipeline."""
        print("Starting candidate processing pipeline...")
        
        # Step 1: Process existing JSON data
        print("Step 1: Processing existing JSON data...")
        json_candidates = self.process_existing_json_data()
        print(f"Imported {len(json_candidates)} candidates from JSON files")
        
        # Step 2: Process screenshot files
        print("Step 2: Processing screenshot files...")
        screenshot_candidates = self.process_all_screenshots()
        print(f"Processed {len(screenshot_candidates)} candidates from screenshots")
        
        # Step 3: Generate report
        print("Step 3: Generating processing report...")
        report = self.generate_processing_report()
        
        # Step 4: Export all candidates
        print("Step 4: Exporting all candidates...")
        export_path = self.export_candidates_to_json()
        
        print(f"\nProcessing complete!")
        print(f"Total candidates processed: {report['total_candidates']}")
        print(f"Report saved to: {self.processed_dir}")
        print(f"All candidates exported to: {export_path}")
        
        return {
            "report": report,
            "export_path": export_path,
            "json_candidates": len(json_candidates),
            "screenshot_candidates": len(screenshot_candidates)
        }

def main():
    """Main function to run the candidate processor."""
    processor = CandidateProcessor()
    
    try:
        results = processor.run_full_processing()
        
        # Print summary
        print("\n" + "="*50)
        print("CANDIDATE PROCESSING SUMMARY")
        print("="*50)
        print(f"Total Candidates: {results['report']['total_candidates']}")
        print(f"From JSON Files: {results['json_candidates']}")
        print(f"From Screenshots: {results['screenshot_candidates']}")
        print(f"Average OCR Confidence: {results['report']['average_ocr_confidence']:.2f}%")
        print(f"Top Skills: {', '.join([skill for skill, _ in results['report']['top_skills'][:5]])}")
        print(f"Export File: {results['export_path']}")
        print("="*50)
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        processor.log_processing("pipeline_error", str(e), False)
        sys.exit(1)

if __name__ == "__main__":
    main() 