import { Users, Calendar, Clock } from 'lucide-react'

export default function Header() {
  const now = new Date()
  
  return (
    <header className="bg-gradient-to-r from-primary-600 to-indigo-700 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <Users className="h-12 w-12 mr-4" />
            <h1 className="text-4xl font-bold">Applicant Management System</h1>
          </div>
          <p className="text-xl opacity-90 mb-6">
            Modern hiring platform with intelligent filtering and portfolio access
          </p>
          <div className="flex justify-center space-x-8 text-sm opacity-75">
            <div className="flex items-center">
              <Calendar className="h-4 w-4 mr-2" />
              {now.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
            </div>
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              {now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
