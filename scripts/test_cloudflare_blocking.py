#!/usr/bin/env python3
"""
Test Cloudflare Blocking - Check if Cloudflare is blocking Playwright
"""

import asyncio
import subprocess
import sys
from typing import Any

async def test_cloudflare_blocking():
    """Test if Cloudflare is blocking Playwright browser"""
    print("🛡️ Testing Cloudflare Blocking")
    print("=" * 50)
    
    # Check if Docker MCP gateway is running
    print("🔍 Checking Docker MCP gateway status...")
    try:
        result = subprocess.run(['docker', 'mcp', 'gateway', 'status'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker MCP gateway is running")
        else:
            print("❌ Docker MCP gateway is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Docker MCP gateway: {e}")
        return False
    
    print("\n🛡️ Cloudflare Blocking Analysis:")
    print("Cloudflare commonly blocks:")
    print("1. Automated browsers (Playwright, Puppeteer)")
    print("2. Headless browsers")
    print("3. Bots and scrapers")
    print("4. Non-human browser signatures")
    
    print("\n🔍 Signs of Cloudflare blocking:")
    print("✅ 'Checking your browser' page")
    print("✅ 'Please wait while we verify'")
    print("✅ CAPTCHA challenges")
    print("✅ Blocked access to content")
    print("✅ Different page content for bots")
    
    print("\n💡 Solutions for Cloudflare blocking:")
    print("1. Use stealth mode in Playwright")
    print("2. Add realistic browser headers")
    print("3. Use undetected-chromedriver")
    print("4. Add delays and human-like behavior")
    print("5. Use residential proxies")
    print("6. Solve CAPTCHAs manually")
    
    print("\n🎯 Current Issue:")
    print("❌ Script is simulating MCP calls (not making real ones)")
    print("❌ Even if we made real calls, Cloudflare might block Playwright")
    print("❌ Need to implement anti-detection measures")
    
    print("\n🔧 To test if Cloudflare is blocking:")
    print("1. Make real MCP calls to navigate to Upwork")
    print("2. Check if we get 'Checking your browser' page")
    print("3. See if we can bypass Cloudflare protection")
    print("4. Verify we can access the actual job content")
    
    return True

async def test_simple_navigation():
    """Test simple navigation to see if Cloudflare blocks us"""
    print("\n🧪 Testing Simple Navigation")
    print("=" * 30)
    
    print("🔧 To make this test work, we need:")
    print("1. Real MCP client connection")
    print("2. Playwright browser with stealth mode")
    print("3. Anti-detection measures")
    
    print("\n📋 Test URLs to try:")
    print("- https://www.upwork.com (main site)")
    print("- https://www.google.com (control test)")
    print("- https://httpbin.org/user-agent (check browser signature)")
    
    print("\n💡 Expected results:")
    print("✅ Google.com: Should work (no Cloudflare)")
    print("❌ Upwork.com: Might be blocked by Cloudflare")
    print("✅ httpbin.org: Should show our browser signature")
    
    return True

async def main():
    """Main function"""
    print("🛡️ Cloudflare Blocking Test")
    print("=" * 50)
    
    success = await test_cloudflare_blocking()
    if success:
        await test_simple_navigation()
        print("\n🎯 Next Steps:")
        print("1. Implement real MCP client")
        print("2. Add Playwright stealth mode")
        print("3. Test with different sites")
        print("4. Handle Cloudflare challenges")
    else:
        print("\n❌ Need to fix Docker MCP gateway first")

if __name__ == "__main__":
    asyncio.run(main()) 