import type { NextApiRequest, NextApiResponse } from 'next'
import { Applicant } from '../../types'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Applicant[] | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // In a real app, this would connect to your database
    // For now, we'll return mock data
    const applicants: Applicant[] = [
      {
        id: 1,
        name: "John Smith",
        title: "Senior Shopify Developer",
        location: "New York, NY",
        hourly_rate: "$45/hr",
        job_success: "98%",
        total_earned: "$12,450",
        hours_worked: "276",
        rating: 5,
        overview: "Experienced Shopify developer with 5+ years building custom e-commerce solutions.",
        skills: ["Shopify", "Liquid", "JavaScript", "React"],
        job_title: "Shopify Developer",
        status: "pending",
        created_at: "2025-01-19T10:00:00Z"
      }
    ]
    
    res.status(200).json(applicants)
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch applicants' })
  }
}
