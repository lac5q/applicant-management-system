import { useState, useEffect } from 'react'
import { Search, Filter } from 'lucide-react'
import { Applicant, Job } from '../types'

interface FiltersProps {
  applicants: Applicant[]
  jobs: Job[]
  onFilter: (filtered: Applicant[]) => void
}

export default function Filters({ applicants, jobs, onFilter }: FiltersProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [jobFilter, setJobFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [ratingFilter, setRatingFilter] = useState('')
  const [rateFilter, setRateFilter] = useState('')

  useEffect(() => {
    let filtered = [...applicants]

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(applicant =>
        applicant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        applicant.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        applicant.skills.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase())) ||
        applicant.overview.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Job filter
    if (jobFilter) {
      filtered = filtered.filter(applicant => applicant.job_title === jobFilter)
    }

    // Status filter
    if (statusFilter) {
      filtered = filtered.filter(applicant => applicant.status === statusFilter)
    }

    // Rating filter
    if (ratingFilter) {
      const minRating = parseInt(ratingFilter)
      filtered = filtered.filter(applicant => applicant.rating >= minRating)
    }

    // Rate filter
    if (rateFilter) {
      filtered = filtered.filter(applicant => {
        const rate = parseFloat(applicant.hourly_rate.replace('$', '').replace('/hr', ''))
        switch (rateFilter) {
          case '0-25': return rate <= 25
          case '25-40': return rate > 25 && rate <= 40
          case '40-60': return rate > 40 && rate <= 60
          case '60+': return rate > 60
          default: return true
        }
      })
    }

    onFilter(filtered)
  }, [searchTerm, jobFilter, statusFilter, ratingFilter, rateFilter, applicants, onFilter])

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
      <div className="flex items-center mb-4">
        <Filter className="h-5 w-5 mr-2 text-gray-500" />
        <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Search */}
        <div className="lg:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search applicants..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Job Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Job Position
          </label>
          <select
            value={jobFilter}
            onChange={(e) => setJobFilter(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Positions</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.job_title}>
                {job.job_title}
              </option>
            ))}
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="interview">Interview</option>
            <option value="hired">Hired</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        {/* Rating Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Rating
          </label>
          <select
            value={ratingFilter}
            onChange={(e) => setRatingFilter(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Ratings</option>
            <option value="5">5 Stars</option>
            <option value="4">4+ Stars</option>
            <option value="3">3+ Stars</option>
            <option value="2">2+ Stars</option>
          </select>
        </div>
      </div>
    </div>
  )
}
