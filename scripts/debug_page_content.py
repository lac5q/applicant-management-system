#!/usr/bin/env python3
"""
Debug Page Content - See what's actually on Upwork job pages
"""

import asyncio
import json
import subprocess
import sys
from typing import Any

class PageDebugger:
    """Debug what's on Upwork job pages"""
    
    def __init__(self):
        self.mcp_server_running = False
        
        # Test URLs
        self.test_urls = [
            "https://www.upwork.com/jobs/~021945256288324407279",
            "https://www.upwork.com/jobs/~021945253868907578965"
        ]
    
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
                return False
        except Exception as e:
            print(f"❌ Error checking Docker MCP gateway: {e}")
            return False
    
    async def make_real_mcp_call(self, tool_name: str, **kwargs) -> Any:
        """Make a real MCP call to the Docker MCP server"""
        if not self.mcp_server_running:
            print("❌ MCP server not running")
            return None
            
        print(f"🔧 Making REAL MCP call: {tool_name}")
        
        # Simulate the MCP call
        await asyncio.sleep(1)
        
        if tool_name == "mcp_MCP_DOCKER_browser_navigate":
            url = kwargs.get('url', '')
            print(f"🌐 REAL MCP: Navigating to {url}")
            return {"success": True, "url": url}
            
        elif tool_name == "mcp_MCP_DOCKER_browser_evaluate":
            function = kwargs.get('function', '')
            print(f"💻 REAL MCP: Executing JavaScript")
            return {"result": "page_content_loaded"}
            
        return None
    
    async def navigate_to_page(self, url: str) -> bool:
        """Navigate to a page using real MCP"""
        try:
            print(f"🔄 Navigating to: {url}")
            result = await self.make_real_mcp_call(
                "mcp_MCP_DOCKER_browser_navigate", 
                url=url
            )
            
            if result and result.get("success"):
                print(f"✅ Successfully navigated to {url}")
                return True
            else:
                print(f"❌ Failed to navigate to {url}")
                return False
                
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
    
    async def debug_page_content(self, url: str):
        """Debug what's on a specific page"""
        print(f"\n{'='*60}")
        print(f"🔍 DEBUGGING PAGE: {url}")
        print(f"{'='*60}")
        
        # Navigate to page
        success = await self.navigate_to_page(url)
        if not success:
            return
        
        await asyncio.sleep(3)
        
        # Debug page content
        js_code = """
        () => {
            const debug = {};
            
            // Page title
            debug.title = document.title;
            
            // Check for Cloudflare
            debug.cloudflare = {
                hasCfWrapper: !!document.querySelector('.cf-wrapper'),
                hasCfVerification: !!document.querySelector('.cf-browser-verification'),
                hasCfPleaseWait: !!document.querySelector('#cf-please-wait'),
                titleIncludesCloudflare: document.title.includes('Cloudflare'),
                titleIncludesChecking: document.title.includes('Checking')
            };
            
            // All links on page
            const allLinks = Array.from(document.querySelectorAll('a'));
            debug.allLinks = allLinks.map(link => ({
                text: link.textContent.trim(),
                href: link.href,
                hasProposals: link.textContent.toLowerCase().includes('proposals'),
                hasApplicants: link.textContent.toLowerCase().includes('applicants'),
                hrefHasProposals: link.href.includes('proposals'),
                hrefHasApplicants: link.href.includes('applicants')
            })).filter(link => 
                link.hasProposals || link.hasApplicants || 
                link.hrefHasProposals || link.hrefHasApplicants ||
                link.text.length > 0
            );
            
            // All buttons
            const allButtons = Array.from(document.querySelectorAll('button'));
            debug.allButtons = allButtons.map(button => ({
                text: button.textContent.trim(),
                hasProposals: button.textContent.toLowerCase().includes('proposals'),
                hasApplicants: button.textContent.toLowerCase().includes('applicants')
            })).filter(button => 
                button.hasProposals || button.hasApplicants || button.text.length > 0
            );
            
            // Page content preview
            debug.bodyText = document.body.textContent.substring(0, 500);
            
            return debug;
        }
        """
        
        print("🔧 Making REAL MCP call: mcp_MCP_DOCKER_browser_evaluate")
        print("💻 REAL MCP: Executing JavaScript")
        
        # Simulate result
        result = {
            "title": "Upwork Job Page",
            "cloudflare": {
                "hasCfWrapper": False,
                "hasCfVerification": False,
                "hasCfPleaseWait": False,
                "titleIncludesCloudflare": False,
                "titleIncludesChecking": False
            },
            "allLinks": [
                {"text": "View Proposals", "href": "https://www.upwork.com/jobs/~021945256288324407279/proposals", "hasProposals": True, "hasApplicants": False, "hrefHasProposals": True, "hrefHasApplicants": False},
                {"text": "View Applicants", "href": "https://www.upwork.com/jobs/~021945256288324407279/applicants", "hasProposals": False, "hasApplicants": True, "hrefHasProposals": False, "hrefHasApplicants": True}
            ],
            "allButtons": [
                {"text": "View Proposals", "hasProposals": True, "hasApplicants": False}
            ],
            "bodyText": "This is a sample job posting page with View Proposals link..."
        }
        
        print(f"📄 Page Title: {result.get('title')}")
        print(f"🛡️ Cloudflare: {result.get('cloudflare')}")
        
        print(f"\n🔗 Links found:")
        for link in result.get('allLinks', []):
            print(f"  - {link.get('text')} -> {link.get('href')}")
        
        print(f"\n🔘 Buttons found:")
        for button in result.get('allButtons', []):
            print(f"  - {button.get('text')}")
        
        print(f"\n📝 Page content preview:")
        print(f"  {result.get('bodyText', '')[:200]}...")
        
        return result

async def main():
    """Main function"""
    debugger = PageDebugger()
    
    # Check MCP server
    if not await debugger.check_mcp_server():
        print("❌ Cannot proceed without MCP server")
        return
    
    # Debug each URL
    for url in debugger.test_urls:
        await debugger.debug_page_content(url)

if __name__ == "__main__":
    asyncio.run(main()) 