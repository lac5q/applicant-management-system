#!/usr/bin/env python3
"""
Applicant Database Manager - SQLite database for tracking all applicants
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ApplicantDatabaseManager:
    """Manage applicant data in SQLite database"""
    
    def __init__(self, db_path: str = "../output/applicants/applicants.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT UNIQUE NOT NULL,
                job_url TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create applicants table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applicants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upwork_id TEXT UNIQUE,
                name TEXT NOT NULL,
                title TEXT,
                location TEXT,
                hourly_rate TEXT,
                job_success TEXT,
                total_earned TEXT,
                hours_worked TEXT,
                jobs_completed TEXT,
                overview TEXT,
                proposal_text TEXT,
                job_id INTEGER,
                applied_date DATE,
                status TEXT DEFAULT 'pending',
                rating INTEGER DEFAULT 0,
                notes TEXT,
                profile_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        ''')
        
        # Create skills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                applicant_id INTEGER,
                skill_name TEXT,
                FOREIGN KEY (applicant_id) REFERENCES applicants (id)
            )
        ''')
        
        # Create rating_details table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                applicant_id INTEGER,
                experience_rating INTEGER,
                skills_match_rating INTEGER,
                portfolio_rating INTEGER,
                communication_rating INTEGER,
                pricing_rating INTEGER,
                availability_rating INTEGER,
                overall_rating INTEGER,
                rating_explanation TEXT,
                recommendation TEXT,
                rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (applicant_id) REFERENCES applicants (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")
    
    def add_job(self, job_title: str, job_url: str = None, category: str = None) -> int:
        """Add a new job to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO jobs (job_title, job_url, category, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (job_title, job_url, category, datetime.now()))
        
        job_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Added job: {job_title} (ID: {job_id})")
        return job_id
    
    def add_applicant(self, applicant_data: Dict[str, Any]) -> int:
        """Add a new applicant to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get or create job
        job_id = self.add_job(applicant_data['job_title'])
        
        # Insert applicant
        cursor.execute('''
            INSERT OR REPLACE INTO applicants (
                upwork_id, name, title, location, hourly_rate, job_success,
                total_earned, hours_worked, jobs_completed, overview,
                proposal_text, job_id, applied_date, status, rating,
                notes, profile_url, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            applicant_data.get('id'),
            applicant_data['name'],
            applicant_data['title'],
            applicant_data['location'],
            applicant_data['hourly_rate'],
            applicant_data['job_success'],
            applicant_data['total_earned'],
            applicant_data['hours_worked'],
            applicant_data['jobs_completed'],
            applicant_data['overview'],
            applicant_data.get('proposal_text', ''),
            job_id,
            applicant_data.get('applied_date', datetime.now().strftime('%Y-%m-%d')),
            applicant_data.get('status', 'pending'),
            applicant_data.get('rating', 0),
            applicant_data.get('notes', ''),
            applicant_data.get('profile_url', ''),
            datetime.now()
        ))
        
        applicant_id = cursor.lastrowid
        
        # Add skills
        if 'skills' in applicant_data:
            cursor.execute('DELETE FROM skills WHERE applicant_id = ?', (applicant_id,))
            for skill in applicant_data['skills']:
                cursor.execute('''
                    INSERT INTO skills (applicant_id, skill_name)
                    VALUES (?, ?)
                ''', (applicant_id, skill))
        
        # Add rating details if available
        if 'rating_data' in applicant_data:
            rating_data = applicant_data['rating_data']
            cursor.execute('''
                INSERT OR REPLACE INTO rating_details (
                    applicant_id, experience_rating, skills_match_rating,
                    portfolio_rating, communication_rating, pricing_rating,
                    availability_rating, overall_rating, rating_explanation,
                    recommendation, rated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                applicant_id,
                rating_data['ratings'].get('experience', 0),
                rating_data['ratings'].get('skills_match', 0),
                rating_data['ratings'].get('portfolio_quality', 0),
                rating_data['ratings'].get('communication', 0),
                rating_data['ratings'].get('pricing', 0),
                rating_data['ratings'].get('availability', 0),
                rating_data['ratings'].get('overall', 0),
                json.dumps(rating_data.get('explanation', {})),
                rating_data.get('recommendation', ''),
                datetime.now()
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Added applicant: {applicant_data['name']} (ID: {applicant_id})")
        return applicant_id
    
    def get_all_applicants(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get all applicants with optional filters"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                a.*,
                j.job_title,
                j.category,
                GROUP_CONCAT(s.skill_name) as skills,
                rd.experience_rating,
                rd.skills_match_rating,
                rd.portfolio_rating,
                rd.communication_rating,
                rd.pricing_rating,
                rd.availability_rating,
                rd.overall_rating,
                rd.rating_explanation,
                rd.recommendation
            FROM applicants a
            LEFT JOIN jobs j ON a.job_id = j.id
            LEFT JOIN skills s ON a.id = s.applicant_id
            LEFT JOIN rating_details rd ON a.id = rd.applicant_id
        '''
        
        where_conditions = []
        params = []
        
        if filters:
            if filters.get('job_title'):
                where_conditions.append("j.job_title = ?")
                params.append(filters['job_title'])
            
            if filters.get('status'):
                where_conditions.append("a.status = ?")
                params.append(filters['status'])
            
            if filters.get('min_rating'):
                where_conditions.append("a.rating >= ?")
                params.append(filters['min_rating'])
            
            if filters.get('search'):
                where_conditions.append("(a.name LIKE ? OR a.title LIKE ? OR a.overview LIKE ?)")
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term, search_term])
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        query += " GROUP BY a.id ORDER BY a.rating DESC, a.name"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        applicants = []
        for row in rows:
            applicant = dict(row)
            if applicant['skills']:
                applicant['skills'] = applicant['skills'].split(',')
            else:
                applicant['skills'] = []
            
            if applicant['rating_explanation']:
                applicant['rating_explanation'] = json.loads(applicant['rating_explanation'])
            
            applicants.append(applicant)
        
        conn.close()
        return applicants
    
    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get all jobs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT j.*, COUNT(a.id) as applicant_count
            FROM jobs j
            LEFT JOIN applicants a ON j.id = a.job_id
            GROUP BY j.id
            ORDER BY j.created_at DESC
        ''')
        
        jobs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jobs
    
    def update_applicant_status(self, applicant_id: int, status: str):
        """Update applicant status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE applicants 
            SET status = ?, updated_at = ?
            WHERE id = ?
        ''', (status, datetime.now(), applicant_id))
        
        conn.commit()
        conn.close()
        print(f"✅ Updated applicant {applicant_id} status to: {status}")
    
    def update_applicant_rating(self, applicant_id: int, rating: int, notes: str = None):
        """Update applicant rating and notes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE applicants 
            SET rating = ?, notes = ?, updated_at = ?
            WHERE id = ?
        ''', (rating, notes, datetime.now(), applicant_id))
        
        conn.commit()
        conn.close()
        print(f"✅ Updated applicant {applicant_id} rating to: {rating}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total applicants
        cursor.execute('SELECT COUNT(*) FROM applicants')
        total_applicants = cursor.fetchone()[0]
        
        # Status breakdown
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM applicants 
            GROUP BY status
        ''')
        status_breakdown = dict(cursor.fetchall())
        
        # Rating breakdown
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN rating >= 4 THEN 'Top (4-5 stars)'
                    WHEN rating >= 3 THEN 'Good (3-4 stars)'
                    WHEN rating >= 2 THEN 'Fair (2-3 stars)'
                    ELSE 'Poor (1-2 stars)'
                END as rating_category,
                COUNT(*) as count
            FROM applicants 
            GROUP BY rating_category
        ''')
        rating_breakdown = dict(cursor.fetchall())
        
        # Jobs breakdown
        cursor.execute('''
            SELECT j.job_title, COUNT(a.id) as applicant_count
            FROM jobs j
            LEFT JOIN applicants a ON j.id = a.job_id
            GROUP BY j.id
        ''')
        jobs_breakdown = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_applicants': total_applicants,
            'status_breakdown': status_breakdown,
            'rating_breakdown': rating_breakdown,
            'jobs_breakdown': jobs_breakdown
        } 