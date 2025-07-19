import React, { useState, useEffect } from 'react'
import Head from 'next/head'

interface Applicant {
  id: string
  name: string
  title: string
  location: string
  hourly_rate: string
  job_success: string
  skills: string[]
  rating: number
  status: string
}

export default function Home() {
  const [applicants, setApplicants] = useState<Applicant[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    total: 0,
    positions: 0,
    averageRating: 0
  })

  useEffect(() => {
    // Load sample data
    const sampleApplicants: Applicant[] = [
      {
        id: '1',
        name: 'Sarah Johnson',
        title: 'Senior UI/UX Designer',
        location: 'San Francisco, CA',
        hourly_rate: '$45/hr',
        job_success: '98%',
        skills: ['Figma', 'Adobe XD', 'Prototyping', 'User Research'],
        rating: 4.8,
        status: 'Active'
      },
      {
        id: '2',
        name: 'Michael Chen',
        title: 'Full Stack Developer',
        location: 'New York, NY',
        hourly_rate: '$55/hr',
        job_success: '95%',
        skills: ['React', 'Node.js', 'TypeScript', 'MongoDB'],
        rating: 4.6,
        status: 'Active'
      },
      {
        id: '3',
        name: 'Emily Rodriguez',
        title: 'Product Manager',
        location: 'Austin, TX',
        hourly_rate: '$65/hr',
        job_success: '99%',
        skills: ['Agile', 'Product Strategy', 'Data Analysis', 'User Stories'],
        rating: 4.9,
        status: 'Active'
      }
    ]

    setApplicants(sampleApplicants)
    setStats({
      total: sampleApplicants.length,
      positions: 3,
      averageRating: 4.7
    })
    setLoading(false)
  }, [])

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
                  Modern hiring platform with intelligent filtering
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

        {/* Stats Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Applicants</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.total}</p>
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
          </div>

          {/* Applicants List */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Recent Applicants</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {applicants.map((applicant) => (
                <div key={applicant.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
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
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">{applicant.hourly_rate}</p>
                        <p className="text-sm text-gray-600">{applicant.job_success} Success</p>
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
                      {applicant.skills.slice(0, 3).map((skill, index) => (
                        <span key={index} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                          {skill}
                        </span>
                      ))}
                      {applicant.skills.length > 3 && (
                        <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                          +{applicant.skills.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  )
} 