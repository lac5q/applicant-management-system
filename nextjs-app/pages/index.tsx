import React, { useState, useEffect, useCallback, useMemo } from 'react'
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
}

interface Stats {
  total: number
  positions: number
  averageRating: string
  totalEarned: number
}

interface Filters {
  search: string
  skills: string[]
  jobPosting: string
  location: string
  minRating: number
  maxHourlyRate: number
  minJobSuccess: number
  status: string
}

interface SortConfig {
  field: string
  direction: 'asc' | 'desc'
}

const Home = React.memo(function Home() {
  const [applicants, setApplicants] = useState<Applicant[]>([])
  const [stats, setStats] = useState<Stats>({
    total: 0,
    positions: 0,
    averageRating: '0',
    totalEarned: 0
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<Filters>({
    search: '',
    skills: [],
    jobPosting: '',
    location: '',
    minRating: 0,
    maxHourlyRate: 100,
    minJobSuccess: 0,
    status: ''
  })
  const [sortConfig, setSortConfig] = useState<SortConfig>({
    field: 'ranking_score',
    direction: 'desc'
  })
  const [expandedFilters, setExpandedFilters] = useState<{[key: string]: boolean}>({
    jobPosting: true,
    search: false,
    location: false,
    skills: false,
    rating: false,
    sorting: false
  })

  // Available sorting options
  const sortOptions = [
    { value: 'ranking_score', label: 'Ranking Score', icon: '🏆' },
    { value: 'rating', label: 'Rating', icon: '⭐' },
    { value: 'name', label: 'Name', icon: '👤' },
    { value: 'hourly_rate', label: 'Hourly Rate', icon: '💰' },
    { value: 'job_success', label: 'Job Success', icon: '📈' },
    { value: 'total_earned', label: 'Total Earned', icon: '💵' },
    { value: 'hours_worked', label: 'Hours Worked', icon: '⏰' },
    { value: 'jobs_completed', label: 'Jobs Completed', icon: '✅' },
    { value: 'location', label: 'Location', icon: '🌍' },
    { value: 'job_title', label: 'Job Title', icon: '💼' },
    { value: 'applied_date', label: 'Applied Date', icon: '📅' },
    { value: 'data_quality_score', label: 'Data Quality', icon: '📊' }
  ]

  // Sorting function
  const sortApplicants = useCallback((applicants: Applicant[], sortConfig: SortConfig) => {
    return [...applicants].sort((a, b) => {
      let aValue: any = a[sortConfig.field as keyof Applicant]
      let bValue: any = b[sortConfig.field as keyof Applicant]

      // Handle special cases for different field types
      switch (sortConfig.field) {
        case 'hourly_rate':
          // Extract numeric value from rate strings like "$35/hr"
          aValue = parseFloat(aValue?.replace(/[^0-9.]/g, '') || '0')
          bValue = parseFloat(bValue?.replace(/[^0-9.]/g, '') || '0')
          break
        case 'job_success':
          // Extract numeric value from success strings like "95% Job Success"
          aValue = parseFloat(aValue?.replace(/[^0-9.]/g, '') || '0')
          bValue = parseFloat(bValue?.replace(/[^0-9.]/g, '') || '0')
          break
        case 'total_earned':
          // Extract numeric value from earned strings like "$15,000+ earned"
          aValue = parseFloat(aValue?.replace(/[^0-9.]/g, '') || '0')
          bValue = parseFloat(bValue?.replace(/[^0-9.]/g, '') || '0')
          break
        case 'hours_worked':
          // Extract numeric value from hours strings like "500 total hours"
          aValue = parseFloat(aValue?.replace(/[^0-9.]/g, '') || '0')
          bValue = parseFloat(bValue?.replace(/[^0-9.]/g, '') || '0')
          break
        case 'jobs_completed':
          // Extract numeric value from jobs strings like "25 completed jobs"
          aValue = parseFloat(aValue?.replace(/[^0-9.]/g, '') || '0')
          bValue = parseFloat(bValue?.replace(/[^0-9.]/g, '') || '0')
          break
        case 'name':
        case 'location':
        case 'job_title':
          // String comparison
          aValue = (aValue || '').toLowerCase()
          bValue = (bValue || '').toLowerCase()
          break
        case 'applied_date':
          // Date comparison
          aValue = new Date(aValue || '1970-01-01').getTime()
          bValue = new Date(bValue || '1970-01-01').getTime()
          break
        default:
          // Numeric comparison for rating, ranking_score, data_quality_score
          aValue = parseFloat(aValue || '0')
          bValue = parseFloat(bValue || '0')
      }

      // Handle null/undefined values
      if (aValue === null || aValue === undefined) aValue = sortConfig.field.includes('rate') ? 0 : ''
      if (bValue === null || bValue === undefined) bValue = sortConfig.field.includes('rate') ? 0 : ''

      // Sort based on direction
      if (sortConfig.direction === 'asc') {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0
      } else {
        return aValue < bValue ? 1 : aValue > bValue ? -1 : 0
      }
    })
  }, [])

  // Handle sort change
  const handleSortChange = useCallback((field: string) => {
    setSortConfig(prev => ({
      field,
      direction: prev.field === field && prev.direction === 'desc' ? 'asc' : 'desc'
    }))
  }, [])

  // Get sort direction indicator
  const getSortIndicator = useCallback((field: string) => {
    if (sortConfig.field !== field) return '↕️'
    return sortConfig.direction === 'asc' ? '↑' : '↓'
  }, [sortConfig])

  // Memoize filter functions to prevent unnecessary re-renders
  const toggleFilterSection = useCallback((section: string) => {
    setExpandedFilters(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }, [])

  const toggleSkill = useCallback((skill: string) => {
    setFilters(prev => ({
      ...prev,
      skills: prev.skills.includes(skill) 
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }))
  }, [])

  const clearFilters = useCallback(() => {
    setFilters({
      search: '',
      skills: [],
      jobPosting: '',
      location: '',
      minRating: 0,
      maxHourlyRate: 100,
      minJobSuccess: 0,
      status: ''
    })
  }, [])

  const hasActiveFilters = useCallback(() => {
    return filters.search || 
           filters.skills.length > 0 || 
           filters.jobPosting || 
           filters.location || 
           filters.minRating > 0 || 
           filters.maxHourlyRate < 100 || 
           filters.minJobSuccess > 0
  }, [filters])

  // Available filter options
  const availableSkills = ['UI/UX Design', 'Figma', 'React', 'Node.js', 'Shopify', 'JavaScript', 'Adobe XD', 'Prototyping', 'Webflow', 'Vue.js', 'MongoDB', 'HTML', 'CSS', 'Liquid', 'Graphic Design', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'User Research', 'Wireframing', 'Responsive Design', 'Conversion Rate Optimization', 'Landing Page Design', 'A/B Testing', 'Web Design', 'Mobile App Design', 'User Interface Design', 'Express.js']
  const availableJobPostings = [
    'URGENT: Contract-to-hire Shopify Developer + UX Specialist - Start This Week!', 
    'URGENT Contract-to-Hire UX/Conversion Designer - Start This Week'
  ]
  const availableLocations = ['Delhi, India', 'India', 'Kolkata, India', 'Kyiv, Ukraine', 'Istanbul, Turkey', 'Lahore, Pakistan']
  const availableStatuses = ['pending', 'Active', 'Inactive']

  useEffect(() => {
    const fetchApplicants = async () => {
      try {
        console.log('Fetching applicants from API...')
        const response = await fetch('/api/applicants/')
        console.log('API response status:', response.status)
        
        if (!response.ok) {
          throw new Error(`Failed to fetch applicants: ${response.status}`)
        }
        
        const data = await response.json()
        console.log('API data received:', data)
        console.log('Number of applicants:', data.applicants?.length)
        
        setApplicants(data.applicants)
        setStats(data.stats)
        setLoading(false)
      } catch (err) {
        console.error('Error fetching applicants:', err)
        setError(err instanceof Error ? err.message : 'Failed to load applicants')
        setLoading(false)
      }
    }

    fetchApplicants()
  }, [])

  // Apply filters and sorting using useMemo for better performance
  const filteredAndSortedApplicants = useMemo(() => {
    // First apply filters
    const filtered = applicants.filter(applicant => {
      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase()
        const searchableText = `${applicant.name} ${applicant.title} ${applicant.location} ${applicant.skills.join(' ')} ${applicant.overview}`.toLowerCase()
        if (!searchableText.includes(searchLower)) return false
      }

      // Skills filter
      if (filters.skills.length > 0) {
        const hasRequiredSkill = filters.skills.some(skill => 
          applicant.skills.some(applicantSkill => 
            applicantSkill.toLowerCase().includes(skill.toLowerCase())
          )
        )
        if (!hasRequiredSkill) return false
      }

      // Job posting filter
      if (filters.jobPosting && applicant.job_title !== filters.jobPosting) {
        return false
      }

      // Location filter
      if (filters.location && applicant.location !== filters.location) {
        return false
      }

      // Rating filter
      if (filters.minRating > 0 && applicant.rating < filters.minRating) {
        return false
      }

      // Hourly rate filter
      if (filters.maxHourlyRate < 100) {
        const rate = parseFloat(applicant.hourly_rate.replace(/[^0-9.]/g, ''))
        if (rate > filters.maxHourlyRate) return false
      }

      // Job success filter
      if (filters.minJobSuccess > 0) {
        const successRate = parseFloat(applicant.job_success.replace(/[^0-9.]/g, ''))
        if (successRate < filters.minJobSuccess) return false
      }

      // Status filter
      if (filters.status && applicant.status !== filters.status) {
        return false
      }

      return true
    })

    // Then apply sorting
    return sortApplicants(filtered, sortConfig)
  }, [applicants, filters, sortConfig, sortApplicants])





  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading applicant data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl mb-4">⚠️ Error Loading Data</div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Applicant Management System</title>
        <meta name="description" content="Modern hiring platform with intelligent filtering and portfolio access" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Applicant Management System
                </h1>
                <p className="text-gray-600 mt-1">
                  Real applicant data from Upwork screenshots with advanced filtering
                </p>
              </div>
              <div className="flex space-x-4">
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                  Add Applicant
                </button>
                <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg transition-colors">
                  Export Data
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Extraction Status Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow mb-8">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">📊 Extraction Status</h2>
              <p className="text-sm text-gray-600 mt-1">Progress tracking for Upwork screenshot processing</p>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">60</div>
                  <div className="text-sm text-gray-600">Expected</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{filteredAndSortedApplicants.length}</div>
                  <div className="text-sm text-gray-600">Extracted</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{filteredAndSortedApplicants.length}</div>
                  <div className="text-sm text-gray-600">Saved</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{filteredAndSortedApplicants.filter(a => a.rating > 0).length}</div>
                  <div className="text-sm text-gray-600">Rated</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600">{((filteredAndSortedApplicants.length / 60) * 100).toFixed(1)}%</div>
                  <div className="text-sm text-gray-600">Complete</div>
                </div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-300" 
                  style={{ width: `${(filteredAndSortedApplicants.length / 60) * 100}%` }}
                ></div>
              </div>
              <div className="flex justify-between items-center text-sm text-gray-600">
                <span>🟡 Extraction in progress - {60 - filteredAndSortedApplicants.length} candidates remaining</span>
                <a 
                  href="/output/reports/extraction_status_dashboard.html" 
                  target="_blank"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  View Detailed Dashboard →
                </a>
              </div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Applicants</p>
                  <p className="text-2xl font-semibold text-gray-900">{filteredAndSortedApplicants.length} / {stats.total}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-green-100 text-green-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Job Positions</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.positions}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Average Rating</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.averageRating}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Earned</p>
                  <p className="text-2xl font-semibold text-gray-900">${((stats?.totalEarned || 0) as number).toLocaleString()}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Filters Section */}
          <div className="bg-white rounded-lg shadow mb-8">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-900">
                  Filters {hasActiveFilters() && (
                    <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Active
                    </span>
                  )}
                </h2>
                {hasActiveFilters() && (
                  <button 
                    onClick={clearFilters}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Clear All Filters
                  </button>
                )}
              </div>
            </div>
            
            <div className="p-6 space-y-4">
              {/* Job Posting Filter - Always Visible */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Posting {filters.jobPosting && (
                    <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      ✓
                    </span>
                  )}
                </label>
                <select
                  value={filters.jobPosting}
                  onChange={(e) => setFilters(prev => ({ ...prev, jobPosting: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Job Postings</option>
                  {availableJobPostings.map(posting => (
                    <option key={posting} value={posting}>{posting}</option>
                  ))}
                </select>
              </div>

              {/* Sorting Section - Always Visible */}
              <div className="border-t border-gray-200 pt-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By {sortConfig.field !== 'ranking_score' && (
                    <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {sortOptions.find(opt => opt.value === sortConfig.field)?.label}
                    </span>
                  )}
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <select
                    value={sortConfig.field}
                    onChange={(e) => handleSortChange(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {sortOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.icon} {option.label}
                      </option>
                    ))}
                  </select>
                  <button
                    onClick={() => setSortConfig(prev => ({ ...prev, direction: prev.direction === 'asc' ? 'desc' : 'asc' }))}
                    className="px-4 py-2 border border-gray-300 rounded-md bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center justify-center"
                  >
                    <span className="mr-2">{getSortIndicator(sortConfig.field)}</span>
                    {sortConfig.direction === 'asc' ? 'Ascending' : 'Descending'}
                  </button>
                </div>
                <div className="mt-2 text-xs text-gray-500">
                  Current: {sortOptions.find(opt => opt.value === sortConfig.field)?.icon} {sortOptions.find(opt => opt.value === sortConfig.field)?.label} ({sortConfig.direction === 'asc' ? 'Low to High' : 'High to Low'})
                </div>
              </div>

              {/* Search Filter - Collapsible */}
              <div className="border-t border-gray-200 pt-4">
                <button
                  onClick={() => toggleFilterSection('search')}
                  className="flex items-center justify-between w-full text-left"
                >
                  <span className="text-sm font-medium text-gray-700">
                    Search {filters.search && (
                      <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        ✓
                      </span>
                    )}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${expandedFilters.search ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedFilters.search && (
                  <div className="mt-3">
                    <input
                      type="text"
                      placeholder="Search by name, title, skills, or overview..."
                      value={filters.search}
                      onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                )}
              </div>

              {/* Location Filter - Collapsible */}
              <div className="border-t border-gray-200 pt-4">
                <button
                  onClick={() => toggleFilterSection('location')}
                  className="flex items-center justify-between w-full text-left"
                >
                  <span className="text-sm font-medium text-gray-700">
                    Location {filters.location && (
                      <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        ✓
                      </span>
                    )}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${expandedFilters.location ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedFilters.location && (
                  <div className="mt-3">
                    <select
                      value={filters.location}
                      onChange={(e) => setFilters(prev => ({ ...prev, location: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">All Locations</option>
                      {availableLocations.map(location => (
                        <option key={location} value={location}>{location}</option>
                      ))}
                    </select>
                  </div>
                )}
              </div>

              {/* Skills Filter - Collapsible */}
              <div className="border-t border-gray-200 pt-4">
                <button
                  onClick={() => toggleFilterSection('skills')}
                  className="flex items-center justify-between w-full text-left"
                >
                  <span className="text-sm font-medium text-gray-700">
                    Required Skills {filters.skills.length > 0 && `(${filters.skills.length} selected)`}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${expandedFilters.skills ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedFilters.skills && (
                  <div className="mt-3">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 max-h-48 overflow-y-auto">
                      {availableSkills.map(skill => (
                        <label key={skill} className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={filters.skills.includes(skill)}
                            onChange={() => toggleSkill(skill)}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-700">{skill}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Rating and Rate Filters - Collapsible */}
              <div className="border-t border-gray-200 pt-4">
                <button
                  onClick={() => toggleFilterSection('rating')}
                  className="flex items-center justify-between w-full text-left"
                >
                  <span className="text-sm font-medium text-gray-700">
                    Rating & Rate Filters {(filters.minRating > 0 || filters.maxHourlyRate < 100 || filters.minJobSuccess > 0) && (
                      <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        ✓
                      </span>
                    )}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${expandedFilters.rating ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedFilters.rating && (
                  <div className="mt-3">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Minimum Rating</label>
                        <select
                          value={filters.minRating}
                          onChange={(e) => setFilters(prev => ({ ...prev, minRating: Number(e.target.value) }))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value={0}>Any Rating</option>
                          <option value={1}>1+ Stars</option>
                          <option value={2}>2+ Stars</option>
                          <option value={3}>3+ Stars</option>
                          <option value={4}>4+ Stars</option>
                          <option value={5}>5 Stars</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Max Hourly Rate</label>
                        <select
                          value={filters.maxHourlyRate}
                          onChange={(e) => setFilters(prev => ({ ...prev, maxHourlyRate: Number(e.target.value) }))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value={100}>Any Rate</option>
                          <option value={15}>$15/hr or less</option>
                          <option value={20}>$20/hr or less</option>
                          <option value={25}>$25/hr or less</option>
                          <option value={30}>$30/hr or less</option>
                          <option value={40}>$40/hr or less</option>
                          <option value={50}>$50/hr or less</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Min Job Success</label>
                        <select
                          value={filters.minJobSuccess}
                          onChange={(e) => setFilters(prev => ({ ...prev, minJobSuccess: Number(e.target.value) }))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value={0}>Any Success Rate</option>
                          <option value={90}>90%+</option>
                          <option value={95}>95%+</option>
                          <option value={98}>98%+</option>
                          <option value={99}>99%+</option>
                          <option value={100}>100%</option>
                        </select>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Applicants List */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    Filtered Applicants ({filteredAndSortedApplicants.length} of {stats.total})
                  </h2>
                  <p className="text-sm text-gray-600 mt-1">Showing applicants from Upwork job postings</p>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600">
                    Sorted by: {sortOptions.find(opt => opt.value === sortConfig.field)?.icon} {sortOptions.find(opt => opt.value === sortConfig.field)?.label}
                  </div>
                  <div className="text-xs text-gray-500">
                    {sortConfig.direction === 'asc' ? 'Low to High' : 'High to Low'}
                  </div>
                </div>
              </div>
            </div>
            <div className="divide-y divide-gray-200">
              {filteredAndSortedApplicants.length === 0 ? (
                <div className="px-6 py-8 text-center">
                  <p className="text-gray-500">No applicants match your current filters.</p>
                  <button 
                    onClick={clearFilters}
                    className="mt-2 text-blue-600 hover:text-blue-800"
                  >
                    Clear filters to see all applicants
                  </button>
                </div>
              ) : (
                filteredAndSortedApplicants.map((applicant) => (
                  <Link key={applicant.id} href={`/applicant/${applicant.id}`} className="block">
                    <div className="px-6 py-4 hover:bg-gray-50 transition-colors cursor-pointer">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="flex-shrink-0">
                            <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                              <span className="text-blue-600 font-semibold text-lg">
                                {applicant.name.split(' ').map(n => n[0]).join('')}
                              </span>
                            </div>
                          </div>
                          <div>
                            <h3 className="text-lg font-medium text-gray-900">{applicant.name}</h3>
                            <p className="text-sm text-gray-600">{applicant.title}</p>
                            <p className="text-sm text-gray-500">{applicant.location}</p>
                            <p className="text-xs text-gray-400 mt-1">{applicant.job_title}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <div className="text-right">
                            <p className="text-sm font-medium text-gray-900">{applicant.hourly_rate}</p>
                            <p className="text-sm text-gray-600">{applicant.job_success}</p>
                            <p className="text-xs text-gray-500">{applicant.total_earned}</p>
                          </div>
                          <div className="flex items-center">
                            <span className="text-yellow-400">★</span>
                            <span className="ml-1 text-sm text-gray-600">{applicant.rating}</span>
                          </div>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                            applicant.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                          }`}>
                            {applicant.status}
                          </span>
                        </div>
                      </div>
                      <div className="mt-3">
                        <div className="flex flex-wrap gap-2">
                          {applicant.skills.slice(0, 4).map((skill, index) => (
                            <span key={index} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                              {skill}
                            </span>
                          ))}
                          {applicant.skills.length > 4 && (
                            <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                              +{applicant.skills.length - 4} more
                            </span>
                          )}
                        </div>
                      </div>
                      {applicant.overview && (
                        <div className="mt-3">
                          <p className="text-sm text-gray-600 line-clamp-2">{applicant.overview}</p>
                        </div>
                      )}
                    </div>
                  </Link>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
})

export default Home 