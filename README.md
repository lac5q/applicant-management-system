# Recruiting Pipeline - Upwork Applicants Scraper

## 📁 Project Structure

```
Recruiting/
├── applicants/          # Real applicant data files
├── scripts/            # Python scripts and automation tools
├── configuration/      # Project configuration files
├── context/           # Outputs, reports, and temporary files
└── README.md          # This file
```

## 🔧 MCP Configuration

This project uses **Docker MCP** for Playwright browser automation to ensure consistency.

### MCP Server Setup
- **Docker MCP**: `MCP_DOCKER` server configured in `~/.cursor/mcp.json`
- **Removed**: Separate Playwright package to avoid conflicts
- **Approach**: Single, consistent Docker MCP server for all browser automation

### MCP Configuration Location
```
~/.cursor/mcp.json
```

## 🚀 Main Scraper Script

**File**: `scripts/upwork_applicants_scraper_docker_mcp.py`

### Features
- ✅ Uses Docker MCP for Playwright browser automation
- ✅ Scrapes real Upwork applicant profiles (no "John Doe" data)
- ✅ Hardcoded brief URLs for consistency
- ✅ Supports UX Designer and Shopify Developer roles
- ✅ Real-time progress saving
- ✅ Comprehensive error handling

### Hardcoded Brief URLs
- **UX Designer**: `https://www.upwork.com/jobs/~021945256288324407279`
- **Shopify Developer**: `https://www.upwork.com/jobs/~021945253868907578965`

## 📊 Data Organization

### Applicants Folder
Contains real applicant data files:
- `upwork_applicants_ux_designer_*.json` - UX Designer applicants
- `upwork_applicants_shopify_developer_*.json` - Shopify Developer applicants
- `upwork_applicants_evaluation_*.json` - Evaluation results

### Context Folder
- `hiring_pipeline_output/` - Pipeline outputs
- `evaluations/` - Evaluation reports
- `reports/` - Generated reports
- `temp/` - Temporary files

## 🛠️ Usage

### Prerequisites
1. **Docker Desktop** running
2. **Docker MCP Gateway** active
3. **Logged into Upwork** in browser session

### Running the Scraper
```bash
cd scripts
python upwork_applicants_scraper_docker_mcp.py
```

### Expected Output
- Real applicant profiles with actual names, skills, rates, etc.
- Progress saved every 10 applicants
- Final results in `applicants/` folder

## 🔍 Data Fields Collected

Each applicant profile includes:
- **Basic Info**: Name, title, location, hourly rate
- **Skills**: Technical skills and expertise
- **Experience**: Work history and background
- **Performance**: Rating, completion rate, response time
- **Portfolio**: Links and certifications
- **Metadata**: Profile URL, role, scraping timestamp

## 🧹 Cleanup Completed

### Removed Files
- ❌ All "John Doe" dummy data files
- ❌ Empty JSON files with `[]` or `{}` content
- ❌ Old scraper versions with different MCP approaches
- ❌ Separate Playwright package from MCP config

### Kept Files
- ✅ Real applicant data (25+ UX Designer files, 5 Shopify Developer files)
- ✅ Evaluation data with real results
- ✅ Docker MCP scraper script
- ✅ Clean project structure

## 📈 Next Steps

1. **Ensure Docker MCP is running**:
   ```bash
   docker ps | grep mcp
   ```

2. **Start the scraper**:
   ```bash
   cd scripts
   python upwork_applicants_scraper_docker_mcp.py
   ```

3. **Monitor progress** and verify real data collection

## 🔧 Troubleshooting

### Common Issues
- **"John Doe" data**: Ensure Docker MCP server is running
- **No applicants found**: Check Upwork login status
- **Navigation errors**: Verify brief URLs are accessible

### MCP Server Status
```bash
# Check if Docker MCP is running
docker ps | grep mcp

# Check MCP configuration
cat ~/.cursor/mcp.json | grep -A 5 "MCP_DOCKER"
```

---

**Last Updated**: July 19, 2025  
**Version**: 2.0 (Docker MCP Only)  
**Status**: Clean, organized, ready for production use 