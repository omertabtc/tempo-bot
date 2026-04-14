#!/usr/bin/env python3
"""
Quick test script for the improved analyzer
Tests the contracts you mentioned
"""
import asyncio
import sys
from analyzers.contract_fetcher import ContractFetcher
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.onchain_checker import OnChainChecker
from analyzers.risk_engine import RiskEngine

# Your test contracts
TEST_CONTRACTS = {
    'NFT Collection': '0x3e12fcb20ad532f653f2907d2ae511364e2ae696',
    'Mint Contract': '0xFdBc002555e155385D15acA9a6ee9dfbB897f7b5',
}

async def test_contract(address: str, name: str):
    """Test a single contract"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Address: {address}")
    print(f"{'='*60}\n")
    
    fetcher = ContractFetcher()
    static = StaticAnalyzer()
    onchain = OnChainChecker()
    risk = RiskEngine()
    
    try:
        # Fetch
        print("→ Fetching contract data...")
        contract_data = await fetcher.fetch_contract(address)
        
        if contract_data.get('error'):
            print(f"✗ Error: {contract_data['error']}")
            return
        
        print(f"✓ Contract fetched")
        print(f"  Verified: {contract_data.get('verified')}")
        
        # Analyze
        print("\n→ Running static analysis...")
        static_findings = await static.analyze(contract_data)
        print(f"✓ Found {len(static_findings)} findings")
        
        # On-chain
        print("\n→ Checking on-chain state...")
        onchain_findings = await onchain.check(address, contract_data)
        print(f"✓ Found {len(onchain_findings)} on-chain findings")
        
        # Report
        print("\n→ Generating risk report...")
        report = await risk.generate_report(
            address, contract_data, static_findings, onchain_findings
        )
        
        # Display results
        print(f"\n{'='*60}")
        print(f"RESULTS for {name}")
        print(f"{'='*60}")
        print(f"Risk Level: {report['risk_level'].upper()}")
        print(f"Risk Score: {report['risk_score']}/100")
        print(f"Contract Type: {report['contract_type']}")
        print(f"Total Issues: {report['total_issues']}")
        
        print(f"\nFindings by Severity:")
        print(f"  CRITICAL: {len(report['critical_findings'])}")
        print(f"  HIGH:     {len(report['high_findings'])}")
        print(f"  MEDIUM:   {len(report['medium_findings'])}")
        print(f"  LOW:      {len(report['low_findings'])}")
        print(f"  INFO:     {len(report.get('info_findings', []))}")
        
        if report['critical_findings']:
            print(f"\n🔴 CRITICAL Issues:")
            for i, finding in enumerate(report['critical_findings'][:3], 1):
                print(f"  {i}. {finding[:100]}...")
        
        if report['high_findings']:
            print(f"\n🟠 HIGH Issues:")
            for i, finding in enumerate(report['high_findings'][:3], 1):
                print(f"  {i}. {finding[:100]}...")
        
        if report['medium_findings']:
            print(f"\n🟡 MEDIUM Issues:")
            for i, finding in enumerate(report['medium_findings'][:3], 1):
                print(f"  {i}. {finding[:100]}...")
        
        print(f"\n💡 Recommendation:")
        print(f"{report['recommendation'][:200]}...")
        
        await fetcher.close()
        
    except Exception as e:
        print(f"✗ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print(" TEMPO CONTRACT ANALYZER - IMPROVED v2 TEST")
    print("="*60)
    
    for name, address in TEST_CONTRACTS.items():
        await test_contract(address, name)
        await asyncio.sleep(1)  # Brief pause between tests
    
    print(f"\n{'='*60}")
    print("All tests complete!")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
