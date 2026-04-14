# Analysis Examples & Customization

## Example Analysis Results

### Example 1: Safe ERC-20 Token (Green Embed)

**Command:**
```
/analyze-contract 0xabcd...1234
```

**Result (Green #00FF00 embed):**
```
╔══════════════════════════════════════════════════╗
║  Tempo Contract Analysis: 0xabcd...1234         ║
╚══════════════════════════════════════════════════╝

Full Address: 0xabcd1234567890abcdef1234567890abcd1234

📄 Contract Type: 💰 ERC-20 Token
✅ Verification Status: ✅ Verified
Compiler: v0.8.19+commit.7dd6d404

🛡️ Risk Summary
✅ SAFE - This contract appears safe based on static and 
on-chain analysis. No major risks detected.

Risk Score: 8/100 (Low)

🔍 Key Findings
✅ No significant security issues detected.

💡 Recommendations
✅ Proceed with caution:
• Contract appears relatively safe
• Still recommended to start with small amounts
• Verify the contract does what you expect
• Check for professional audit reports

Analysis powered by AI static + on-chain checks. Always DYOR. 
Not financial advice. This is not a substitute for professional audit.
```

---

### Example 2: Dangerous NFT Mint Contract (Red Embed)

**Command:**
```
/analyze-contract 0xbad...beef
```

**Result (Red #FF0000 embed):**
```
╔══════════════════════════════════════════════════╗
║  Tempo Contract Analysis: 0xbad0...beef         ║
╚══════════════════════════════════════════════════╝

Full Address: 0xbad0c0deba5eba11deadbeef12345678deadbeef

📄 Contract Type: 🎨 ERC-721 NFT Mint Contract
✅ Verification Status: ✅ Verified
Compiler: v0.8.0+commit.c7dfd78e

🛡️ Risk Summary
⚠️ HIGH RISK - Potential for asset/fund loss!

This contract exhibits dangerous patterns that could result 
in loss of funds or assets.

Risk Score: 95/100 (CRITICAL)

🔍 Key Findings

🔴 CRITICAL: Owner Can Drain Contract Balance
Function detected that allows owner to withdraw entire contract 
balance. The owner can call withdrawAll() at any time to drain 
all ETH and tokens from the contract.

🔴 CRITICAL: Unlimited Owner Minting
Owner can mint unlimited tokens/NFTs with no max supply 
enforcement detected. The mint() function has onlyOwner modifier 
but no require() check against MAX_SUPPLY.

🔴 CRITICAL: Upgradeable Proxy with Owner Control
Contract can be upgraded by owner at any time. Logic can be 
completely changed. Uses UUPS pattern with owner-only 
_authorizeUpgrade().

🟠 HIGH: Blacklist Mechanism Detected
Contract can blacklist addresses, preventing them from 
transferring tokens. The _beforeTokenTransfer hook checks 
isBlacklisted mapping.

🟠 HIGH: Metadata Can Be Changed by Owner
Owner can modify baseURI, potentially changing all NFT metadata. 
The setBaseURI() function is callable by owner with no timelock.

💡 Recommendations
🛑 DO NOT APPROVE OR SEND FUNDS:
• This contract has critical security issues
• High risk of losing your assets/funds
• If already interacted, revoke approvals immediately
• Wait for professional security audit
• Avoid until issues are addressed

Analysis powered by AI static + on-chain checks. Always DYOR. 
Not financial advice. This is not a substitute for professional audit.
```

---

### Example 3: Unverified Contract (Yellow Warning)

**Command:**
```
/analyze-contract 0xdead...c0de
```

**Result (Yellow #FFFF00 embed):**
```
╔══════════════════════════════════════════════════╗
║  Tempo Contract Analysis: 0xdead...c0de         ║
╚══════════════════════════════════════════════════╝

Full Address: 0xdeadc0de1234567890abcdefdeadc0de12345678

📄 Contract Type: ❓ Unknown (Unverified)
✅ Verification Status: ❌ Not Verified
Compiler: Unknown

🛡️ Risk Summary
⚠️ WARNING - Moderate risks detected.

• 1 HIGH issue(s)
• 1 MEDIUM issue(s)

Risk Score: 55/100 (Medium)

🔍 Key Findings

🟠 HIGH: Unverified Contract
Source code is not verified on Tempo blockchain explorer. 
Full security analysis impossible. Proceed with extreme caution. 
Without source code, we can only perform limited bytecode analysis.

🟡 MEDIUM: Delegatecall in Bytecode
DELEGATECALL opcode (0xf4) detected in contract bytecode. 
This can execute arbitrary code in the contract's context. 
Cannot verify safety without source code.

💡 Recommendations
⚠️ Exercise caution:
• Review the identified risks carefully
• Only interact if you understand the implications
• Use small test amounts first
• Check team reputation and social channels
• Wait for professional audit if possible

Analysis powered by AI static + on-chain checks. Always DYOR. 
Not financial advice. This is not a substitute for professional audit.
```

---

### Example 4: Rate Limit Exceeded

**Scenario:** User tries to analyze more than 3 contracts in 60 seconds

**Result:**
```
╔══════════════════════════════════════╗
║  ⏱️ Rate Limit Exceeded             ║
╚══════════════════════════════════════╝

You can analyze up to 3 contracts per 60 seconds.

Please try again in 45 seconds.

(This message is only visible to you)
```

**Note:** Rate limiting is per-user to prevent abuse and ensure fair usage. The limits can be configured in `.env`:
```env
RATE_LIMIT_WINDOW=60  # Time window in seconds
RATE_LIMIT_MAX=3      # Max analyses per window
```

---

## Customizing Detection Rules

### Adding Custom Vulnerability Checks

Edit `analyzers/static_analyzer.py` and add a new check function:

```python
async def _check_my_custom_pattern(self, source: str):
    """Check for my custom vulnerability pattern"""
    
    # Example: Detect contracts that can freeze specific addresses
    if re.search(r'function\s+freeze\w*\s*\([^)]*address', source, re.IGNORECASE):
        self._add_finding(
            'high',
            'Address Freeze Capability',
            'Contract can freeze specific addresses, preventing their transfers.'
        )
```

Then call it in the `analyze()` method:
```python
async def analyze(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    # ... existing checks ...
    await self._check_my_custom_pattern(source_code)
    return self.findings
```

### Adjusting Risk Weights

Edit `config.py` to change how findings affect the risk score:

```python
RISK_WEIGHTS = {
    'critical': 150,  # Increased from 100
    'high': 60,       # Increased from 50
    'medium': 20,
    'low': 5,
    'info': 0         # Changed from 1 (ignore in scoring)
}
```

### Whitelisting Known Safe Patterns

Add to `static_analyzer.py`:

```python
# At the top of the class
SAFE_OWNER_ADDRESSES = [
    '0x0000000000000000000000000000000000000001',  # Gnosis Safe deployer
    # Add more known safe addresses
]

async def _check_ownership_risks(self, source: str):
    owner = await self._call_function(address, 'owner()', [])
    
    if owner in self.SAFE_OWNER_ADDRESSES:
        self._add_finding('info', 'Owner is Known Safe Contract', 
                         f'Owner {owner} is a recognized safe contract.')
        return  # Skip other ownership checks
```

---

## Advanced Usage

### Running Analysis Programmatically

You can use the analyzer without Discord:

```python
import asyncio
from analyzers.contract_fetcher import ContractFetcher
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.onchain_checker import OnChainChecker
from analyzers.risk_engine import RiskEngine

async def analyze_contract(address: str):
    fetcher = ContractFetcher()
    static = StaticAnalyzer()
    onchain = OnChainChecker()
    risk = RiskEngine()
    
    # Fetch contract
    contract_data = await fetcher.fetch_contract(address)
    if contract_data.get('error'):
        print(f"Error: {contract_data['error']}")
        return
    
    # Analyze
    static_findings = await static.analyze(contract_data)
    onchain_findings = await onchain.check(address, contract_data)
    
    # Generate report
    report = await risk.generate_report(
        address, contract_data, static_findings, onchain_findings
    )
    
    # Print results
    print(f"Risk Level: {report['risk_level']}")
    print(f"Risk Score: {report['risk_score']}/100")
    print(f"\nCritical Issues: {len(report['critical_findings'])}")
    for finding in report['critical_findings']:
        print(f"  - {finding}")
    
    await fetcher.close()

# Run it
asyncio.run(analyze_contract('0xYourContractAddressHere'))
```

### Batch Analysis

Analyze multiple contracts:

```python
async def batch_analyze(addresses: list):
    results = {}
    
    for addr in addresses:
        print(f"Analyzing {addr}...")
        report = await analyze_contract(addr)
        results[addr] = report['risk_level']
    
    # Sort by risk
    sorted_results = sorted(
        results.items(), 
        key=lambda x: ['safe', 'low', 'medium', 'high', 'critical'].index(x[1]),
        reverse=True
    )
    
    print("\n=== Results Summary ===")
    for addr, risk in sorted_results:
        print(f"{addr}: {risk.upper()}")

addresses = [
    '0x1111111111111111111111111111111111111111',
    '0x2222222222222222222222222222222222222222',
    # ... more addresses
]

asyncio.run(batch_analyze(addresses))
```

### Export to JSON

```python
import json

async def analyze_and_export(address: str, output_file: str):
    report = await analyze_contract(address)
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report exported to {output_file}")

asyncio.run(analyze_and_export(
    '0xYourAddress',
    'security_report.json'
))
```

---

## Integration with Other Tools

### Webhook Alerts

Send critical findings to a webhook:

```python
import aiohttp

async def send_alert(report: dict, webhook_url: str):
    if report['risk_level'] in ['critical', 'high']:
        async with aiohttp.ClientSession() as session:
            await session.post(webhook_url, json={
                'content': f"🚨 High-risk contract detected: {report['address']}",
                'embeds': [{
                    'title': 'Security Alert',
                    'description': report['recommendation'],
                    'color': 0xff0000
                }]
            })
```

### Database Storage

Store analysis results:

```python
import sqlite3
from datetime import datetime

def save_to_db(address: str, report: dict):
    conn = sqlite3.connect('analysis.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS analyses
                 (address TEXT, timestamp TEXT, risk_level TEXT, 
                  risk_score INTEGER, report TEXT)''')
    
    c.execute('INSERT INTO analyses VALUES (?, ?, ?, ?, ?)',
              (address, datetime.now().isoformat(), 
               report['risk_level'], report['risk_score'],
               json.dumps(report)))
    
    conn.commit()
    conn.close()
```

---

## Performance Tuning

### Caching Contract Data

Add caching to avoid re-fetching:

```python
from functools import lru_cache
import json

class ContractFetcher:
    def __init__(self):
        self.cache = {}
    
    async def fetch_contract(self, address: str):
        if address in self.cache:
            print(f"Using cached data for {address}")
            return self.cache[address]
        
        # ... normal fetch logic ...
        
        self.cache[address] = result
        return result
```

### Parallel Analysis

Analyze multiple findings in parallel:

```python
async def analyze(self, contract_data):
    # Run checks in parallel
    results = await asyncio.gather(
        self._check_ownership_risks(source_code),
        self._check_rug_pull_vectors(source_code),
        self._check_honeypot_patterns(source_code),
        # ... more checks
    )
    
    return self.findings
```

---

## Testing

### Unit Tests

Create `tests/test_analyzer.py`:

```python
import pytest
from analyzers.static_analyzer import StaticAnalyzer

@pytest.mark.asyncio
async def test_detects_selfdestruct():
    analyzer = StaticAnalyzer()
    
    malicious_code = '''
    contract Evil {
        function destroy() public {
            selfdestruct(payable(msg.sender));
        }
    }
    '''
    
    findings = await analyzer.analyze({
        'verified': True,
        'source_code': malicious_code
    })
    
    assert any(f['severity'] == 'critical' for f in findings)
    assert any('Self-Destruct' in f['title'] for f in findings)
```

Run tests:
```bash
pip install pytest pytest-asyncio
pytest tests/
```

---

This bot is highly customizable - modify it to fit your specific needs! 🛠️
