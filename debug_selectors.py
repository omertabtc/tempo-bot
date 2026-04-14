#!/usr/bin/env python3
"""
Debug script to see what selectors are extracted from bytecode
"""
import asyncio
from analyzers.contract_fetcher import ContractFetcher
from analyzers.bytecode_patterns import BytecodePatternMatcher

async def debug_contract(address: str, name: str):
    """Debug selector extraction"""
    print("\n" + "="*70)
    print(f"{name}: {address}")
    print("="*70)
    
    fetcher = ContractFetcher()
    
    try:
        contract_data = await fetcher.fetch_contract(address)
        
        if contract_data.get('error'):
            print(f"ERROR: {contract_data['error']}")
            return
        
        bytecode = contract_data.get('bytecode', '')
        print(f"\nBytecode length: {len(bytecode)} chars")
        
        # Extract selectors
        selectors = BytecodePatternMatcher.extract_function_selectors(bytecode)
        print(f"\nExtracted {len(selectors)} function selectors:")
        for sel in sorted(selectors)[:20]:  # Show first 20
            print(f"  {sel}")
        
        if len(selectors) > 20:
            print(f"  ... and {len(selectors) - 20} more")
        
        # Check opcodes
        opcodes = BytecodePatternMatcher.detect_opcodes(bytecode)
        print(f"\nOpcodes found:")
        for op, count in opcodes.items():
            if count > 0:
                print(f"  {op}: {count}")
        
        # Try pattern matching
        pattern, confidence, desc = BytecodePatternMatcher.match_pattern(bytecode)
        print(f"\nPattern match:")
        print(f"  Pattern: {pattern}")
        print(f"  Description: {desc}")
        print(f"  Confidence: {confidence*100:.1f}%")
        
        # Check against known patterns
        print(f"\nChecking against known patterns:")
        for pattern_name, pattern_data in BytecodePatternMatcher.KNOWN_SAFE_PATTERNS.items():
            pattern_selectors = set(pattern_data['selectors'])
            common = selectors & pattern_selectors
            if common:
                match_pct = len(common) / len(pattern_selectors) * 100
                print(f"  {pattern_name}: {len(common)}/{len(pattern_selectors)} matches ({match_pct:.0f}%)")
                if len(common) <= 5:
                    print(f"    Matching: {list(common)}")
        
        await fetcher.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Debug all 3 contracts"""
    contracts = {
        'NFT Collection': '0x3e12fcb20ad532f653f2907d2ae511364e2ae696',
        'NFT Listing': '0x2a0A6fdA20EcBFaD07c62eCbF33e68B205A08776',
        'NFT Mint': '0xFdBc002555e155385D15acA9a6ee9dfbB897f7b5',
    }
    
    print("="*70)
    print(" SELECTOR EXTRACTION DEBUG")
    print("="*70)
    
    for name, addr in contracts.items():
        await debug_contract(addr, name)
        await asyncio.sleep(0.5)

if __name__ == '__main__':
    asyncio.run(main())
