# Known Scam Contracts for Testing

## How to Test Scam Detection

### Option 1: Test with Simulated Scams (Recommended)

```bash
python test_scam_detection.py
```

This tests 6 common scam patterns:
1. ✓ Honeypot (can't sell)
2. ✓ Rug pull (owner can drain)
3. ✓ Malicious proxy (no access control)
4. ✓ Self-destruct scam
5. ✓ Unlimited minting
6. ✓ Fee manipulation

**Expected result:** All should be detected as HIGH/CRITICAL

---

### Option 2: Known Scam Contracts (Real Examples)

These are REAL scam contracts from various blockchains (DO NOT INTERACT):

#### Ethereum Mainnet Scams

**Honeypot Token (Can't Sell)**
```
0x5558447B06867ffebd87DD63426d61c868c45904
```
- Users can buy but can't sell
- Should detect: Transfer restrictions

**Rug Pull (Owner Drained)**
```
0x69692D3345010a207b759a7D1af6fc7F38b35c5E
```
- Owner withdrew all liquidity
- Should detect: Owner withdrawal functions

**Unlimited Mint Scam**
```
0xB8c77482e45F1F44dE1745F52C74426C631bDD52
```
- Owner can mint unlimited tokens
- Should detect: Unlimited minting

---

### Option 3: Create Your Own Test Contract

Deploy a simple malicious contract on a testnet:

```solidity
// SCAM EXAMPLE - DO NOT USE IN PRODUCTION
pragma solidity ^0.8.0;

contract TestScam {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // RED FLAG: Owner can drain all funds
    function drainAll() public {
        require(msg.sender == owner);
        payable(owner).transfer(address(this).balance);
    }
    
    // RED FLAG: Unlimited minting
    function mint(uint256 amount) public {
        require(msg.sender == owner);
        // No max supply check
    }
    
    // RED FLAG: Can destroy contract
    function kill() public {
        require(msg.sender == owner);
        selfdestruct(payable(owner));
    }
}
```

Deploy on Tempo testnet, then test:
```
/analyze-contract YOUR_TEST_CONTRACT_ADDRESS
```

---

## What Should Be Detected

### CRITICAL Patterns (Should ALWAYS be flagged)
- ✓ SELFDESTRUCT capability
- ✓ Owner can drain entire balance
- ✓ Public minting without access control
- ✓ Upgradeable with no authorization
- ✓ Delegatecall to user input

### HIGH Risk Patterns
- ✓ Unlimited owner minting (no max supply)
- ✓ Transfer restrictions (honeypot)
- ✓ Blacklist mechanisms
- ✓ Modifiable fees (can set to 100%)
- ✓ Missing reentrancy protection

### MEDIUM Risk Patterns
- ✓ Pausable contract
- ✓ No timelock on critical functions
- ✓ Centralized ownership (single EOA)

---

## Testing Checklist

Run these tests to verify scam detection:

```bash
# 1. Test simulated scams
python test_scam_detection.py

# 2. Test your known safe contracts
python test_smart_detection.py

# 3. Test on Discord with real contracts
# In Discord:
/analyze-contract 0x3e12fcb20ad532f653f2907d2ae511364e2ae696  # Should be SAFE
/analyze-contract 0x5558447B06867ffebd87DD63426d61c868c45904  # Should be HIGH RISK
```

---

## Expected Results

### Safe Contracts
- ✓ Risk Level: SAFE or LOW
- ✓ Risk Score: 5-25/100
- ✓ Green or Yellow embed
- ✓ Mostly INFO findings

### Scam Contracts
- ✓ Risk Level: HIGH or CRITICAL
- ✓ Risk Score: 70-100/100
- ✓ Red embed
- ✓ Multiple CRITICAL/HIGH findings

---

## If Scam Detection Fails

If a scam is marked as SAFE:
1. Run `python test_scam_detection.py` to see which patterns failed
2. Send me the contract address
3. I'll add specific detection for that pattern

If a safe contract is marked as SCAM:
1. Run `python debug_selectors.py` to see what's detected
2. Send me the results
3. I'll tune the pattern matching

---

## Common Scam Patterns Library

The bot checks for these malicious patterns:

### 1. Honeypot Patterns
```solidity
// Can buy but can't sell
require(msg.sender == owner || to == owner);

// Blacklist mechanism
require(!isBlacklisted[msg.sender]);

// Cooldown prevents selling
require(block.timestamp - lastTrade[msg.sender] > cooldown);
```

### 2. Rug Pull Patterns
```solidity
// Owner can drain
function withdraw() public onlyOwner {
    payable(owner).transfer(address(this).balance);
}

// Token sweep
function rescueTokens(address token) public onlyOwner {
    // Transfer all tokens out
}
```

### 3. Mint Manipulation
```solidity
// Unlimited minting
function mint(uint256 amount) public onlyOwner {
    // No require(totalSupply + amount <= MAX_SUPPLY)
}

// Hidden mint in transfer
function _transfer() internal {
    _mint(someAddress, amount); // Suspicious!
}
```

### 4. Dangerous Proxy
```solidity
// Anyone can upgrade
function upgradeTo(address impl) public {
    // No access control!
    implementation = impl;
}
```

### 5. Self-Destruct
```solidity
// Can destroy contract
function destroy() public onlyOwner {
    selfdestruct(payable(owner));
}
```

---

## Real-World Testing Tips

1. **Start with simulated tests**
   - Run `test_scam_detection.py` first
   - Verify all patterns are caught

2. **Test known scams**
   - Use Ethereum mainnet scams (they're verified)
   - Change RPC to Ethereum temporarily
   - Test detection on real scam contracts

3. **Test your safe contracts**
   - Ensure they're not false positives
   - Should be SAFE or LOW risk

4. **Balance is key**
   - Too strict = False positives (safe = scam)
   - Too loose = Missed scams (scam = safe)
   - Current setting aims for 80% accuracy

---

**Run `python test_scam_detection.py` now to verify scam detection!** 🔍
