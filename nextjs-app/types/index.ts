export interface Applicant {
  id: number;
  name: string;
  title: string;
  location: string;
  hourly_rate: string;
  job_success: string;
  total_earned: string;
  hours_worked: string;
  rating: number;
  overview: string;
  skills: string[];
  job_title: string;
  status: 'pending' | 'interview' | 'hired' | 'rejected';
  proposal_text?: string;
  portfolio_link?: string;
  profile_image?: string;
  created_at: string;
}

export interface Job {
  id: number;
  job_title: string;
  description: string;
  requirements: string[];
  applicant_count: number;
  created_at: string;
}

export interface Statistics {
  total_applicants: number;
  status_breakdown: {
    pending: number;
    interview: number;
    hired: number;
    rejected: number;
  };
  jobs_breakdown: Record<string, number>;
  average_rating: number;
  total_earned: string;
}
