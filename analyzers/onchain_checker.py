"""On-chain state verification for smart contracts"""
import asyncio
import logging
from typing import Dict, List, Any
from web3 import Web3
from eth_abi import decode

from config import TEMPO_RPC_URL

logger = logging.getLogger(__name__)

class OnChainChecker:
    """Performs on-chain state verification"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(TEMPO_RPC_URL))
    
    async def check(self, address: str, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Main on-chain checking entry point"""
        findings = []
        
        try:
            address = Web3.to_checksum_address(address)
            
            # Basic checks
            findings.extend(await self._check_ownership(address, contract_data))
            findings.extend(await self._check_balance(address))
            findings.extend(await self._check_pause_status(address, contract_data))
            findings.extend(await self._check_supply_info(address, contract_data))
            
        except Exception as e:
            logger.error(f"Error in on-chain checks: {e}", exc_info=True)
            findings.append({
                'severity': 'info',
                'title': 'On-Chain Check Incomplete',
                'description': f'Some on-chain checks failed: {str(e)}'
            })
        
        return findings
    
    async def _check_ownership(self, address: str, contract_data: Dict[str, Any]) -> List[Dict]:
        """Check contract ownership status"""
        findings = []
        
        try:
            # Try to call owner() function
            owner = await self._call_function(address, 'owner()', [])
            
            if owner and owner != '0x0000000000000000000000000000000000000000':
                # Check if it's an EOA or contract
                owner_code = await self._get_code(owner)
                
                if owner_code == '0x':
                    findings.append({
                        'severity': 'medium',
                        'title': 'Owner is EOA (Single Wallet)',
                        'description': f'Contract owner is {owner} (single wallet, not multisig).'
                    })
                else:
                    # Owner is a contract - check if it's a known multisig/timelock
                    findings.append({
                        'severity': 'low',
                        'title': 'Owner is Smart Contract',
                        'description': f'Owner is contract at {owner}. Could be multisig or timelock (verify manually).'
                    })
            elif owner == '0x0000000000000000000000000000000000000000':
                findings.append({
                    'severity': 'info',
                    'title': 'Ownership Renounced',
                    'description': 'Contract ownership has been renounced (owner is 0x0).'
                })
                
        except Exception as e:
            logger.debug(f"Could not check owner(): {e}")
        
        return findings
    
    async def _check_balance(self, address: str) -> List[Dict]:
        """Check contract balance"""
        findings = []
        
        try:
            loop = asyncio.get_event_loop()
            balance = await loop.run_in_executor(
                None,
                self.w3.eth.get_balance,
                address
            )
            
            balance_eth = self.w3.from_wei(balance, 'ether')
            
            if balance_eth > 0:
                findings.append({
                    'severity': 'info',
                    'title': f'Contract Holds {balance_eth:.4f} Native Tokens',
                    'description': f'Contract balance: {balance_eth:.4f} tokens. Verify if withdrawable by owner.'
                })
                
        except Exception as e:
            logger.debug(f"Could not check balance: {e}")
        
        return findings
    
    async def _check_pause_status(self, address: str, contract_data: Dict[str, Any]) -> List[Dict]:
        """Check if contract is paused"""
        findings = []
        
        try:
            # Try to call paused() function
            paused = await self._call_function(address, 'paused()', [])
            
            if paused is not None:
                if paused:
                    findings.append({
                        'severity': 'high',
                        'title': '⚠️ Contract is Currently PAUSED',
                        'description': 'Contract is paused. Transfers and other functions are disabled.'
                    })
                else:
                    findings.append({
                        'severity': 'info',
                        'title': 'Contract Not Paused',
                        'description': 'Contract is active (not paused).'
                    })
                    
        except Exception as e:
            logger.debug(f"Could not check paused status: {e}")
        
        return findings
    
    async def _check_supply_info(self, address: str, contract_data: Dict[str, Any]) -> List[Dict]:
        """Check total supply and max supply info"""
        findings = []
        
        try:
            # Try totalSupply()
            total_supply = await self._call_function(address, 'totalSupply()', [])
            
            if total_supply is not None:
                # Try maxSupply() or MAX_SUPPLY()
                max_supply = await self._call_function(address, 'maxSupply()', [])
                if max_supply is None:
                    max_supply = await self._call_function(address, 'MAX_SUPPLY()', [])
                
                if max_supply is not None and max_supply > 0:
                    percent_minted = (total_supply / max_supply) * 100
                    
                    findings.append({
                        'severity': 'info',
                        'title': f'Supply: {total_supply:,} / {max_supply:,} ({percent_minted:.1f}%)',
                        'description': f'Total minted: {total_supply:,} out of max {max_supply:,} ({percent_minted:.1f}%)'
                    })
                    
                    if percent_minted >= 100:
                        findings.append({
                            'severity': 'info',
                            'title': 'Max Supply Reached',
                            'description': 'All tokens/NFTs have been minted.'
                        })
                else:
                    findings.append({
                        'severity': 'medium',
                        'title': f'Current Supply: {total_supply:,} (No Max Supply Found)',
                        'description': 'Total supply exists but no max supply detected on-chain. May be unlimited.'
                    })
                    
        except Exception as e:
            logger.debug(f"Could not check supply info: {e}")
        
        return findings
    
    async def _call_function(self, address: str, signature: str, params: list) -> Any:
        """Call a contract function and return decoded result"""
        try:
            # Encode function call
            selector = self.w3.keccak(text=signature)[:4].hex()
            data = selector
            
            # Make call
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.w3.eth.call({
                    'to': address,
                    'data': data
                })
            )
            
            if not result or result == b'':
                return None
            
            # Decode result based on function signature
            if signature == 'owner()' or signature.startswith('owner'):
                # Returns address
                return self.w3.to_checksum_address('0x' + result.hex()[-40:])
            elif signature == 'paused()':
                # Returns bool
                return bool(int(result.hex(), 16))
            elif 'Supply' in signature or 'supply' in signature:
                # Returns uint256
                return int(result.hex(), 16)
            else:
                # Default: try to decode as uint256
                try:
                    return int(result.hex(), 16)
                except:
                    return result.hex()
                    
        except Exception as e:
            logger.debug(f"Failed to call {signature}: {e}")
            return None
    
    async def _get_code(self, address: str) -> str:
        """Get bytecode at address"""
        try:
            loop = asyncio.get_event_loop()
            code = await loop.run_in_executor(
                None,
                self.w3.eth.get_code,
                Web3.to_checksum_address(address)
            )
            return code.hex()
        except:
            return '0x'
