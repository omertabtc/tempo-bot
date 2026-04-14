#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic script for contract analysis
"""
import asyncio
import sys
import os

# Fix Windows console encoding
if os.name == 'nt':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

from analyzers.contract_fetcher import ContractFetcher
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.risk_engine import RiskEngine

async def diagnose(address):
    """Diagnose a specific contract"""
    print(f"\n{'='*60}")
    print(f"DIAGNOSTIC - Contract: {address}")
    print(f"{'='*60}\n")
    
    fetcher = ContractFetcher()
    analyzer = StaticAnalyzer()
    risk = RiskEngine()
    
    try:
        # Step 1: Fetch
        print("[1/4] Fetching contract...")
        contract_data = await fetcher.fetch_contract(address)
        
        if contract_data.get('error'):
            print(f"❌ ERROR: {contract_data['error']}")
            print("\nPossible reasons:")
            print("  • Contract not on Tempo blockchain")
            print("  • Invalid address")
            print("  • RPC connection issue")
            return
        
        print(f"✓ Contract fetched successfully")
        print(f"  Verified: {contract_data.get('verified')}")
        print(f"  Has source: {bool(contract_data.get('source_code'))}")
        
        if not contract_data.get('verified'):
            print("\n⚠️  Contract is NOT VERIFIED")
            print("   The bot can only do limited bytecode analysis.")
            print("   This may result in higher risk scores.")
            await fetcher.close()
            return
        
        # Step 2: Check source code length
        source = contract_data.get('source_code', '')
        print(f"  Source length: {len(source)} chars")
        
        if len(source) < 100:
            print("\n❌ Source code too short or missing")
            await fetcher.close()
            return
        
        # Step 3: Analyze with context detection
        print("\n[2/4] Running smart analysis...")
        findings = await analyzer.analyze(contract_data)
        
        print(f"✓ Analysis complete")
        print(f"  Contract purpose: {analyzer.contract_purpose}")
        print(f"  OpenZeppelin: {analyzer.is_openzeppelin}")
        print(f"  Confidence: {analyzer.confidence_score:.2f}")
        print(f"  Total findings: {len(findings)}")
        
        # Step 4: Show findings breakdown
        print("\n[3/4] Findings by severity:")
        critical = [f for f in findings if f['severity'] == 'critical']
        high = [f for f in findings if f['severity'] == 'high']
        medium = [f for f in findings if f['severity'] == 'medium']
        low = [f for f in findings if f['severity'] == 'low']
        info = [f for f in findings if f['severity'] == 'info']
        
        print(f"  CRITICAL: {len(critical)}")
        print(f"  HIGH:     {len(high)}")
        print(f"  MEDIUM:   {len(medium)}")
        print(f"  LOW:      {len(low)}")
        print(f"  INFO:     {len(info)}")
        
        # Step 5: Generate report
        print("\n[4/4] Generating risk report...")
        report = await risk.generate_report(
            address, contract_data, findings, []
        )
        
        print(f"\n{'='*60}")
        print(f"FINAL RESULT")
        print(f"{'='*60}")
        print(f"Risk Level: {report['risk_level'].upper()}")
        print(f"Risk Score: {report['risk_score']}/100")
        print(f"Contract Type: {report['contract_type']}")
        
        if len(critical) > 0:
            print(f"\n❌ CRITICAL issues found:")
            for i, f in enumerate(critical[:3], 1):
                print(f"  {i}. {f['title']}")
        
        if len(high) > 0:
            print(f"\n⚠️  HIGH issues found:")
            for i, f in enumerate(high[:3], 1):
                print(f"  {i}. {f['title']}")
        
        if len(medium) > 0:
            print(f"\n🟡 MEDIUM issues found:")
            for i, f in enumerate(medium[:3], 1):
                print(f"  {i}. {f['title']}")
        
        print(f"\n{'='*60}")
        print("DIAGNOSIS:")
        print(f"{'='*60}")
        
        if report['risk_level'] in ['critical', 'high']:
            print("⚠️  Contract marked as HIGH RISK because:")
            if len(critical) > 0:
                print(f"   • {len(critical)} CRITICAL issue(s) found")
            if len(high) > 0:
                print(f"   • {len(high)} HIGH severity issue(s) found")
            print("\nIf this is a legitimate contract, the issues might be:")
            print("  • False positives (we're improving detection)")
            print("  • Real risks that need attention")
            print("  • Standard patterns not yet recognized")
        else:
            print("✓ Contract risk level is acceptable")
        
        await fetcher.close()
        
    except Exception as e:
        print(f"\n❌ ERROR during diagnosis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Use default test address
        address = '0x3e12fcb20ad532f653f2907d2ae511364e2ae696'
        print(f"No address provided, using test: {address}")
    else:
        address = sys.argv[1]
    
    asyncio.run(diagnose(address))
