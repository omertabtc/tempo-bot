"""Configuration management for Tempo Contract Analyzer Bot"""
import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')

# Tempo Blockchain Configuration
TEMPO_RPC_URL = os.getenv('TEMPO_RPC_URL', 'https://rpc.tempo.xyz')
TEMPO_EXPLORER_API = os.getenv('TEMPO_EXPLORER_API', 'https://contracts.tempo.xyz/api')
TEMPO_CHAIN_ID = int(os.getenv('TEMPO_CHAIN_ID', '42431'))

# Analysis Settings
MAX_CONTRACT_SIZE = int(os.getenv('MAX_CONTRACT_SIZE', '50000'))
ANALYSIS_TIMEOUT = int(os.getenv('ANALYSIS_TIMEOUT', '60'))
ENABLE_BYTECODE_ANALYSIS = os.getenv('ENABLE_BYTECODE_ANALYSIS', 'true').lower() == 'true'

# Rate Limiting
RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds
RATE_LIMIT_MAX = int(os.getenv('RATE_LIMIT_MAX', '3'))  # max analyses per window

# Risk Scoring Weights
RISK_WEIGHTS = {
    'critical': 100,
    'high': 50,
    'medium': 20,
    'low': 5,
    'info': 1
}

# Validation
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN must be set in .env file")
