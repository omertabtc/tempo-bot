# Project Structure

Complete overview of all files and directories in the Tempo Contract Analyzer Bot.

```
tempo-contract-analyzer/
│
├── 📄 bot.py                          # Main entry point - starts the Discord bot
├── 📄 config.py                       # Configuration management (loads .env, sets defaults)
│
├── 📁 cogs/                           # Discord bot command handlers
│   ├── __init__.py
│   └── contract_analysis.py          # /analyze-contract slash command implementation
│
├── 📁 analyzers/                      # Core analysis engines
│   ├── __init__.py
│   ├── contract_fetcher.py           # Fetches contract data from Tempo blockchain
│   ├── static_analyzer.py            # Analyzes Solidity source code for vulnerabilities
│   ├── onchain_checker.py            # Verifies on-chain state (ownership, balance, etc.)
│   └── risk_engine.py                # Calculates risk scores and generates reports
│
├── 📁 utils/                          # Utility modules (currently empty, for future extensions)
│   └── __init__.py
│
├── 📄 requirements.txt                # Python dependencies
├── 📄 .env.example                    # Environment variables template
├── 📄 .env                            # Your actual config (DO NOT COMMIT - in .gitignore)
├── 📄 .gitignore                      # Git ignore rules
│
├── 📄 README.md                       # Main documentation
├── 📄 QUICKSTART.md                   # Fast setup guide for beginners
├── 📄 EXAMPLES.md                     # Usage examples and customization guide
├── 📄 PROJECT_STRUCTURE.md            # This file - project overview
├── 📄 LICENSE                         # MIT License + disclaimer
│
├── 📄 run.sh                          # Quick start script for Linux/Mac
└── 📄 run.bat                         # Quick start script for Windows
```

---

## File Purposes

### Core Files

#### `bot.py`
The main application entry point. This file:
- Creates the Discord bot instance
- Loads the slash command cog
- Syncs commands to Discord
- Handles bot lifecycle (startup, errors, shutdown)

**Key Functions:**
- `TempoAnalyzerBot.__init__()` - Initializes bot with intents
- `setup_hook()` - Loads cogs and syncs commands
- `on_ready()` - Called when bot connects to Discord
- `main()` - Entry point that runs the bot

#### `config.py`
Central configuration management. This file:
- Loads environment variables from `.env`
- Sets default values for all settings
- Validates required configuration (e.g., Discord token)
- Defines risk scoring weights

**Key Variables:**
- `DISCORD_TOKEN` - Your bot's authentication token
- `TEMPO_RPC_URL` - Tempo blockchain RPC endpoint
- `TEMPO_EXPLORER_API` - Explorer API for fetching verified source code
- `RISK_WEIGHTS` - Severity scoring system

---

### Command Handlers (`cogs/`)

#### `cogs/contract_analysis.py`
Implements the `/analyze-contract` slash command. This file:
- Validates user input (contract address format)
- Orchestrates the analysis pipeline
- Sends progress updates to Discord
- Formats results into Discord embeds

**Key Functions:**
- `analyze_contract()` - Main slash command handler
- `send_report()` - Formats and sends analysis results
- `create_embed()` - Helper for creating Discord embeds

---

### Analysis Engines (`analyzers/`)

#### `analyzers/contract_fetcher.py`
Responsible for retrieving contract data. This file:
- Attempts to fetch verified source code from Tempo explorer
- Falls back to bytecode-only analysis for unverified contracts
- Handles multiple explorer API formats (BlockScout, Etherscan-style)
- Parses multi-file contract source code

**Key Functions:**
- `fetch_contract()` - Main entry point, returns contract data dict
- `_fetch_verified_source()` - Tries to get verified source from explorer
- `_get_bytecode()` - Retrieves contract bytecode via RPC
- `_parse_explorer_response()` - Handles different API response formats

**Returns:**
```python
{
    'address': '0x...',
    'verified': True/False,
    'source_code': '...',  # Solidity code (if verified)
    'abi': [...],          # Contract ABI (if verified)
    'bytecode': '0x...',   # Raw bytecode
    'compiler_version': 'v0.8.19',
    'contract_name': 'MyToken'
}
```

#### `analyzers/static_analyzer.py`
The core vulnerability detection engine. This file:
- Parses Solidity source code with regex patterns
- Detects 30+ vulnerability types and rug pull vectors
- Checks for ownership risks, honeypot patterns, minting issues
- Performs bytecode analysis for unverified contracts

**Key Functions:**
- `analyze()` - Main entry point, runs all checks
- `_check_ownership_risks()` - Detects centralization issues
- `_check_rug_pull_vectors()` - Finds drain/sweep functions
- `_check_honeypot_patterns()` - Identifies transfer restrictions
- `_check_minting_risks()` - Validates supply controls
- `_check_approval_risks()` - Checks approval patterns
- `_check_classic_vulnerabilities()` - Reentrancy, overflow, etc.
- `_check_nft_specific()` - NFT metadata and mint security
- `_check_proxy_patterns()` - Upgradeable contract risks
- `_check_dangerous_patterns()` - Assembly, obfuscation, selfdestruct

**Returns:**
```python
[
    {
        'severity': 'critical',  # critical|high|medium|low|info
        'title': 'Owner Can Drain Contract Balance',
        'description': 'Function detected that allows...',
        'code_snippet': '...'  # Optional
    },
    # ... more findings
]
```

#### `analyzers/onchain_checker.py`
Verifies on-chain contract state. This file:
- Calls contract functions via RPC (owner(), paused(), totalSupply(), etc.)
- Checks contract balance
- Validates ownership (EOA vs multisig)
- Verifies supply and max supply

**Key Functions:**
- `check()` - Main entry point
- `_check_ownership()` - Determines owner type
- `_check_balance()` - Gets contract ETH/token balance
- `_check_pause_status()` - Checks if contract is paused
- `_check_supply_info()` - Validates supply vs max supply

**Returns:**
Same format as static_analyzer (list of findings)

#### `analyzers/risk_engine.py`
Combines findings into a final report. This file:
- Calculates overall risk score (0-100)
- Categorizes findings by severity
- Generates human-readable recommendations
- Determines contract type (ERC-20, NFT, DEX, etc.)

**Key Functions:**
- `generate_report()` - Main entry point
- `_calculate_risk_score()` - Weights findings to produce score
- `_get_risk_level()` - Converts score to level (safe/low/medium/high/critical)
- `_generate_recommendation()` - Creates actionable advice

**Returns:**
```python
{
    'address': '0x...',
    'contract_type': '💰 ERC-20 Token',
    'verified': '✅ Yes',
    'compiler': 'v0.8.19',
    'risk_score': 75,
    'risk_level': 'high',
    'risk_emoji': '🔴',
    'total_issues': 8,
    'critical_findings': [...],
    'high_findings': [...],
    'medium_findings': [...],
    'low_findings': [...],
    'recommendation': '🚨 HIGH RISK...'
}
```

---

## Configuration Files

### `.env` (You create this)
Your private configuration. **Never commit this file!**

```env
DISCORD_TOKEN=your_bot_token_here
TEMPO_RPC_URL=https://rpc.tempo.xyz
TEMPO_EXPLORER_API=https://contracts.tempo.xyz/api
TEMPO_CHAIN_ID=42431
```

### `.env.example`
Template for `.env`. Safe to commit. Copy this to `.env` and fill in your values.

### `requirements.txt`
Python package dependencies. Install with:
```bash
pip install -r requirements.txt
```

### `.gitignore`
Prevents committing sensitive files:
- `.env` (your secrets)
- `__pycache__/` (Python cache)
- `*.log` (log files)
- `venv/` (virtual environment)

---

## Documentation Files

### `README.md`
Main documentation with:
- Feature overview
- Installation instructions
- Technical architecture
- Security features list
- Disclaimer

### `QUICKSTART.md`
Step-by-step setup guide for beginners:
1. Get Discord bot token
2. Install dependencies
3. Configure `.env`
4. Run the bot
5. Test in Discord

### `EXAMPLES.md`
Advanced usage:
- Example analysis outputs
- Customizing detection rules
- Programmatic usage
- Batch analysis
- Integration with webhooks/databases
- Performance tuning

### `PROJECT_STRUCTURE.md`
This file! Explains every file and directory.

### `LICENSE`
MIT License with disclaimer about automated analysis limitations.

---

## Helper Scripts

### `run.sh` (Linux/Mac)
One-command startup:
```bash
chmod +x run.sh
./run.sh
```

Does:
1. Checks for `.env`
2. Creates virtual environment if needed
3. Installs dependencies
4. Runs the bot

### `run.bat` (Windows)
Windows equivalent of `run.sh`. Double-click to run.

---

## Data Flow

```
Discord User
    ↓
/analyze-contract 0x123...
    ↓
cogs/contract_analysis.py
    ↓
┌─────────────────────────────────────┐
│ analyzers/contract_fetcher.py       │
│ ├─ Try explorer API for source      │
│ └─ Fallback to bytecode via RPC     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ analyzers/static_analyzer.py        │
│ ├─ Parse Solidity source            │
│ ├─ Detect vulnerability patterns    │
│ └─ Return findings list              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ analyzers/onchain_checker.py        │
│ ├─ Call contract functions (RPC)    │
│ ├─ Verify ownership, balance, etc.  │
│ └─ Return findings list              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ analyzers/risk_engine.py             │
│ ├─ Combine all findings             │
│ ├─ Calculate risk score             │
│ ├─ Generate recommendation          │
│ └─ Return formatted report           │
└─────────────────────────────────────┘
    ↓
cogs/contract_analysis.py
    ↓
Format as Discord embeds
    ↓
Discord User receives report
```

---

## Extending the Bot

Want to add features? Here's where to start:

### Add a new vulnerability check
→ Edit `analyzers/static_analyzer.py`
→ Add `_check_my_feature()` method
→ Call it in `analyze()`

### Add a new Discord command
→ Create new function in `cogs/contract_analysis.py`
→ Decorate with `@app_commands.command()`

### Change risk scoring
→ Edit `RISK_WEIGHTS` in `config.py`
→ Or modify `_calculate_risk_score()` in `risk_engine.py`

### Add another blockchain
→ Update `config.py` with new chain settings
→ Modify `contract_fetcher.py` to handle chain-specific explorers

### Store analysis results
→ Add database module to `utils/`
→ Import and call in `cogs/contract_analysis.py` after analysis

---

## Testing

Run the analyzer standalone (without Discord):

```python
# test.py
import asyncio
from analyzers.contract_fetcher import ContractFetcher
from analyzers.static_analyzer import StaticAnalyzer

async def test():
    fetcher = ContractFetcher()
    analyzer = StaticAnalyzer()
    
    data = await fetcher.fetch_contract('0xYourAddress')
    findings = await analyzer.analyze(data)
    
    for f in findings:
        print(f"{f['severity'].upper()}: {f['title']}")
    
    await fetcher.close()

asyncio.run(test())
```

---

## Questions?

- **Bot won't start?** → Check `QUICKSTART.md`
- **Want examples?** → See `EXAMPLES.md`
- **Need to customize?** → See `EXAMPLES.md` customization section
- **Architecture questions?** → See `README.md` Technical Architecture section

Happy hacking! 🚀
