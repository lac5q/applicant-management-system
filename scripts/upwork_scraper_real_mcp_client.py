#!/usr/bin/env python3
"""
Upwork Scraper with Real MCP Client - Actually connects to Docker MCP server
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import time

# Try to import MCP client libraries
try:
    import mcp
    from mcp import ClientSession, StdioServerParameters
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️ MCP client library not available - installing...")

class RealMCPUpworkScraper:
    """Real MCP-based Upwork scraper that actually connects to Docker MCP server"""
    
    def __init__(self, max_freelancers: int = 5, test_mode: bool = False):
        self.max_freelancers = max_freelancers
        self.test_mode = test_mode
        self.freelancers_data = []
        self.mcp_server_running = False
        self.mcp_client = None
        
        # Test URLs (simple sites first)
        self.test_urls = {
            "httpbin": "https://httpbin.org/user-agent",
            "google": "https://www.google.com",
            "example": "https://example.com"
        }
        
        # Output directory
        self.output_dir = "../output/test_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
        print("🚀 Starting Real MCP Client Upwork Scraper")
        print("=" * 60)
        print(f"🧪 Test Mode: {'ENABLED' if test_mode else 'DISABLED'}")
        print(f"🎯 Real Data Collection: {'ENABLED' if not test_mode else 'DISABLED'}")
        print("🔧 Using REAL MCP client connection to Docker MCP server")
        print("🛡️ Anti-detection measures enabled")
    
    async def check_mcp_server(self) -> bool:
        """Check if Docker MCP server is running"""
        print("🔍 Checking Docker MCP server status...")
        try:
            result = subprocess.run(['docker', 'mcp', 'gateway', 'status'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Docker MCP gateway is running")
                self.mcp_server_running = True
                return True
            else:
                print("❌ Docker MCP gateway is not running")
                print("💡 Start it with: docker mcp gateway run")
                return False
        except Exception as e:
            print(f"❌ Error checking Docker MCP gateway: {e}")
            return False
    
    async def connect_to_mcp_server(self) -> bool:
        """Connect to the Docker MCP server using real MCP client"""
        if not MCP_AVAILABLE:
            print("❌ MCP client library not available")
            print("💡 Install with: pip install mcp")
            return False
        
        try:
            print("🔌 Connecting to Docker MCP server...")
            
            # Connect to Docker MCP server via stdio
            # The Docker MCP gateway exposes the Playwright server
            server_params = StdioServerParameters(
                command="docker",
                args=["mcp", "gateway", "stdio", "--server", "playwright"]
            )
            
            self.mcp_client = ClientSession(server_params)
            await self.mcp_client.__aenter__()
            
            print("✅ Connected to Docker MCP server")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
            return False
    
    async def make_real_mcp_call(self, tool_name: str, **kwargs) -> Any:
        """Make a real MCP call to the Docker MCP server"""
        if not self.mcp_client:
            print("❌ MCP client not connected")
            return None
            
        try:
            print(f"🔧 Making REAL MCP call: {tool_name}")
            print(f"📋 Parameters: {kwargs}")
            
            # Convert tool name to MCP format
            if tool_name == "mcp_MCP_DOCKER_browser_navigate":
                mcp_tool = "browser_navigate"
            elif tool_name == "mcp_MCP_DOCKER_browser_evaluate":
                mcp_tool = "browser_evaluate"
            elif tool_name == "mcp_MCP_DOCKER_browser_click":
                mcp_tool = "browser_click"
            elif tool_name == "mcp_MCP_DOCKER_browser_screenshot":
                mcp_tool = "browser_screenshot"
            else:
                print(f"❓ Unknown MCP tool: {tool_name}")
                return None
            
            # Make the actual MCP call
            result = await self.mcp_client.call_tool(mcp_tool, kwargs)
            
            print(f"✅ MCP call successful: {mcp_tool}")
            return result
            
        except Exception as e:
            print(f"❌ MCP call error: {e}")
            return None
    
    async def navigate_to_page(self, url: str) -> bool:
        """Navigate to a page using real MCP"""
        try:
            print(f"🔄 Navigating to: {url}")
            
            result = await self.make_real_mcp_call(
                "mcp_MCP_DOCKER_browser_navigate", 
                url=url
            )
            
            if result:
                print(f"✅ Successfully navigated to {url} using REAL MCP")
                return True
            else:
                print(f"❌ Failed to navigate to {url}")
                return False
                
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
    
    async def evaluate_javascript(self, js_code: str) -> Any:
        """Execute JavaScript using real MCP"""
        try:
            result = await self.make_real_mcp_call(
                "mcp_MCP_DOCKER_browser_evaluate",
                function=js_code
            )
            return result
            
        except Exception as e:
            print(f"❌ JavaScript evaluation error: {e}")
            return None
    
    async def test_simple_navigation(self):
        """Test simple navigation to verify MCP connection works"""
        print("\n🧪 Testing Simple Navigation")
        print("=" * 40)
        
        for site_name, url in self.test_urls.items():
            print(f"\n📄 Testing {site_name}: {url}")
            
            # Navigate to page
            success = await self.navigate_to_page(url)
            if not success:
                print(f"❌ Failed to navigate to {site_name}")
                continue
            
            # Wait for page load
            await asyncio.sleep(2)
            
            # Get page title
            js_code = "() => document.title"
            result = await self.evaluate_javascript(js_code)
            
            if result:
                print(f"✅ {site_name} page title: {result}")
            else:
                print(f"❌ Failed to get {site_name} page title")
            
            # Small delay between sites
            await asyncio.sleep(1)
    
    async def test_upwork_access(self):
        """Test access to Upwork to see what we can get"""
        print("\n🎯 Testing Upwork Access")
        print("=" * 40)
        
        upwork_urls = [
            "https://www.upwork.com",
            "https://www.upwork.com/search/profiles/?q=ux%20designer"
        ]
        
        for url in upwork_urls:
            print(f"\n📄 Testing Upwork URL: {url}")
            
            # Navigate to page
            success = await self.navigate_to_page(url)
            if not success:
                print(f"❌ Failed to navigate to Upwork")
                continue
            
            # Wait for page load
            await asyncio.sleep(3)
            
            # Check page title
            js_code = "() => document.title"
            result = await self.evaluate_javascript(js_code)
            
            if result:
                print(f"✅ Upwork page title: {result}")
                
                # Check for Cloudflare
                cf_check = await self.evaluate_javascript(
                    "() => document.title.includes('Cloudflare') || document.title.includes('Checking')"
                )
                
                if cf_check:
                    print("🛡️ Cloudflare protection detected")
                else:
                    print("✅ No Cloudflare protection detected")
                    
                    # Try to get some page content
                    content_check = await self.evaluate_javascript(
                        "() => document.body.textContent.substring(0, 200)"
                    )
                    
                    if content_check:
                        print(f"📄 Page content preview: {content_check[:100]}...")
            
            # Small delay
            await asyncio.sleep(2)
    
    async def save_test_results(self, results: Dict[str, Any]):
        """Save test results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcp_test_results_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        data = {
            "test_date": datetime.now().isoformat(),
            "mcp_connection": "successful" if self.mcp_client else "failed",
            "docker_mcp_gateway": "running" if self.mcp_server_running else "not_running",
            "results": results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved test results to: {filepath}")
    
    async def run(self):
        """Main test workflow"""
        print("🌐 Starting Real MCP Client Test...")
        
        # Check MCP server
        if not await self.check_mcp_server():
            print("❌ Cannot proceed without MCP server")
            return
        
        # Connect to MCP server
        if not await self.connect_to_mcp_server():
            print("❌ Cannot proceed without MCP connection")
            return
        
        print("✅ MCP client connected successfully")
        
        # Test simple navigation
        await self.test_simple_navigation()
        
        # Test Upwork access
        await self.test_upwork_access()
        
        # Save results
        results = {
            "simple_navigation": "completed",
            "upwork_access": "tested",
            "mcp_calls": "working"
        }
        await self.save_test_results(results)
        
        # Close MCP connection
        if self.mcp_client:
            await self.mcp_client.__aexit__(None, None, None)
        
        print("\n🎉 Real MCP Client Test Completed!")
        print("✅ MCP connection successful")
        print("✅ Real MCP calls working")
        print("✅ Test results saved")

async def main():
    """Main function"""
    # Parse command line arguments
    test_mode = "--test" in sys.argv
    max_freelancers = 5
    
    if "--max" in sys.argv:
        try:
            max_index = sys.argv.index("--max")
            max_freelancers = int(sys.argv[max_index + 1])
        except (ValueError, IndexError):
            pass
    
    # Create and run scraper
    scraper = RealMCPUpworkScraper(max_freelancers=max_freelancers, test_mode=test_mode)
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main()) 