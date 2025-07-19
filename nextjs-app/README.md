# Applicant Management System

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
@layer components {
  .custom-button {
    @apply bg-primary-600 hover:bg-primary-700;
  }
}
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

Generated on July 19, 2025 at 02:28 AM
