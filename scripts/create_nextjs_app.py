#!/usr/bin/env python3
"""
Create Next.js Application - Build modern web app with applicant management
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
            "components", 
            "styles",
            "public",
            "public/images",
            "public/profiles",
            "utils",
            "types",
            "hooks"
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
                "clsx": "^2.0.0",
                "framer-motion": "^10.16.0"
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
  trailingSlash: true,
  exportPathMap: async function () {
    return {
      '/': { page: '/' },
      '/applicants': { page: '/applicants' },
      '/jobs': { page: '/jobs' },
      '/reports': { page: '/reports' }
    }
  }
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
        
        index_tsx = f"""import { useState, useEffect } from 'react'
import Head from 'next/head'
import { Applicant, Job, Statistics } from '../types'
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
        
        print(f"✅ Created components: Header, StatsBar")
        return [header_path, stats_path]
    
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
        
        # GitHub Actions for deployment
        github_workflow = """name: Deploy to Vercel

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build application
      run: npm run build
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.ORG_ID }}
        vercel-project-id: ${{ secrets.PROJECT_ID }}
        vercel-args: '--prod'
"""
        
        workflow_dir = os.path.join(self.app_dir, ".github/workflows")
        os.makedirs(workflow_dir, exist_ok=True)
        workflow_path = os.path.join(workflow_dir, "deploy.yml")
        with open(workflow_path, 'w') as f:
            f.write(github_workflow)
        
        print(f"✅ Created deployment configs: vercel.json, GitHub Actions")
        return [vercel_path, workflow_path]
    
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
- **Animations**: Framer Motion
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

# Export static files
npm run export

# Deploy to your hosting provider
\`\`\`

## 📁 Project Structure

\`\`\`
nextjs-app/
├── components/          # React components
├── pages/              # Next.js pages
├── styles/             # Global styles
├── types/              # TypeScript types
├── public/             # Static assets
├── utils/              # Utility functions
└── hooks/              # Custom React hooks
\`\`\`

## 🎯 Key Components

- **Header** - Professional branding and navigation
- **StatsBar** - Real-time applicant statistics
- **Filters** - Advanced search and filtering
- **ApplicantGrid** - Card-based applicant display
- **ApplicantCard** - Individual applicant information

## 🔧 Configuration

### Environment Variables

Create a \`.env.local\` file:

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:3000/api
DATABASE_URL=your_database_url
\`\`\`

### Tailwind CSS

Custom colors and animations are configured in \`tailwind.config.js\`.

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

## 📞 Support

For support and questions, please open an issue on GitHub.

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