#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-deployment check - Verifies everything is ready for hosting
"""
import os
import sys
import io
from pathlib import Path

# Fix Windows console encoding
if os.name == 'nt':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

def check_files():
    """Check required files exist"""
    print("\n[1/5] Checking required files...")
    
    required_files = [
        'bot.py',
        'requirements.txt',
        'config.py',
        '.env',
        '.gitignore',
        'Procfile',
        'railway.json',
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING!")
            missing.append(file)
    
    return len(missing) == 0

def check_gitignore():
    """Verify .env is in .gitignore"""
    print("\n[2/5] Checking .gitignore...")
    
    if not Path('.gitignore').exists():
        print("  ✗ .gitignore missing!")
        return False
    
    with open('.gitignore', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if '.env' in content:
        print("  ✓ .env is in .gitignore (GOOD - won't push secrets)")
    else:
        print("  ⚠️  .env NOT in .gitignore! Add it to avoid pushing secrets!")
        return False
    
    return True

def check_env_file():
    """Check .env has required variables"""
    print("\n[3/5] Checking .env configuration...")
    
    if not Path('.env').exists():
        print("  ✗ .env file not found!")
        print("    Create it from .env.example")
        return False
    
    with open('.env', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    required_vars = [
        'DISCORD_TOKEN',
        'TEMPO_RPC_URL',
        'TEMPO_EXPLORER_API',
        'TEMPO_CHAIN_ID',
    ]
    
    missing = []
    for var in required_vars:
        if var in content and 'your_' not in content.lower():
            print(f"  ✓ {var} is set")
        else:
            print(f"  ✗ {var} not configured!")
            missing.append(var)
    
    return len(missing) == 0

def check_dependencies():
    """Check dependencies can be installed"""
    print("\n[4/5] Checking dependencies...")
    
    try:
        import discord
        print("  ✓ discord.py installed")
    except ImportError:
        print("  ✗ discord.py not installed")
        print("    Run: pip install -r requirements.txt")
        return False
    
    try:
        import web3
        print("  ✓ web3 installed")
    except ImportError:
        print("  ✗ web3 not installed")
        return False
    
    return True

def check_bot_runs():
    """Check if bot.py can be imported"""
    print("\n[5/5] Checking if bot can start...")
    
    try:
        # Try to import config
        sys.path.insert(0, os.getcwd())
        import config
        print("  ✓ config.py loads successfully")
        
        # Check if token is set
        token = config.DISCORD_TOKEN
        if token and 'your_' not in token.lower():
            print("  ✓ Discord token configured")
        else:
            print("  ✗ Discord token not configured!")
            return False
        
        print("  ✓ Bot should be able to start")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all checks"""
    print("="*60)
    print(" PRE-DEPLOYMENT CHECK")
    print(" Verifying bot is ready for hosting")
    print("="*60)
    
    results = {
        'Files': check_files(),
        'Gitignore': check_gitignore(),
        'Environment': check_env_file(),
        'Dependencies': check_dependencies(),
        'Configuration': check_bot_runs(),
    }
    
    print("\n" + "="*60)
    print(" RESULTS")
    print("="*60)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print(" ✓ ALL CHECKS PASSED!")
        print(" Your bot is ready for deployment!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Push to GitHub: run deploy/push_to_github.bat")
        print("  2. Deploy on Railway: https://railway.app/")
        print("  3. Add environment variables in Railway")
        print("\nSee HEBERGER_RAPIDE.md for detailed instructions!")
    else:
        print(" ✗ SOME CHECKS FAILED!")
        print(" Fix the issues above before deploying.")
        print("="*60)
        print("\nCommon fixes:")
        print("  - Missing .env: cp .env.example .env (then edit it)")
        print("  - Missing packages: pip install -r requirements.txt")
        print("  - Missing .gitignore: Add '.env' to it")
    
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
