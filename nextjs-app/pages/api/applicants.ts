import { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs'
import path from 'path'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  try {
    let applicants = []
    
    // Try multiple data sources in order of preference
    const dataSources = [
      // 1. Frontend data directory (most accessible)
      path.join(process.cwd(), 'data', 'candidates.json'),
      // 2. Latest perfected data file
      path.join(process.cwd(), '..', 'output', 'processed_candidates', 'perfected_all_applicants_20250720_203439.json'),
      // 3. Latest comprehensive data file
      path.join(process.cwd(), '..', 'output', 'processed_candidates', 'comprehensive_all_applicants_20250720_203300.json'),
      // 4. Fallback to any available data file
      path.join(process.cwd(), '..', 'output', 'processed_candidates', 'all_ranked_applicants_20250720_203047.json')
    ]
    
    for (const jsonPath of dataSources) {
      try {
        console.log('Trying data source:', jsonPath)
        
        if (fs.existsSync(jsonPath)) {
          const jsonData = fs.readFileSync(jsonPath, 'utf8')
          const parsedData = JSON.parse(jsonData)
          
          // Handle different data formats
          if (Array.isArray(parsedData)) {
            applicants = parsedData
          } else if (parsedData.applicants && Array.isArray(parsedData.applicants)) {
            applicants = parsedData.applicants
          } else {
            applicants = [parsedData]
          }
          
          console.log(`✅ Successfully loaded ${applicants.length} applicants from ${jsonPath}`)
          break
        }
      } catch (fileError: any) {
        console.log(`❌ Failed to load from ${jsonPath}:`, fileError?.message || 'Unknown error')
        continue
      }
    }
    
    // If no data sources worked, use fallback sample data
    if (applicants.length === 0) {
      console.log('⚠️ No data sources found, using sample data')
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

    console.log('📊 Final applicant count:', applicants.length)

    // Calculate stats
    const stats = {
      total: applicants.length,
      positions: new Set(applicants.map((a: any) => a.job_title || a.job_type)).size,
      averageRating: applicants.length > 0 
        ? (applicants.reduce((sum: number, a: any) => sum + (a.rating || a.ranking_score || 0), 0) / applicants.length).toFixed(1)
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
