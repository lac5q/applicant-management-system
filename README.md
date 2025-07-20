# Applicant Management System

**Created:** July 19, 2025  
**Updated:** July 19, 2025  
**Version:** 1.0.0

A modern, full-stack applicant management system built with Next.js frontend and Python backend, featuring intelligent filtering, data processing, and portfolio access.

## 🚀 Live Demo

**GitHub Pages:** [https://lac5q.github.io/applicant-management-system](https://lac5q.github.io/applicant-management-system)

## ✨ Features

### 🎯 Core Functionality
- **Applicant Tracking**: Comprehensive database for managing job applicants
- **Intelligent Filtering**: Advanced search and filter capabilities
- **Portfolio Access**: Direct access to applicant portfolios and work samples
- **Rating System**: Multi-criteria evaluation and scoring
- **Data Processing**: Automated processing of applicant data from multiple sources

### 🛠️ Technical Stack
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: Python with FastAPI and SQLite database
- **Data Processing**: Pandas, NumPy, and custom processing scripts
- **Web Scraping**: MCP (Model Context Protocol) integration with Playwright
- **Deployment**: GitHub Pages with GitHub Actions CI/CD

### 📊 Data Management
- **Database**: SQLite with structured tables for jobs, applicants, skills, and ratings
- **Import/Export**: JSON, CSV, and HTML report generation
- **Image Processing**: OCR capabilities for processing screenshots
- **Real-time Updates**: Live data processing and updates

## 🏗️ Project Structure

```
Recruiting/
├── .github/workflows/     # GitHub Actions for deployment
├── nextjs-app/           # Next.js frontend application
├── scripts/              # Python processing scripts
├── configuration/        # Configuration files
├── output/              # Generated outputs and reports
├── site/                # Static site files
└── types/               # TypeScript type definitions
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lac5q/applicant-management-system.git
   cd applicant-management-system
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r configuration/requirements.txt
   pip install -r scripts/requirements_candidate_processing.txt
   ```

3. **Set up Next.js application**
   ```bash
   cd nextjs-app
   npm install
   ```

4. **Start the development server**
   ```bash
   # From the root directory
   ./startup.sh
   
   # Or manually
   cd nextjs-app
   npm run dev
   ```

5. **Access the application**
   - **Local Development**: http://localhost:3000
   - **Production**: https://lac5q.github.io/applicant-management-system

## 📋 Usage

### Processing Applicants
```bash
# Process existing candidate data
python3 scripts/process_existing_candidates.py

# Generate reports
python3 scripts/build_site_structure.py
```

### Database Management
```bash
# Initialize database
python3 -c "from scripts.applicant_database_manager import ApplicantDatabaseManager; db = ApplicantDatabaseManager()"
```

### MCP Integration
```bash
# Test MCP connection
python3 scripts/test_mcp_connection.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
# Database
DATABASE_URL=sqlite:///output/applicants/applicants.db

# API Keys (if needed)
OPENAI_API_KEY=your_openai_key_here
```

### MCP Setup
The project includes MCP (Model Context Protocol) integration for web scraping:
- Docker MCP Gateway for Playwright automation
- 24 available Playwright tools
- Automated browser control and data extraction

## 📊 Data Processing Pipeline

1. **Data Collection**: Web scraping and manual input
2. **Processing**: Automated data cleaning and validation
3. **Analysis**: Rating and scoring algorithms
4. **Export**: Multiple format support (JSON, HTML, CSV)
5. **Visualization**: Charts and reports generation

## 🎨 UI Components

- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Modern Interface**: Clean, professional design
- **Interactive Elements**: Hover effects and smooth transitions
- **Data Visualization**: Charts and statistics display
- **Filtering System**: Advanced search and filter capabilities

## 🚀 Deployment

### GitHub Pages (Automatic)
The application is automatically deployed to GitHub Pages via GitHub Actions:
- **Trigger**: Push to master branch
- **Build**: Next.js static export
- **Deploy**: GitHub Pages hosting

### Manual Deployment
```bash
# Build for production
cd nextjs-app
npm run build

# Export static files
npm run export
```

## 📈 Performance

- **Build Time**: ~30 seconds
- **Bundle Size**: Optimized with Next.js
- **Loading Speed**: Fast static generation
- **SEO**: Optimized meta tags and structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/lac5q/applicant-management-system/issues)
- **Documentation**: Check the `docs/` folder for detailed guides
- **Email**: Contact through GitHub profile

## 🔄 Changelog

### Version 1.0.0 (July 19, 2025)
- ✅ Initial release
- ✅ Next.js frontend with TypeScript
- ✅ Python backend with data processing
- ✅ MCP integration for web scraping
- ✅ GitHub Pages deployment
- ✅ Comprehensive documentation

---

**Built with ❤️ using Next.js, Python, and modern web technologies** 