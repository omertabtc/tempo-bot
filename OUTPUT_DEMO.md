# Visual Output Demo

## What Users See in Discord

This document shows EXACTLY what the Discord embeds look like for different risk levels.

---

## 🟢 SAFE Contract (Green Embed)

**Embed Color:** `#00FF00` (Bright Green)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Tempo Contract Analysis: 0xA0b8...69Af                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Full Address: 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48

📄 Contract Type          ✅ Verification Status
💰 ERC-20 Token           ✅ Verified
                          v0.8.19+commit.7dd6d404

───────────────────────────────────────────────────────────────

🛡️ Risk Summary

✅ SAFE - This contract appears safe based on static and 
on-chain analysis. No major risks detected.

Risk Score: 8/100 (Low)

───────────────────────────────────────────────────────────────

🔍 Key Findings

✅ No significant security issues detected.

───────────────────────────────────────────────────────────────

💡 Recommendations

✅ Proceed with caution:
• Contract appears relatively safe
• Still recommended to start with small amounts
• Verify the contract does what you expect
• Check for professional audit reports

───────────────────────────────────────────────────────────────

Analysis powered by AI static + on-chain checks. Always DYOR. 
Not financial advice. This is not a substitute for professional 
audit.
```

---

## 🟡 WARNING Contract (Yellow Embed)

**Embed Color:** `#FFFF00` (Bright Yellow)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Tempo Contract Analysis: 0xDEAD...C0DE                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Full Address: 0xDEADC0DE1234567890ABCDEFDEADC0DE12345678

📄 Contract Type          ✅ Verification Status
❓ Unknown                ❌ Not Verified
                          Unknown

───────────────────────────────────────────────────────────────

🛡️ Risk Summary

⚠️ WARNING - Moderate risks detected.

• 1 HIGH issue(s)
• 2 MEDIUM issue(s)

Risk Score: 55/100 (Medium)

───────────────────────────────────────────────────────────────

🔍 Key Findings

🟠 HIGH: Unverified Contract
Source code is not verified on Tempo blockchain explorer. 
Full security analysis impossible. Proceed with extreme 
caution. Without source code, we can only perform limited 
bytecode analysis.

🟡 MEDIUM: Delegatecall in Bytecode
DELEGATECALL opcode (0xf4) detected in contract bytecode. 
This can execute arbitrary code in the contract's context. 
Cannot verify safety without source code.

🟡 MEDIUM: No Max Supply Found
Current supply exists but no max supply detected on-chain. 
Token supply may be unlimited or changeable by owner.

───────────────────────────────────────────────────────────────

💡 Recommendations

⚠️ Exercise caution:
• Review the identified risks carefully
• Only interact if you understand the implications
• Use small test amounts first
• Check team reputation and social channels
• Wait for professional audit if possible

───────────────────────────────────────────────────────────────

Analysis powered by AI static + on-chain checks. Always DYOR. 
Not financial advice. This is not a substitute for professional 
audit.
```

---

## 🔴 HIGH RISK Contract (Red Embed)

**Embed Color:** `#FF0000` (Bright Red)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Tempo Contract Analysis: 0xBAD0...BEEF                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Full Address: 0xBAD0C0DEBA5EBA11DEADBEEF12345678DEADBEEF

📄 Contract Type          ✅ Verification Status
🎨 ERC-721 NFT            ✅ Verified
Mint Contract             v0.8.0+commit.c7dfd78e

───────────────────────────────────────────────────────────────

🛡️ Risk Summary

⚠️ HIGH RISK - Potential for asset/fund loss!

This contract exhibits dangerous patterns that could result 
in loss of funds or assets.

Risk Score: 95/100 (CRITICAL)

───────────────────────────────────────────────────────────────

🔍 Key Findings

🔴 CRITICAL: Owner Can Drain Contract Balance
Function detected that allows owner to withdraw entire contract 
balance. The owner can call withdrawAll() at any time to drain 
all ETH and tokens held by the contract. This is a common rug 
pull pattern.

🔴 CRITICAL: Unlimited Owner Minting
Owner can mint unlimited tokens/NFTs with no max supply 
enforcement detected. The mint() function has onlyOwner modifier 
but contains no require() check against MAX_SUPPLY. Owner could 
mint infinite supply, diluting value.

🔴 CRITICAL: Upgradeable Proxy with Owner Control
Contract can be upgraded by owner at any time. Logic can be 
completely changed. Uses UUPS (Universal Upgradeable Proxy 
Standard) pattern with owner-only _authorizeUpgrade() function. 
Owner could replace entire contract logic maliciously.

🟠 HIGH: Blacklist Mechanism Detected
Contract can blacklist addresses, preventing them from 
transferring tokens. The _beforeTokenTransfer() hook checks an 
isBlacklisted mapping controlled by owner. You could be 
prevented from selling or transferring your NFTs.

🟠 HIGH: Metadata Can Be Changed by Owner
Owner can modify baseURI, potentially changing all NFT metadata 
after mint. The setBaseURI() function is callable by owner with 
no timelock or restrictions. Your NFT's image and properties 
could change at any time.

🟡 MEDIUM: No Timelock or Multisig Detected
Owner can execute privileged functions immediately without delay 
or consensus. Single EOA wallet controls critical functions with 
no time delay for community to react.

───────────────────────────────────────────────────────────────

💡 Recommendations

🛑 DO NOT APPROVE OR SEND FUNDS:
• This contract has critical security issues
• High risk of losing your assets/funds
• If already interacted, revoke approvals immediately
• Wait for professional security audit
• Avoid until issues are addressed

To revoke approvals:
• Visit revoke.cash or similar tool
• Search for this contract address
• Revoke all token approvals

───────────────────────────────────────────────────────────────

Analysis powered by AI static + on-chain checks. Always DYOR. 
Not financial advice. This is not a substitute for professional 
audit.
```

---

## ⏱️ Rate Limit Message

**Embed Color:** `#FFA500` (Orange) - Ephemeral (only user sees it)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ⏱️ Rate Limit Exceeded             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

You can analyze up to 3 contracts per 60 seconds.

Please try again in 42 seconds.
```

*This message is only visible to you*

---

## ❌ Error Messages

### Invalid Address Format

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ❌ Invalid Address                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

The address `0x123` is not a valid Ethereum address.

Expected format: `0x` followed by 40 hexadecimal 
characters

Example: 0x1234567890abcdef1234567890abcdef12345678
```

### Contract Not Found

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ❌ Contract Not Found              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Address: 0x0000000000000000000000000000000000000000

Error: No contract code found at this address. 
It may be an EOA (wallet) or undeployed contract.

Please verify:
• The address is correct
• The contract exists on Tempo blockchain
• The contract is deployed (not just an EOA)
```

### Analysis Timeout

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ⏱️ Analysis Timeout                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Analysis of `0x1234...5678` took too long.

This may happen with very large or complex contracts.

Please try again or contact support if this persists.
```

---

## 📊 Progress Messages

While analyzing, users see:

### Step 1
```
🔍 Analyzing Contract

Address: 0x1234567890abcdef1234567890abcdef12345678

⏳ Fetching contract data from Tempo blockchain...
```

### Step 2
```
🔍 Analyzing Contract

Address: 0x1234567890abcdef1234567890abcdef12345678
Status: Contract found!

⏳ Performing static code analysis...
```

### Step 3
```
🔍 Analyzing Contract

Address: 0x1234567890abcdef1234567890abcdef12345678
Status: Static analysis complete!

⏳ Checking on-chain state...
```

### Step 4
```
🔍 Analyzing Contract

Address: 0x1234567890abcdef1234567890abcdef12345678
Status: On-chain analysis complete!

⏳ Generating security report...
```

Then the final report appears and the progress message is deleted.

---

## 💡 Key Visual Elements

### Risk Level Indicators

**Safe:**
- Embed: Bright green (#00FF00)
- Icon: ✅
- Text: "SAFE - This contract appears safe..."

**Warning:**
- Embed: Bright yellow (#FFFF00)
- Icon: ⚠️
- Text: "WARNING - Moderate risks detected"

**High Risk:**
- Embed: Bright red (#FF0000)
- Icon: ⚠️
- Text: "HIGH RISK - Potential for asset/fund loss!"

### Severity Tags in Findings

- 🔴 **CRITICAL:** - Most dangerous issues
- 🟠 **HIGH:** - Serious security concerns
- 🟡 **MEDIUM:** - Notable risks to consider
- 🟢 **LOW:** - Minor issues or informational

---

## 🎨 Embed Structure

Every analysis report follows this exact structure:

1. **Title bar** - "Tempo Contract Analysis: [short address]"
2. **Description** - Full contract address
3. **Field: Contract Type** - Inline, left
4. **Field: Verification Status** - Inline, right
5. **Field: (spacing)** - Inline (creates row)
6. **Field: Risk Summary** - Full width
7. **Field: Key Findings** - Full width (may split if long)
8. **Field: Recommendations** - Full width
9. **Footer** - Standard disclaimer

All fields have clear labels with emoji icons for easy scanning.

---

## 📱 Mobile vs Desktop

The embeds are responsive and look great on:

- **Desktop Discord** - Full width, all fields visible
- **Mobile Discord** - Stacked vertically, easy to scroll
- **Web Discord** - Same as desktop

The color coding makes risk levels obvious at a glance on any device!

---

This is exactly what users will see when they run `/analyze-contract`! 🎉
