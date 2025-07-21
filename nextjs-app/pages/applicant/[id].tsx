import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'

interface Applicant {
  id: string
  name: string
  title: string
  location: string
  hourly_rate: string
  job_success: string
  total_earned: string
  hours_worked: string
  jobs_completed: string
  skills: string[]
  overview: string
  proposal_text: string
  job_title: string
  profile_url: string
  status: string
  rating: number
  applied_date: string
  notes: string
  profile_image: string
  screenshot_source: string
  portfolio_links: string[]
  work_samples: string[]
  processed_at: string
  source_file: string
  data_quality_score: number
  ranking_score?: number
}

interface RatingBreakdown {
  dimension: string
  score: number
  maxScore: number
  percentage: number
  description: string
  icon: string
}

const ApplicantDetail = () => {
  const router = useRouter()
  const { id } = router.query
  const [applicant, setApplicant] = useState<Applicant | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return

    const fetchApplicant = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/applicants/')
        
        if (!response.ok) {
          throw new Error(`Failed to fetch applicants: ${response.status}`)
        }
        
        const data = await response.json()
        const foundApplicant = data.applicants.find((a: Applicant) => a.id === id)
        
        if (!foundApplicant) {
          throw new Error('Applicant not found')
        }
        
        setApplicant(foundApplicant)
      } catch (err) {
        console.error('Error fetching applicant:', err)
        setError(err instanceof Error ? err.message : 'Failed to load applicant')
      } finally {
        setLoading(false)
      }
    }

    fetchApplicant()
  }, [id])

  // Calculate rating breakdown based on available data
  const getRatingBreakdown = (applicant: Applicant): RatingBreakdown[] => {
    const breakdown: RatingBreakdown[] = []

    // Job Success Rating
    const jobSuccessRate = parseFloat(applicant.job_success?.replace(/[^0-9.]/g, '') || '0')
    breakdown.push({
      dimension: 'Job Success Rate',
      score: jobSuccessRate,
      maxScore: 100,
      percentage: jobSuccessRate,
      description: 'Success rate on completed jobs',
      icon: '📈'
    })

    // Hours Worked Rating
    const hoursWorked = parseFloat(applicant.hours_worked?.replace(/[^0-9.]/g, '') || '0')
    const hoursScore = Math.min(hoursWorked / 1000 * 100, 100) // Normalize to 1000 hours = 100%
    breakdown.push({
      dimension: 'Experience Level',
      score: hoursScore,
      maxScore: 100,
      percentage: hoursScore,
      description: 'Based on total hours worked',
      icon: '⏰'
    })

    // Jobs Completed Rating
    const jobsCompleted = parseFloat(applicant.jobs_completed?.replace(/[^0-9.]/g, '') || '0')
    const jobsScore = Math.min(jobsCompleted / 50 * 100, 100) // Normalize to 50 jobs = 100%
    breakdown.push({
      dimension: 'Project Experience',
      score: jobsScore,
      maxScore: 100,
      percentage: jobsScore,
      description: 'Based on number of completed projects',
      icon: '✅'
    })

    // Skills Match Rating (based on relevant skills)
    const relevantSkills = ['UI/UX Design', 'Figma', 'React', 'Shopify', 'JavaScript', 'Adobe XD', 'Prototyping', 'Webflow', 'Conversion Rate Optimization', 'Landing Page Design']
    const matchingSkills = applicant.skills.filter(skill => 
      relevantSkills.some(relevant => skill.toLowerCase().includes(relevant.toLowerCase()))
    )
    const skillsScore = (matchingSkills.length / relevantSkills.length) * 100
    breakdown.push({
      dimension: 'Skills Match',
      score: skillsScore,
      maxScore: 100,
      percentage: skillsScore,
      description: 'Relevance of skills to job requirements',
      icon: '🛠️'
    })

    // Data Quality Rating
    breakdown.push({
      dimension: 'Data Quality',
      score: applicant.data_quality_score || 0,
      maxScore: 100,
      percentage: applicant.data_quality_score || 0,
      description: 'Completeness and accuracy of profile data',
      icon: '📊'
    })

    // Overall Rating (if available)
    if (applicant.rating > 0) {
      breakdown.push({
        dimension: 'Overall Rating',
        score: applicant.rating,
        maxScore: 5,
        percentage: (applicant.rating / 5) * 100,
        description: 'Client feedback and platform rating',
        icon: '⭐'
      })
    }

    return breakdown
  }

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  // Format date
  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A'
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    } catch {
      return dateString
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading applicant details...</p>
        </div>
      </div>
    )
  }

  if (error || !applicant) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl mb-4">⚠️ Error Loading Applicant</div>
          <p className="text-gray-600 mb-4">{error || 'Applicant not found'}</p>
          <Link href="/" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
            Back to Applicants
          </Link>
        </div>
      </div>
    )
  }

  const ratingBreakdown = getRatingBreakdown(applicant)
  const averageRating = ratingBreakdown.reduce((sum, item) => sum + item.percentage, 0) / ratingBreakdown.length

  return (
    <>
      <Head>
        <title>{applicant.name} - Applicant Profile | Recruiting System</title>
        <meta name="description" content={`Detailed profile for ${applicant.name} - ${applicant.title}`} />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center">
                <Link href="/" className="text-blue-600 hover:text-blue-800 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  Back to Applicants
                </Link>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-600">Applicant Profile</div>
                <div className="text-lg font-semibold text-gray-900">{applicant.name}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              {/* Basic Info Card */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start space-x-6">
                  <div className="flex-shrink-0">
                    <div className="h-20 w-20 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-blue-600 font-semibold text-2xl">
                        {applicant.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                  </div>
                  <div className="flex-1">
                    <h1 className="text-3xl font-bold text-gray-900">{applicant.name}</h1>
                    <p className="text-xl text-gray-600 mt-1">{applicant.title}</p>
                    <p className="text-gray-500 mt-2">{applicant.location}</p>
                    <div className="flex items-center mt-4 space-x-4">
                      <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(applicant.status)}`}>
                        {applicant.status}
                      </span>
                      {applicant.rating > 0 && (
                        <div className="flex items-center">
                          <span className="text-yellow-400 text-lg">★</span>
                          <span className="ml-1 text-sm text-gray-600">{applicant.rating}/5</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Rating Breakdown */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Rating Breakdown</h2>
                <div className="space-y-6">
                  {ratingBreakdown.map((rating, index) => (
                    <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <span className="text-2xl mr-3">{rating.icon}</span>
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900">{rating.dimension}</h3>
                            <p className="text-sm text-gray-600">{rating.description}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-blue-600">{rating.score.toFixed(1)}</div>
                          <div className="text-sm text-gray-500">/ {rating.maxScore}</div>
                        </div>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-300" 
                          style={{ width: `${rating.percentage}%` }}
                        ></div>
                      </div>
                      <div className="text-right mt-1">
                        <span className="text-sm text-gray-600">{rating.percentage.toFixed(1)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-semibold text-gray-900">Average Rating</span>
                    <span className="text-3xl font-bold text-green-600">{averageRating.toFixed(1)}%</span>
                  </div>
                </div>
              </div>

              {/* Overview */}
              {applicant.overview && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Overview</h2>
                  <p className="text-gray-700 leading-relaxed">{applicant.overview}</p>
                </div>
              )}

              {/* Proposal */}
              {applicant.proposal_text && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Proposal</h2>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{applicant.proposal_text}</p>
                  </div>
                </div>
              )}

              {/* Skills */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Skills</h2>
                <div className="flex flex-wrap gap-2">
                  {applicant.skills.map((skill, index) => (
                    <span key={index} className="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-full">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Key Metrics */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Metrics</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Hourly Rate</span>
                    <span className="font-semibold text-green-600">{applicant.hourly_rate}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Job Success</span>
                    <span className="font-semibold text-blue-600">{applicant.job_success}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Total Earned</span>
                    <span className="font-semibold text-purple-600">{applicant.total_earned}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Hours Worked</span>
                    <span className="font-semibold text-orange-600">{applicant.hours_worked}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Jobs Completed</span>
                    <span className="font-semibold text-indigo-600">{applicant.jobs_completed}</span>
                  </div>
                </div>
              </div>

              {/* Job Information */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Job Information</h3>
                <div className="space-y-3">
                  <div>
                    <span className="text-sm text-gray-600">Applied for</span>
                    <p className="text-sm font-medium text-gray-900 mt-1">{applicant.job_title}</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-600">Applied Date</span>
                    <p className="text-sm font-medium text-gray-900 mt-1">{formatDate(applicant.applied_date)}</p>
                  </div>
                  <div>
                    <span className="text-sm text-gray-600">Data Quality Score</span>
                    <p className="text-sm font-medium text-gray-900 mt-1">{applicant.data_quality_score}/100</p>
                  </div>
                  {applicant.ranking_score && (
                    <div>
                      <span className="text-sm text-gray-600">Ranking Score</span>
                      <p className="text-sm font-medium text-gray-900 mt-1">{applicant.ranking_score.toFixed(2)}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
                <div className="space-y-3">
                  {applicant.profile_url && (
                    <a 
                      href={applicant.profile_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center justify-center"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      View Upwork Profile
                    </a>
                  )}
                  <button className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
                    Contact Candidate
                  </button>
                  <button className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                    Add to Shortlist
                  </button>
                </div>
              </div>

              {/* Technical Details */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Technical Details</h3>
                <div className="space-y-3 text-sm">
                  <div>
                    <span className="text-gray-600">ID:</span>
                    <p className="font-mono text-gray-900">{applicant.id}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Processed:</span>
                    <p className="text-gray-900">{formatDate(applicant.processed_at)}</p>
                  </div>
                  <div>
                    <span className="text-gray-600">Source File:</span>
                    <p className="font-mono text-gray-900 text-xs">{applicant.source_file}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default ApplicantDetail 