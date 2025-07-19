import { Applicant } from '../types'
import ApplicantCard from './ApplicantCard'

interface ApplicantGridProps {
  applicants: Applicant[]
  onStatusUpdate: (id: number, status: string) => void
}

export default function ApplicantGrid({ applicants, onStatusUpdate }: ApplicantGridProps) {
  if (applicants.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 text-lg">No applicants match your filters</div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {applicants.map((applicant) => (
        <ApplicantCard
          key={applicant.id}
          applicant={applicant}
          onStatusUpdate={onStatusUpdate}
        />
      ))}
    </div>
  )
}
