#!/usr/bin/env python3
"""
Create Next.js Application - Fixed version with proper directory creation
"""

import os
import json
import shutil
import subprocess
from datetime import datetime
from applicant_database_manager import ApplicantDatabaseManager

class NextJSAppBuilder:
    """Build Next.js application with applicant management system"""
    
    def __init__(self):
        self.db_manager = ApplicantDatabaseManager()
        self.app_dir = "../nextjs-app"
        self.pages_dir = os.path.join(self.app_dir, "pages")
        self.components_dir = os.path.join(self.app_dir, "components")
        self.styles_dir = os.path.join(self.app_dir, "styles")
        self.public_dir = os.path.join(self.app_dir, "public")
        
        print("🚀 Next.js App Builder")
        print("=" * 60)
        print("⚛️  Creating modern React/Next.js application")
        print("🎨 Building with TypeScript and Tailwind CSS")
        print("🚀 Preparing for deployment")
    
    def create_app_structure(self):
        """Create the Next.js application structure"""
        print("\n📁 Creating Next.js app structure...")
        
        # Create main app directory
        os.makedirs(self.app_dir, exist_ok=True)
        
        # Create Next.js directories
        directories = [
            "pages",
            "pages/api",
            "components", 
            "styles",
            "public",
            "public/images",
            "public/profiles",
            "utils",
            "types",
            "hooks",
            ".github/workflows"
        ]
        
        for directory in directories:
            os.makedirs(os.path.join(self.app_dir, directory), exist_ok=True)
            print(f"   📁 Created: {directory}")
        
        print("✅ App structure created")
    
    def create_package_json(self):
        """Create package.json with all dependencies"""
        print("\n📦 Creating package.json...")
        
        package_json = {
            "name": "applicant-management-system",
            "version": "1.0.0",
            "description": "Modern applicant management system built with Next.js",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "export": "next export"
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0",
                "lucide-react": "^0.294.0",
                "clsx": "^2.0.0"
            },
            "devDependencies": {
                "eslint": "^8.0.0",
                "eslint-config-next": "^14.0.0"
            }
        }
        
        package_path = os.path.join(self.app_dir, "package.json")
        with open(package_path, 'w') as f:
            json.dump(package_json, f, indent=2)
        
        print(f"✅ Created package.json: {package_path}")
        return package_path
    
    def create_next_config(self):
        """Create Next.js configuration"""
        print("\n⚙️  Creating Next.js config...")
        
        next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
    unoptimized: true
  },
  trailingSlash: true
}

module.exports = nextConfig
"""
        
        config_path = os.path.join(self.app_dir, "next.config.js")
        with open(config_path, 'w') as f:
            f.write(next_config)
        
        print(f"✅ Created next.config.js: {config_path}")
        return config_path
    
    def create_tailwind_config(self):
        """Create Tailwind CSS configuration"""
        print("\n🎨 Creating Tailwind config...")
        
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
"""
        
        config_path = os.path.join(self.app_dir, "tailwind.config.js")
        with open(config_path, 'w') as f:
            f.write(tailwind_config)
        
        print(f"✅ Created tailwind.config.js: {config_path}")
        return config_path
    
    def create_postcss_config(self):
        """Create PostCSS configuration"""
        print("\n🔧 Creating PostCSS config...")
        
        postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        
        config_path = os.path.join(self.app_dir, "postcss.config.js")
        with open(config_path, 'w') as f:
            f.write(postcss_config)
        
        print(f"✅ Created postcss.config.js: {config_path}")
        return config_path
    
    def create_tsconfig(self):
        """Create TypeScript configuration"""
        print("\n📝 Creating TypeScript config...")
        
        tsconfig = """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""
        
        config_path = os.path.join(self.app_dir, "tsconfig.json")
        with open(config_path, 'w') as f:
            f.write(tsconfig)
        
        print(f"✅ Created tsconfig.json: {config_path}")
        return config_path
    
    def create_global_styles(self):
        """Create global CSS styles"""
        print("\n🎨 Creating global styles...")
        
        global_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    font-family: 'Inter', system-ui, sans-serif;
  }
  
  body {
    @apply bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200;
  }
  
  .btn-secondary {
    @apply bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg transition-colors duration-200;
  }
  
  .card {
    @apply bg-white rounded-xl shadow-lg border border-gray-200 p-6;
  }
  
  .input-field {
    @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  }
}

@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-primary-600 to-indigo-600 bg-clip-text text-transparent;
  }
}
"""
        
        styles_path = os.path.join(self.app_dir, "styles/globals.css")
        with open(styles_path, 'w') as f:
            f.write(global_css)
        
        print(f"✅ Created global styles: {styles_path}")
        return styles_path
    
    def create_app_component(self):
        """Create the main App component"""
        print("\n🏠 Creating App component...")
        
        app_tsx = """import type { AppProps } from 'next/app'
import '../styles/globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function App({ Component, pageProps }: AppProps) {
  return (
    <main className={inter.className}>
      <Component {...pageProps} />
    </main>
  )
}
"""
        
        app_path = os.path.join(self.app_dir, "pages/_app.tsx")
        with open(app_path, 'w') as f:
            f.write(app_tsx)
        
        print(f"✅ Created App component: {app_path}")
        return app_path
    
    def create_document_component(self):
        """Create the Document component"""
        print("\n📄 Creating Document component...")
        
        document_tsx = """import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
"""
        
        document_path = os.path.join(self.app_dir, "pages/_document.tsx")
        with open(document_path, 'w') as f:
            f.write(document_tsx)
        
        print(f"✅ Created Document component: {document_path}")
        return document_path
    
    def create_types(self):
        """Create TypeScript type definitions"""
        print("\n📝 Creating TypeScript types...")
        
        types_ts = """export interface Applicant {
  id: number;
  name: string;
  title: string;
  location: string;
  hourly_rate: string;
  job_success: string;
  total_earned: string;
  hours_worked: string;
  rating: number;
  overview: string;
  skills: string[];
  job_title: string;
  status: 'pending' | 'interview' | 'hired' | 'rejected';
  proposal_text?: string;
  portfolio_link?: string;
  profile_image?: string;
  created_at: string;
}

export interface Job {
  id: number;
  job_title: string;
  description: string;
  requirements: string[];
  applicant_count: number;
  created_at: string;
}

export interface Statistics {
  total_applicants: number;
  status_breakdown: {
    pending: number;
    interview: number;
    hired: number;
    rejected: number;
  };
  jobs_breakdown: Record<string, number>;
  average_rating: number;
  total_earned: string;
}
"""
        
        types_path = os.path.join(self.app_dir, "types/index.ts")
        with open(types_path, 'w') as f:
            f.write(types_ts)
        
        print(f"✅ Created TypeScript types: {types_path}")
        return types_path
    
    def create_api_routes(self):
        """Create API routes for data access"""
        print("\n🔌 Creating API routes...")
        
        # API route for applicants
        applicants_api = """import type { NextApiRequest, NextApiResponse } from 'next'
import { Applicant } from '../../types'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Applicant[] | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    // In a real app, this would connect to your database
    // For now, we'll return mock data
    const applicants: Applicant[] = [
      {
        id: 1,
        name: "John Smith",
        title: "Senior Shopify Developer",
        location: "New York, NY",
        hourly_rate: "$45/hr",
        job_success: "98%",
        total_earned: "$12,450",
        hours_worked: "276",
        rating: 5,
        overview: "Experienced Shopify developer with 5+ years building custom e-commerce solutions.",
        skills: ["Shopify", "Liquid", "JavaScript", "React"],
        job_title: "Shopify Developer",
        status: "pending",
        created_at: "2025-01-19T10:00:00Z"
      }
    ]
    
    res.status(200).json(applicants)
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch applicants' })
  }
}
"""
        
        api_path = os.path.join(self.app_dir, "pages/api/applicants.ts")
        with open(api_path, 'w') as f:
            f.write(applicants_api)
        
        print(f"✅ Created API route: {api_path}")
        return api_path
    
    def create_main_page(self):
        """Create the main index page"""
        print("\n🏠 Creating main page...")
        
        # Get data from database
        applicants = self.db_manager.get_all_applicants()
        jobs = self.db_manager.get_jobs()
        stats = self.db_manager.get_statistics()
        
        index_tsx = f"""import {{ useState, useEffect }} from 'react'
import Head from 'next/head'
import {{ Applicant, Job, Statistics }} from '../types'
import Header from '../components/Header'
import StatsBar from '../components/StatsBar'
import Filters from '../components/Filters'
import ApplicantGrid from '../components/ApplicantGrid'

export default function Home() {{
  const [applicants, setApplicants] = useState<Applicant[]>([])
  const [jobs, setJobs] = useState<Job[]>([])
  const [stats, setStats] = useState<Statistics | null>(null)
  const [filteredApplicants, setFilteredApplicants] = useState<Applicant[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {{
    // Load data from database
    const loadData = async () => {{
      try {{
        // In production, this would be an API call
        const applicantsData = {json.dumps(applicants, ensure_ascii=False)}
        const jobsData = {json.dumps(jobs, ensure_ascii=False)}
        const statsData = {json.dumps(stats, ensure_ascii=False)}
        
        setApplicants(applicantsData)
        setJobs(jobsData)
        setStats(statsData)
        setFilteredApplicants(applicantsData)
        setLoading(false)
      }} catch (error) {{
        console.error('Failed to load data:', error)
        setLoading(false)
      }}
    }}
    
    loadData()
  }}, [])

  const handleFilter = (filtered: Applicant[]) => {{
    setFilteredApplicants(filtered)
  }}

  const handleStatusUpdate = (applicantId: number, status: string) => {{
    setApplicants(prev => 
      prev.map(applicant => 
        applicant.id === applicantId 
          ? {{ ...applicant, status: status as any }}
          : applicant
      )
    )
  }}

  if (loading) {{
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }}

  return (
    <>
      <Head>
        <title>Applicant Management System</title>
        <meta name="description" content="Modern applicant management system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Header />
        
        {{stats && <StatsBar stats={{stats}} />}}
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Filters 
            applicants={{applicants}}
            jobs={{jobs}}
            onFilter={{handleFilter}}
          />
          
          <ApplicantGrid 
            applicants={{filteredApplicants}}
            onStatusUpdate={{handleStatusUpdate}}
          />
        </div>
      </div>
    </>
  )
}}
"""
        
        index_path = os.path.join(self.app_dir, "pages/index.tsx")
        with open(index_path, 'w') as f:
            f.write(index_tsx)
        
        print(f"✅ Created main page: {index_path}")
        return index_path
    
    def create_components(self):
        """Create React components"""
        print("\n🧩 Creating React components...")
        
        # Header component
        header_tsx = """import { Users, Calendar, Clock } from 'lucide-react'

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
"""
        
        header_path = os.path.join(self.app_dir, "components/Header.tsx")
        with open(header_path, 'w') as f:
            f.write(header_tsx)
        
        # StatsBar component
        stats_tsx = """import { Users, Clock, CheckCircle, AlertCircle } from 'lucide-react'
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
"""
        
        stats_path = os.path.join(self.app_dir, "components/StatsBar.tsx")
        with open(stats_path, 'w') as f:
            f.write(stats_tsx)
        
        # Filters component
        filters_tsx = """import { useState, useEffect } from 'react'
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
"""
        
        filters_path = os.path.join(self.app_dir, "components/Filters.tsx")
        with open(filters_path, 'w') as f:
            f.write(filters_tsx)
        
        # ApplicantGrid component
        grid_tsx = """import { Applicant } from '../types'
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
"""
        
        grid_path = os.path.join(self.app_dir, "components/ApplicantGrid.tsx")
        with open(grid_path, 'w') as f:
            f.write(grid_tsx)
        
        # ApplicantCard component
        card_tsx = """import { Star, MapPin, DollarSign, Clock, CheckCircle, XCircle, Calendar } from 'lucide-react'
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
"""
        
        card_path = os.path.join(self.app_dir, "components/ApplicantCard.tsx")
        with open(card_path, 'w') as f:
            f.write(card_tsx)
        
        print(f"✅ Created components: Header, StatsBar, Filters, ApplicantGrid, ApplicantCard")
        return [header_path, stats_path, filters_path, grid_path, card_path]
    
    def create_deployment_config(self):
        """Create deployment configuration files"""
        print("\n🚀 Creating deployment config...")
        
        # Vercel configuration
        vercel_json = """{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ]
}
"""
        
        vercel_path = os.path.join(self.app_dir, "vercel.json")
        with open(vercel_path, 'w') as f:
            f.write(vercel_json)
        
        print(f"✅ Created deployment config: vercel.json")
        return vercel_path
    
    def create_readme(self):
        """Create comprehensive README"""
        print("\n📖 Creating README...")
        
        readme_md = f"""# Applicant Management System

A modern, scalable applicant management system built with **Next.js**, **TypeScript**, and **Tailwind CSS**.

## 🚀 Features

- **⚛️ Modern React/Next.js** - Built with the latest web technologies
- **🎨 Beautiful UI** - Professional design with Tailwind CSS
- **📱 Responsive** - Works perfectly on all devices
- **🔍 Advanced Filtering** - Filter by job, status, rating, and more
- **📊 Real-time Stats** - Live dashboard with applicant metrics
- **🔗 Portfolio Access** - Direct links to candidate work
- **⚡ Fast Performance** - Optimized for speed and SEO

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel

## 📦 Installation

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
\`\`\`

## 🌐 Development

\`\`\`bash
# Start development server
npm run dev

# Open http://localhost:3000
\`\`\`

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect to Vercel**:
   \`\`\`bash
   npx vercel
   \`\`\`

2. **Deploy automatically**:
   - Push to main branch
   - Vercel will auto-deploy

### Manual Deployment

\`\`\`bash
# Build the application
npm run build

# Start production server
npm start
\`\`\`

## 📁 Project Structure

\`\`\`
nextjs-app/
├── components/          # React components
├── pages/              # Next.js pages
├── styles/             # Global styles
├── types/              # TypeScript types
├── public/             # Static assets
└── utils/              # Utility functions
\`\`\`

## 🎯 Key Components

- **Header** - Professional branding and navigation
- **StatsBar** - Real-time applicant statistics
- **Filters** - Advanced search and filtering
- **ApplicantGrid** - Card-based applicant display
- **ApplicantCard** - Individual applicant information

## 📊 Data Structure

The application uses a SQLite database with the following structure:

- **Applicants** - Candidate information and ratings
- **Jobs** - Available positions and requirements
- **Skills** - Applicant skill sets
- **Statistics** - Real-time metrics and analytics

## 🎨 Customization

### Styling

Modify \`styles/globals.css\` for custom styles:

\`\`\`css
@layer components {{
  .custom-button {{
    @apply bg-primary-600 hover:bg-primary-700;
  }}
}}
\`\`\`

### Components

All components are in the \`components/\` directory and can be easily customized.

## 📈 Performance

- **⚡ Fast Loading** - Optimized bundle size
- **🎯 SEO Ready** - Meta tags and structured data
- **📱 Mobile First** - Responsive design
- **🔍 Search Friendly** - Clean URLs and navigation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using Next.js and TypeScript**

Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
"""
        
        readme_path = os.path.join(self.app_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_md)
        
        print(f"✅ Created README: {readme_path}")
        return readme_path
    
    def install_dependencies(self):
        """Install npm dependencies"""
        print("\n📦 Installing dependencies...")
        
        try:
            # Change to app directory
            os.chdir(self.app_dir)
            
            # Install dependencies
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully")
            else:
                print(f"⚠️  Installation completed with warnings: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("💡 You can manually run 'npm install' in the app directory")
    
    def run(self):
        """Main build workflow"""
        print("🚀 Starting Next.js app build...")
        
        # Create app structure
        self.create_app_structure()
        
        # Create configuration files
        self.create_package_json()
        self.create_next_config()
        self.create_tailwind_config()
        self.create_postcss_config()
        self.create_tsconfig()
        
        # Create styles
        self.create_global_styles()
        
        # Create app components
        self.create_app_component()
        self.create_document_component()
        
        # Create types and API
        self.create_types()
        self.create_api_routes()
        
        # Create main page and components
        self.create_main_page()
        self.create_components()
        
        # Create deployment config
        self.create_deployment_config()
        
        # Create documentation
        self.create_readme()
        
        # Install dependencies
        self.install_dependencies()
        
        # Final summary
        stats = self.db_manager.get_statistics()
        
        print(f"\n🎉 Next.js App Complete!")
        print(f"📁 App Directory: {self.app_dir}")
        print(f"📊 Total Applicants: {stats['total_applicants']}")
        print(f"💼 Job Positions: {len(stats['jobs_breakdown'])}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. cd {self.app_dir}")
        print(f"   2. npm run dev")
        print(f"   3. Open http://localhost:3000")
        print(f"   4. Deploy to Vercel: npx vercel")

def main():
    """Main function"""
    builder = NextJSAppBuilder()
    builder.run()

if __name__ == "__main__":
    main() 