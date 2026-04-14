"""Contract data fetcher for Tempo blockchain"""
import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional
from web3 import Web3
import json

from config import (
    TEMPO_RPC_URL,
    TEMPO_EXPLORER_API,
    TEMPO_CHAIN_ID,
    ANALYSIS_TIMEOUT,
    ENABLE_BYTECODE_ANALYSIS
)

logger = logging.getLogger(__name__)

class ContractFetcher:
    """Fetches contract data from Tempo blockchain"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(TEMPO_RPC_URL))
        self.explorer_api = TEMPO_EXPLORER_API
        self.session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def fetch_contract(self, address: str) -> Dict[str, Any]:
        """
        Main entry point: fetch contract data from Tempo
        Tries verified source first, falls back to bytecode analysis
        """
        try:
            async with asyncio.timeout(ANALYSIS_TIMEOUT):
                # Normalize address
                address = Web3.to_checksum_address(address)
                
                # Check if address has code
                code = await self._get_bytecode(address)
                if not code or code == '0x':
                    return {
                        'error': 'No contract code found at this address. It may be an EOA (wallet) or undeployed contract.'
                    }
                
                # Try to fetch verified source code from explorer
                verified_data = await self._fetch_verified_source(address)
                
                if verified_data and not verified_data.get('error'):
                    logger.info(f"Contract {address} is verified, using source code")
                    return {
                        'address': address,
                        'verified': True,
                        'source_code': verified_data['source_code'],
                        'abi': verified_data.get('abi', []),
                        'compiler_version': verified_data.get('compiler_version'),
                        'optimization': verified_data.get('optimization'),
                        'contract_name': verified_data.get('contract_name'),
                        'bytecode': code,
                        'chain_id': TEMPO_CHAIN_ID
                    }
                
                # Fallback: unverified contract - use bytecode analysis
                logger.info(f"Contract {address} is not verified, using bytecode analysis")
                
                if not ENABLE_BYTECODE_ANALYSIS:
                    return {
                        'error': 'Contract is not verified and bytecode analysis is disabled in config.'
                    }
                
                return {
                    'address': address,
                    'verified': False,
                    'source_code': None,
                    'abi': None,
                    'bytecode': code,
                    'chain_id': TEMPO_CHAIN_ID
                }
                
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching contract {address}")
            return {'error': 'Timeout fetching contract data'}
        except Exception as e:
            logger.error(f"Error fetching contract {address}: {e}", exc_info=True)
            return {'error': f'Failed to fetch contract: {str(e)}'}
    
    async def _fetch_verified_source(self, address: str) -> Optional[Dict[str, Any]]:
        """Fetch verified source code from Tempo explorer API"""
        session = await self.get_session()
        
        # Try multiple API endpoints (different explorers may use different formats)
        api_urls = [
            # BlockScout-style API (common for EVM explorers)
            f"{self.explorer_api}?module=contract&action=getsourcecode&address={address}",
            # Etherscan-style API
            f"{self.explorer_api}/api?module=contract&action=getsourcecode&address={address}",
            # Direct endpoint (some explorers)
            f"{self.explorer_api}/contracts/{address}",
        ]
        
        for api_url in api_urls:
            try:
                async with session.get(api_url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Parse different API response formats
                        result = self._parse_explorer_response(data)
                        if result and not result.get('error'):
                            return result
                            
            except Exception as e:
                logger.debug(f"Failed to fetch from {api_url}: {e}")
                continue
        
        return None
    
    def _parse_explorer_response(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse explorer API response (handles multiple formats)"""
        try:
            # BlockScout / Etherscan format
            if isinstance(data, dict) and data.get('status') == '1' and data.get('result'):
                result = data['result']
                if isinstance(result, list):
                    result = result[0]
                
                source_code = result.get('SourceCode', '')
                if not source_code:
                    return None
                
                # Handle JSON-encoded source (multi-file contracts)
                if source_code.startswith('{'):
                    try:
                        source_json = json.loads(source_code)
                        if 'sources' in source_json:
                            # Concatenate all source files
                            source_code = '\n\n'.join([
                                f"// File: {filename}\n{content.get('content', '')}"
                                for filename, content in source_json['sources'].items()
                            ])
                    except:
                        pass
                
                return {
                    'source_code': source_code,
                    'abi': json.loads(result.get('ABI', '[]')) if result.get('ABI') else [],
                    'contract_name': result.get('ContractName'),
                    'compiler_version': result.get('CompilerVersion'),
                    'optimization': result.get('OptimizationUsed') == '1',
                    'runs': result.get('Runs')
                }
            
            # Direct contract object format
            elif isinstance(data, dict) and data.get('source_code'):
                return {
                    'source_code': data['source_code'],
                    'abi': data.get('abi', []),
                    'contract_name': data.get('name'),
                    'compiler_version': data.get('compiler_version'),
                    'optimization': data.get('optimization_enabled', False)
                }
            
        except Exception as e:
            logger.debug(f"Failed to parse explorer response: {e}")
        
        return None
    
    async def _get_bytecode(self, address: str) -> str:
        """Get contract bytecode from RPC"""
        try:
            # Use asyncio to run web3 call in executor (web3.py is sync)
            loop = asyncio.get_event_loop()
            code = await loop.run_in_executor(
                None,
                self.w3.eth.get_code,
                Web3.to_checksum_address(address)
            )
            return code.hex()
        except Exception as e:
            logger.error(f"Failed to get bytecode for {address}: {e}")
            return '0x'
    
    async def close(self):
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
