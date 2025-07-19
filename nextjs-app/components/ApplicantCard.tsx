import { Star, MapPin, DollarSign, Clock, CheckCircle, XCircle, Calendar } from 'lucide-react'
import { Applicant } from '../types'

interface ApplicantCardProps {
  applicant: Applicant
  onStatusUpdate: (id: number, status: string) => void
}

export default function ApplicantCard({ applicant, onStatusUpdate }: ApplicantCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'interview': return 'bg-blue-100 text-blue-800'
      case 'hired': return 'bg-green-100 text-green-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-lg mr-3">
            {applicant.name.charAt(0)}
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{applicant.name}</h3>
            <p className="text-sm text-gray-600">{applicant.title}</p>
            <div className="flex items-center text-xs text-gray-500 mt-1">
              <MapPin className="h-3 w-3 mr-1" />
              {applicant.location}
            </div>
          </div>
        </div>
        <div className="flex items-center">
          <Star className="h-4 w-4 text-yellow-400 mr-1" />
          <span className="text-sm font-medium">{applicant.rating}/5</span>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="text-center p-2 bg-gray-50 rounded">
          <div className="text-xs text-gray-500">Rate</div>
          <div className="font-semibold text-sm">{applicant.hourly_rate}</div>
        </div>
        <div className="text-center p-2 bg-gray-50 rounded">
          <div className="text-xs text-gray-500">Success</div>
          <div className="font-semibold text-sm">{applicant.job_success}</div>
        </div>
        <div className="text-center p-2 bg-gray-50 rounded">
          <div className="text-xs text-gray-500">Earned</div>
          <div className="font-semibold text-sm">{applicant.total_earned}</div>
        </div>
        <div className="text-center p-2 bg-gray-50 rounded">
          <div className="text-xs text-gray-500">Hours</div>
          <div className="font-semibold text-sm">{applicant.hours_worked}</div>
        </div>
      </div>

      {/* Skills */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-1">
          {applicant.skills.slice(0, 3).map((skill, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-primary-100 text-primary-800 text-xs rounded-full"
            >
              {skill}
            </span>
          ))}
          {applicant.skills.length > 3 && (
            <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
              +{applicant.skills.length - 3} more
            </span>
          )}
        </div>
      </div>

      {/* Overview */}
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">
        {applicant.overview}
      </p>

      {/* Actions */}
      <div className="flex gap-2 mb-3">
        <button
          onClick={() => onStatusUpdate(applicant.id, 'interview')}
          className="flex-1 flex items-center justify-center px-3 py-2 bg-blue-100 text-blue-700 text-sm rounded hover:bg-blue-200 transition-colors"
        >
          <Calendar className="h-3 w-3 mr-1" />
          Interview
        </button>
        <button
          onClick={() => onStatusUpdate(applicant.id, 'hired')}
          className="flex-1 flex items-center justify-center px-3 py-2 bg-green-100 text-green-700 text-sm rounded hover:bg-green-200 transition-colors"
        >
          <CheckCircle className="h-3 w-3 mr-1" />
          Hire
        </button>
        <button
          onClick={() => onStatusUpdate(applicant.id, 'rejected')}
          className="flex-1 flex items-center justify-center px-3 py-2 bg-red-100 text-red-700 text-sm rounded hover:bg-red-200 transition-colors"
        >
          <XCircle className="h-3 w-3 mr-1" />
          Reject
        </button>
      </div>

      {/* Status Badge */}
      <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(applicant.status)}`}>
        {applicant.status.toUpperCase()}
      </div>
    </div>
  )
}
