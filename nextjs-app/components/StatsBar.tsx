import { Users, Clock, CheckCircle, AlertCircle } from 'lucide-react'
import { Statistics } from '../types'

interface StatsBarProps {
  stats: Statistics
}

export default function StatsBar({ stats }: StatsBarProps) {
  const statItems = [
    {
      label: 'Total Applicants',
      value: stats.total_applicants,
      icon: Users,
      color: 'text-blue-600'
    },
    {
      label: 'Pending Review',
      value: stats.status_breakdown.pending,
      icon: Clock,
      color: 'text-yellow-600'
    },
    {
      label: 'Interview',
      value: stats.status_breakdown.interview,
      icon: AlertCircle,
      color: 'text-orange-600'
    },
    {
      label: 'Hired',
      value: stats.status_breakdown.hired,
      icon: CheckCircle,
      color: 'text-green-600'
    }
  ]

  return (
    <div className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {statItems.map((item, index) => (
            <div key={index} className="text-center">
              <div className={`mx-auto h-12 w-12 rounded-full bg-gray-100 flex items-center justify-center ${item.color}`}>
                <item.icon className="h-6 w-6" />
              </div>
              <div className="mt-2">
                <div className="text-2xl font-bold text-gray-900">{item.value}</div>
                <div className="text-sm text-gray-500">{item.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
