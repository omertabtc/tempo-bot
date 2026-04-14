#!/usr/bin/env python3
"""
Test smart bytecode detection on your 3 safe contracts
"""
import asyncio
from analyzers.contract_fetcher import ContractFetcher
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.risk_engine import RiskEngine

# Your 3 SAFE contracts
TEST_CONTRACTS = {
    'NFT Collection': '0x3e12fcb20ad532f653f2907d2ae511364e2ae696',
    'NFT Listing': '0x2a0A6fdA20EcBFaD07c62eCbF33e68B205A08776',
    'NFT Mint': '0xFdBc002555e155385D15acA9a6ee9dfbB897f7b5',
}

async def test_contract(address: str, name: str):
    """Test smart detection on one contract"""
    print("\n" + "="*70)
    print(f"Testing: {name}")
    print(f"Address: {address}")
    print("="*70)
    
    fetcher = ContractFetcher()
    analyzer = StaticAnalyzer()
    risk = RiskEngine()
    
    try:
        # Fetch
        print("\n[1/3] Fetching contract from Tempo...")
        contract_data = await fetcher.fetch_contract(address)
        
        if contract_data.get('error'):
            print(f"[ERROR] {contract_data['error']}")
            return
        
        print(f"[OK] Contract fetched")
        print(f"  Verified: {contract_data.get('verified')}")
        
        # Analyze with SMART detection
        print("\n[2/3] Running SMART bytecode analysis...")
        findings = await analyzer.analyze(contract_data)
        
        print(f"[OK] Analysis complete")
        print(f"  Total findings: {len(findings)}")
        
        # Breakdown
        critical = [f for f in findings if f['severity'] == 'critical']
        high = [f for f in findings if f['severity'] == 'high']
        medium = [f for f in findings if f['severity'] == 'medium']
        low = [f for f in findings if f['severity'] == 'low']
        info = [f for f in findings if f['severity'] == 'info']
        
        print(f"\nFindings by severity:")
        print(f"  CRITICAL: {len(critical)}")
        print(f"  HIGH:     {len(high)}")
        print(f"  MEDIUM:   {len(medium)}")
        print(f"  LOW:      {len(low)}")
        print(f"  INFO:     {len(info)}")
        
        # Generate report
        print("\n[3/3] Generating risk report...")
        report = await risk.generate_report(
            address, contract_data, findings, []
        )
        
        # Results
        print("\n" + "="*70)
        print("RESULTS:")
        print("="*70)
        print(f"Risk Level: {report['risk_level'].upper()}")
        print(f"Risk Score: {report['risk_score']}/100")
        print(f"Contract Type: {report['contract_type']}")
        
        # Show key findings
        if info:
            print(f"\n[INFO] Findings:")
            for f in info[:3]:
                print(f"  - {f['title']}")
        
        if critical:
            print(f"\n[CRITICAL] Issues:")
            for f in critical[:2]:
                print(f"  - {f['title']}")
        
        if high:
            print(f"\n[HIGH] Issues:")
            for f in high[:2]:
                print(f"  - {f['title']}")
        
        # Verdict
        print("\n" + "="*70)
        if report['risk_level'] in ['safe', 'low']:
            print("[SUCCESS] Contract recognized as SAFE!")
            print("Smart detection is working!")
        elif report['risk_level'] == 'medium':
            print("[OK] Contract marked as MEDIUM risk")
            print("Not perfect but better than HIGH!")
        else:
            print("[NEEDS IMPROVEMENT] Still marked as HIGH/CRITICAL")
            print("Pattern matching needs tuning for this contract type")
        print("="*70)
        
        await fetcher.close()
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Test all 3 contracts"""
    print("\n" + "="*70)
    print(" SMART BYTECODE DETECTION TEST")
    print(" Testing your 3 SAFE contracts")
    print("="*70)
    
    for name, address in TEST_CONTRACTS.items():
        await test_contract(address, name)
        await asyncio.sleep(1)
    
    print("\n" + "="*70)
    print(" TEST COMPLETE!")
    print("="*70)
    print("\nIf the contracts are marked as SAFE/LOW:")
    print("  -> Smart detection is working!")
    print("  -> Similar contracts will be recognized")
    print("\nIf still marked as HIGH:")
    print("  -> We need to tune the patterns")
    print("  -> Send me the results and I'll improve it")
    print("="*70 + "\n")

if __name__ == '__main__':
    asyncio.run(main())
