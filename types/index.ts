export interface Applicant {
  id: number;
  upwork_id?: string | null;
  name: string;
  title: string;
  location: string;
  hourly_rate: string;
  job_success: string;
  total_earned: string;
  hours_worked: string;
  jobs_completed?: string;
  overview: string;
  skills: string[];
  job_title: string | null;
  status: 'pending' | 'interview' | 'hired' | 'rejected';
  rating: number;
  proposal_text?: string | null;
  portfolio_link?: string | null;
  profile_image?: string | null;
  created_at: string;
  updated_at?: string;
  recommendation?: string | null;
}

export interface Job {
  id: number;
  job_title: string;
  description?: string;
  requirements?: string[];
  applicant_count: number;
  created_at: string;
  updated_at?: string;
}

export interface Statistics {
  total_applicants: number;
  status_breakdown: {
    pending: number;
    interview: number;
    hired: number;
    rejected: number;
  };
  rating_breakdown?: Record<string, number>;
  jobs_breakdown: Record<string, number>;
  average_rating?: number;
  total_earned?: string;
} 