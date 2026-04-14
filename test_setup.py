#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Test Script
Tests if all dependencies are installed and configured correctly
Run this BEFORE starting the bot to catch issues early
"""
import sys
import os

print("=" * 60)
print("Tempo Contract Analyzer - Setup Test")
print("=" * 60)
print()

# Test 1: Python Version
print("[*] Testing Python version...")
if sys.version_info < (3, 9):
    print(f"  [!] Python {sys.version_info.major}.{sys.version_info.minor} detected")
    print(f"  [WARNING] Python 3.9+ is recommended")
else:
    print(f"  [OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

print()

# Test 2: Required Packages
print("[*] Testing required packages...")
required_packages = [
    'discord',
    'web3',
    'aiohttp',
    'dotenv',
    'requests',
    'eth_abi',
    'eth_utils'
]

missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  [OK] {package}")
    except ImportError:
        print(f"  [MISSING] {package}")
        missing.append(package)

if missing:
    print()
    print("[WARNING] Missing packages detected!")
    print("          Run: pip install -r requirements.txt")
    print()

print()

# Test 3: .env File
print("[*] Testing .env configuration...")
from pathlib import Path

env_file = Path('.env')
if not env_file.exists():
    print("  [!] .env file not found!")
    print("      Run: cp .env.example .env")
else:
    print("  [OK] .env file exists")
    
    # Load and check
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv('DISCORD_TOKEN')
        rpc_url = os.getenv('TEMPO_RPC_URL')
        
        if not token or token == 'your_bot_token_here':
            print("  [WARNING] DISCORD_TOKEN not set or using default value")
            print("            Edit .env and add your bot token from Discord Developer Portal")
            print("            Get it from: https://discord.com/developers/applications/.../bot")
        else:
            print(f"  [OK] DISCORD_TOKEN is set ({len(token)} characters)")
        
        if rpc_url:
            print(f"  [OK] TEMPO_RPC_URL: {rpc_url}")
        else:
            print("  [WARNING] TEMPO_RPC_URL not set")
    except Exception as e:
        print(f"  [ERROR] Failed to load .env: {e}")

print()

# Test 4: File Structure
print("[*] Testing file structure...")
required_files = [
    'bot.py',
    'config.py',
    'requirements.txt',
    'cogs/contract_analysis.py',
    'analyzers/contract_fetcher.py',
    'analyzers/static_analyzer.py',
    'analyzers/onchain_checker.py',
    'analyzers/risk_engine.py'
]

for file in required_files:
    if Path(file).exists():
        print(f"  [OK] {file}")
    else:
        print(f"  [MISSING] {file}")

print()

# Test 5: Network Test (optional)
print("[*] Testing network connectivity (optional)...")
try:
    import aiohttp
    import asyncio
    
    async def test_rpc():
        rpc_url = os.getenv('TEMPO_RPC_URL', 'https://rpc.tempo.xyz')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    rpc_url,
                    json={"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 1},
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        chain_id = int(data['result'], 16)
                        print(f"  [OK] Tempo RPC connected (Chain ID: {chain_id})")
                        return True
        except Exception as e:
            print(f"  [INFO] Tempo RPC connection test failed: {str(e)[:50]}...")
            print(f"         This might be normal if RPC requires authentication")
            return False
    
    asyncio.run(test_rpc())
except Exception as e:
    print(f"  [INFO] Network test skipped: {e}")

print()
print("=" * 60)

# Summary
if missing:
    print("[INCOMPLETE] Setup incomplete - missing packages")
    print("             Run: pip install -r requirements.txt")
elif not env_file.exists():
    print("[INCOMPLETE] Setup incomplete - .env file missing")
    print("             Run: cp .env.example .env")
elif not token or token == 'your_bot_token_here':
    print("[INCOMPLETE] Setup incomplete - configure .env file")
    print("             1. Get bot token from Discord Developer Portal")
    print("             2. Edit .env and replace 'your_bot_token_here'")
    print("             3. Run this test again")
else:
    print("[SUCCESS] Setup looks good! Ready to start the bot")
    print("          Run: python bot.py")

print("=" * 60)
print()
print("Documentation:")
print("  * START_HERE.md - Quick setup guide")
print("  * DISCORD_SETUP.md - Detailed Discord configuration")
print("  * QUICKSTART.md - Complete beginner guide")
print()
