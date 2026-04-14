# Tempo Smart Contract Security Analyzer Bot

A professional Discord bot that performs comprehensive security analysis of smart contracts on the Tempo blockchain (EVM-compatible L1 for stablecoin payments).

---

## 🚀 Quick Start

**New here?** → Read **[START_HERE.md](START_HERE.md)** for instant setup!

**Your Application ID:** `2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e`

---

## Features

- ✅ Analyzes ALL contract types (ERC-20, ERC-721, ERC-1155, presale, DEX, proxies)
- ✅ Fetches verified source code from Tempo explorer
- ✅ On-chain bytecode analysis for unverified contracts
- ✅ Detects 30+ vulnerability patterns and rug pull vectors
- ✅ Ownership & centralization risk assessment
- ✅ Honeypot & transfer restriction detection
- ✅ Minting & supply manipulation checks
- ✅ Reentrancy & classic vulnerability scanning
- ✅ NFT-specific metadata & mint security analysis
- ✅ **User rate limiting** (3 analyses per 60 seconds to prevent abuse)
- ✅ **Professional embed reports** with color-coded risk levels

## Installation

### Prerequisites

- Python 3.9+
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- Tempo RPC endpoint (public or private)

### Setup

1. Clone/download this directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Edit `.env` and add your credentials:
```env
DISCORD_TOKEN=your_bot_token_here
TEMPO_RPC_URL=https://rpc.tempo.xyz
TEMPO_EXPLORER_API=https://contracts.tempo.xyz/api
TEMPO_CHAIN_ID=42431
```

5. Run the bot:
```bash
python bot.py
```

## Usage

### Discord Commands

#### `/analyze-contract <contract_address>`

Analyzes a Tempo blockchain smart contract for security risks.

**Parameters:**
- `contract_address` (required): The contract address (0x...)

**Example:**
```
/analyze-contract 0x1234567890abcdef1234567890abcdef12345678
```

**Response:**
The bot will provide a detailed security report including:
- Contract type and verification status
- Risk summary with color-coded severity:
  - 🟢 **GREEN (SAFE)**: No major risks detected
  - 🟡 **YELLOW (WARNING)**: Moderate risks present
  - 🔴 **RED (HIGH RISK)**: Potential for asset/fund loss!
- Key findings in plain English with explanations
- Specific recommendations (Do not interact, Exercise caution, or Proceed carefully)
- Powered by AI static analysis + on-chain verification

**Rate Limiting:**
To prevent abuse, each user is limited to **3 analyses per 60 seconds**. If you exceed this limit, you'll see a friendly message telling you when you can try again.

## Technical Architecture

### Analysis Pipeline

1. **Contract Fetching** (`contract_fetcher.py`)
   - Attempts to fetch verified source code from Tempo explorer API
   - Falls back to bytecode analysis via RPC for unverified contracts
   - Retrieves ABI, compiler version, optimization settings

2. **Static Analysis** (`analyzer.py`)
   - Parses Solidity source code for dangerous patterns
   - Detects privileged functions and modifiers
   - Identifies transfer restrictions and honeypot code
   - Analyzes minting mechanics and supply controls

3. **On-Chain Analysis** (`onchain_checker.py`)
   - Queries current contract state via RPC
   - Checks ownership, paused status, balances
   - Simulates common user interactions
   - Validates supply and liquidity data

4. **Risk Scoring** (`risk_engine.py`)
   - Weights findings by severity
   - Generates overall risk score
   - Provides actionable recommendations

### Files

- `bot.py` - Main Discord bot entry point
- `cogs/contract_analysis.py` - Slash command handler
- `analyzers/contract_fetcher.py` - Fetches contract data from Tempo
- `analyzers/static_analyzer.py` - Static code analysis engine
- `analyzers/onchain_checker.py` - On-chain state verification
- `analyzers/risk_engine.py` - Risk scoring and reporting
- `utils/solidity_parser.py` - Solidity source code parser
- `utils/web3_helper.py` - Web3 RPC interaction utilities
- `config.py` - Configuration management

## Security Features Detected

### Ownership & Centralization
- ✅ Owner/admin privilege detection
- ✅ Multisig and timelock checks
- ✅ Renounce ownership status
- ✅ Proxy upgrade mechanisms

### Rug Pull Vectors
- ✅ Owner withdrawal functions
- ✅ Hidden drain mechanisms
- ✅ Liquidity lock verification
- ✅ Team allocation vesting

### Honeypot Detection
- ✅ Transfer restriction analysis
- ✅ Blacklist/whitelist mechanisms
- ✅ Buy/sell tax asymmetry
- ✅ Hidden fee structures

### Minting Risks
- ✅ Unlimited mint detection
- ✅ Hidden mint in hooks
- ✅ Max supply enforcement
- ✅ Mint price manipulation

### Classic Vulnerabilities
- ✅ Reentrancy guards
- ✅ Integer overflow/underflow (Solidity <0.8)
- ✅ Dangerous delegatecall
- ✅ Unchecked external calls
- ✅ Self-destruct mechanisms

### NFT-Specific
- ✅ Metadata mutability
- ✅ Reveal mechanisms
- ✅ Royalty enforcement
- ✅ Max supply validation

## Contributing

Pull requests welcome! Please ensure all code follows PEP 8 and includes tests.

## Disclaimer

This bot provides automated analysis and is NOT a substitute for professional security audits. Always DYOR before interacting with smart contracts.

## License

MIT License - see LICENSE file
