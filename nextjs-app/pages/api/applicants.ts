import { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs'
import path from 'path'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  try {
    let applicants = []
    
    // Try to read from the JSON file
    try {
      const jsonPath = path.join(process.cwd(), '..', 'output', 'processed_candidates', 'all_ranked_applicants_20250720_201117.json')
      console.log('JSON path:', jsonPath)
      
      const jsonData = fs.readFileSync(jsonPath, 'utf8')
      const parsedData = JSON.parse(jsonData)
      applicants = parsedData.applicants || parsedData
    } catch (fileError: any) {
      console.log('File not found, using sample data:', fileError?.message || 'Unknown error')
      // Fallback to sample data for Vercel deployment
      applicants = [
        {
          name: "Sample Candidate",
          job_title: "UX Designer",
          rating: 4.5,
          total_earned: "$15,000",
          skills: ["Figma", "Adobe XD", "User Research"],
          experience: "3 years",
          location: "Remote"
        }
      ]
    }

    console.log('Found', applicants.length, 'applicants')

    // Calculate stats
    const stats = {
      total: applicants.length,
      positions: new Set(applicants.map((a: any) => a.job_title)).size,
      averageRating: applicants.length > 0 
        ? (applicants.reduce((sum: number, a: any) => sum + (a.rating || 0), 0) / applicants.length).toFixed(1)
        : 0,
      totalEarned: applicants.reduce((sum: number, a: any) => {
        const earned = a.total_earned ? parseFloat(a.total_earned.replace(/[^0-9.]/g, '')) : 0
        return sum + earned
      }, 0)
    }

    res.status(200).json({ applicants, stats })
  } catch (error) {
    console.error('API error:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}
