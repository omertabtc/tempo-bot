#!/usr/bin/env python3
"""
Find where a contract is deployed and verified
"""
import asyncio
import aiohttp

async def check_explorer(url, chain_name):
    """Check if contract exists on this explorer"""
    print(f"\nChecking {chain_name}...")
    print(f"URL: {url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    # Check for verification indicators
                    is_verified = any(keyword in text.lower() for keyword in [
                        'contract source code verified',
                        'verified contract',
                        'contract verified',
                        'sourcecode'
                    ])
                    
                    has_contract = 'contract' in text.lower() and response.status == 200
                    
                    if has_contract:
                        print(f"  [FOUND] Contract exists on {chain_name}")
                        if is_verified:
                            print(f"  [VERIFIED] Source code appears to be verified!")
                            return True
                        else:
                            print(f"  [NOT VERIFIED] Contract found but not verified")
                    else:
                        print(f"  [NOT FOUND] on {chain_name}")
                else:
                    print(f"  [ERROR] HTTP {response.status}")
    except asyncio.TimeoutError:
        print(f"  [TIMEOUT] Explorer not responding")
    except Exception as e:
        print(f"  [ERROR] {str(e)[:50]}")
    
    return False

async def find_contract(address):
    """Try to find the contract on various explorers"""
    print("="*60)
    print(f"SEARCHING FOR CONTRACT: {address}")
    print("="*60)
    
    # List of explorers to check
    explorers = [
        # Tempo explorers
        (f"https://contracts.tempo.xyz/address/{address}", "Tempo (contracts.tempo.xyz)"),
        (f"https://explore.tempo.xyz/address/{address}", "Tempo (explore.tempo.xyz)"),
        (f"https://temposcan.io/address/{address}", "Tempo (temposcan.io)"),
        
        # Ethereum
        (f"https://etherscan.io/address/{address}", "Ethereum Mainnet"),
        
        # BSC
        (f"https://bscscan.com/address/{address}", "Binance Smart Chain"),
        
        # Polygon
        (f"https://polygonscan.com/address/{address}", "Polygon"),
        
        # Arbitrum
        (f"https://arbiscan.io/address/{address}", "Arbitrum"),
        
        # Optimism
        (f"https://optimistic.etherscan.io/address/{address}", "Optimism"),
        
        # Avalanche
        (f"https://snowtrace.io/address/{address}", "Avalanche"),
        
        # Fantom
        (f"https://ftmscan.com/address/{address}", "Fantom"),
    ]
    
    print("\nChecking multiple blockchain explorers...")
    print("This may take a minute...\n")
    
    found_on = []
    
    for url, chain in explorers:
        verified = await check_explorer(url, chain)
        if verified:
            found_on.append((chain, url))
        await asyncio.sleep(0.5)  # Be nice to explorers
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    
    if found_on:
        print(f"\nContract FOUND and VERIFIED on:")
        for chain, url in found_on:
            print(f"  - {chain}")
            print(f"    {url}")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("\nTo configure the bot for this chain:")
        print("1. Edit .env file")
        print("2. Update these values based on the chain above")
        print("3. Restart the bot")
        
        if "Ethereum" in found_on[0][0]:
            print("\nFor Ethereum Mainnet:")
            print("  TEMPO_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY")
            print("  TEMPO_EXPLORER_API=https://api.etherscan.io/api")
            print("  TEMPO_CHAIN_ID=1")
        elif "BSC" in found_on[0][0]:
            print("\nFor BSC:")
            print("  TEMPO_RPC_URL=https://bsc-dataseed.binance.org")
            print("  TEMPO_EXPLORER_API=https://api.bscscan.com/api")
            print("  TEMPO_CHAIN_ID=56")
        elif "Polygon" in found_on[0][0]:
            print("\nFor Polygon:")
            print("  TEMPO_RPC_URL=https://polygon-rpc.com")
            print("  TEMPO_EXPLORER_API=https://api.polygonscan.com/api")
            print("  TEMPO_CHAIN_ID=137")
    else:
        print("\nContract NOT FOUND on any checked explorer.")
        print("\nPossible reasons:")
        print("  1. Contract is on a different/private blockchain")
        print("  2. Contract address is incorrect")
        print("  3. Contract exists but explorers are down")
        print("\nPlease verify:")
        print("  - The contract address is correct")
        print("  - Which blockchain it's deployed on")
        print("  - Share the explorer URL where you can see it")

if __name__ == '__main__':
    address = '0x3e12fcb20ad532f653f2907d2ae511364e2ae696'
    asyncio.run(find_contract(address))
