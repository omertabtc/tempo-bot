#!/usr/bin/env python3
"""
Test if the bot still detects REAL scam patterns
Simulates various malicious contract patterns
"""
import asyncio
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.risk_engine import RiskEngine

# Simulated malicious contract source codes
SCAM_CONTRACTS = {
    "Honeypot - Can't Sell": """
    pragma solidity ^0.8.0;
    
    contract HoneypotToken {
        mapping(address => uint256) public balanceOf;
        mapping(address => bool) public isBlacklisted;
        address public owner;
        
        function transfer(address to, uint256 amount) public returns (bool) {
            require(!isBlacklisted[msg.sender], "Blacklisted");
            require(msg.sender == owner || to == owner, "Only owner can transfer");
            balanceOf[msg.sender] -= amount;
            balanceOf[to] += amount;
            return true;
        }
        
        function blacklist(address user) public {
            require(msg.sender == owner);
            isBlacklisted[user] = true;
        }
    }
    """,
    
    "Rug Pull - Owner Can Drain": """
    pragma solidity ^0.8.0;
    
    contract RugPull {
        address public owner;
        
        function mint(address to, uint256 amount) public {
            // Anyone can mint!
        }
        
        function drainAll() public {
            require(msg.sender == owner);
            payable(owner).transfer(address(this).balance);
        }
        
        function emergencyWithdraw() public {
            require(msg.sender == owner);
            // Drain all tokens
        }
    }
    """,
    
    "Malicious Proxy - Upgradeable Backdoor": """
    pragma solidity ^0.8.0;
    
    contract MaliciousProxy {
        address public implementation;
        address public owner;
        
        function upgradeTo(address newImplementation) public {
            // No onlyOwner! Anyone can upgrade!
            implementation = newImplementation;
        }
        
        fallback() external payable {
            address impl = implementation;
            assembly {
                calldatacopy(0, 0, calldatasize())
                let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
                returndatacopy(0, 0, returndatasize())
                switch result
                case 0 { revert(0, returndatasize()) }
                default { return(0, returndatasize()) }
            }
        }
    }
    """,
    
    "Self-Destruct Scam": """
    pragma solidity ^0.8.0;
    
    contract SelfDestructScam {
        address public owner;
        
        function destroy() public {
            require(msg.sender == owner);
            selfdestruct(payable(owner));
        }
    }
    """,
    
    "Unlimited Mint - No Max Supply": """
    pragma solidity ^0.8.0;
    
    contract UnlimitedMint {
        address public owner;
        uint256 public totalSupply;
        
        function mint(uint256 amount) public {
            require(msg.sender == owner);
            // No max supply check!
            totalSupply += amount;
        }
    }
    """,
    
    "Fee Manipulation": """
    pragma solidity ^0.8.0;
    
    contract FeeManipulation {
        uint256 public sellTax = 10;
        address public owner;
        
        function setSellTax(uint256 newTax) public {
            require(msg.sender == owner);
            sellTax = newTax; // Can set to 100%!
        }
        
        function transfer(address to, uint256 amount) public {
            uint256 tax = amount * sellTax / 100;
            // User loses tax
        }
    }
    """,
}

async def test_scam_pattern(name: str, source_code: str):
    """Test if a scam pattern is detected"""
    print("\n" + "="*70)
    print(f"Testing: {name}")
    print("="*70)
    
    analyzer = StaticAnalyzer()
    risk = RiskEngine()
    
    try:
        # Simulate contract data with source code
        contract_data = {
            'address': '0xSCAM000000000000000000000000000000000000',
            'verified': True,
            'source_code': source_code,
            'abi': [],
            'compiler_version': 'v0.8.0',
            'contract_name': name.replace(' ', '')
        }
        
        # Analyze
        findings = await analyzer.analyze(contract_data)
        
        # Generate report
        report = await risk.generate_report(
            contract_data['address'], 
            contract_data, 
            findings, 
            []
        )
        
        # Check results
        critical_count = len(report['critical_findings'])
        high_count = len(report['high_findings'])
        
        print(f"\nRisk Level: {report['risk_level'].upper()}")
        print(f"Risk Score: {report['risk_score']}/100")
        print(f"Critical Issues: {critical_count}")
        print(f"High Issues: {high_count}")
        
        # Verdict
        is_detected = report['risk_level'] in ['critical', 'high']
        
        if is_detected:
            print(f"\n✓ SUCCESS: Scam pattern DETECTED!")
            print(f"  Status: {report['risk_level'].upper()} RISK")
        else:
            print(f"\n✗ PROBLEM: Scam pattern NOT detected properly!")
            print(f"  Status: Only {report['risk_level'].upper()}")
            print(f"  This should be HIGH or CRITICAL!")
        
        # Show what was found
        if critical_count > 0:
            print(f"\nCritical issues found:")
            for i, finding in enumerate(report['critical_findings'][:3], 1):
                print(f"  {i}. {finding[:100]}")
        
        if high_count > 0:
            print(f"\nHigh issues found:")
            for i, finding in enumerate(report['high_findings'][:3], 1):
                print(f"  {i}. {finding[:100]}")
        
        return is_detected
        
    except Exception as e:
        print(f"\n✗ ERROR testing pattern: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Test all scam patterns"""
    print("\n" + "="*70)
    print(" SCAM DETECTION TEST")
    print(" Verifying the bot still catches malicious contracts")
    print("="*70)
    
    results = {}
    
    for name, source_code in SCAM_CONTRACTS.items():
        detected = await test_scam_pattern(name, source_code)
        results[name] = detected
        await asyncio.sleep(0.5)
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    detected_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for name, detected in results.items():
        status = "✓ DETECTED" if detected else "✗ MISSED"
        print(f"{status}: {name}")
    
    print("\n" + "="*70)
    print(f"Detection Rate: {detected_count}/{total_count} ({detected_count/total_count*100:.0f}%)")
    
    if detected_count == total_count:
        print("\n✓ PERFECT! All scam patterns detected!")
        print("The bot is still protecting users from malicious contracts.")
    elif detected_count >= total_count * 0.8:
        print(f"\n✓ GOOD! Most scams detected ({detected_count}/{total_count})")
        print("The bot catches the majority of malicious patterns.")
    else:
        print(f"\n✗ WARNING! Only {detected_count}/{total_count} scams detected")
        print("The bot may need improvement on scam detection.")
    
    print("="*70 + "\n")

if __name__ == '__main__':
    asyncio.run(main())
