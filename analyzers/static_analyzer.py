"""Static code analysis for smart contracts"""
import re
import logging
from typing import Dict, List, Any
from .smart_patterns import SmartPatterns

logger = logging.getLogger(__name__)

class StaticAnalyzer:
    """Performs static analysis on Solidity source code"""
    
    def __init__(self):
        self.findings = []
        self.contract_purpose = 'UNKNOWN'
        self.is_openzeppelin = False
        self.confidence_score = 0.5
    
    async def analyze(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Main analysis entry point"""
        self.findings = []
        
        if not contract_data.get('verified') or not contract_data.get('source_code'):
            # Bytecode-only analysis
            return await self._analyze_bytecode(contract_data)
        
        source_code = contract_data['source_code']
        
        # STEP 1: Detect contract context (reduces false positives)
        self.contract_purpose = SmartPatterns.detect_contract_purpose(source_code)
        self.is_openzeppelin = SmartPatterns.is_openzeppelin_based(source_code)
        self.confidence_score = SmartPatterns.calculate_confidence_score(source_code)
        
        logger.info(f"Contract purpose detected: {self.contract_purpose}")
        logger.info(f"OpenZeppelin-based: {self.is_openzeppelin}")
        logger.info(f"Confidence score: {self.confidence_score:.2f}")
        
        # Add info finding about contract quality
        if self.is_openzeppelin:
            self._add_finding('info', 'Uses OpenZeppelin Contracts',
                            'Contract imports OpenZeppelin standard contracts, which are well-audited and battle-tested.')
        
        # STEP 2: Run context-aware analysis checks
        await self._check_ownership_risks(source_code)
        await self._check_rug_pull_vectors(source_code)
        await self._check_honeypot_patterns(source_code)
        await self._check_minting_risks(source_code)
        await self._check_approval_risks(source_code)
        await self._check_classic_vulnerabilities(source_code)
        await self._check_nft_specific(source_code)
        await self._check_proxy_patterns(source_code)
        await self._check_dangerous_patterns(source_code)
        
        return self.findings
    
    def _add_finding(self, severity: str, title: str, description: str, code_snippet: str = None):
        """Add a finding to the results"""
        self.findings.append({
            'severity': severity,  # critical, high, medium, low, info
            'title': title,
            'description': description,
            'code_snippet': code_snippet
        })
    
    async def _check_ownership_risks(self, source: str):
        """Check for ownership and centralization risks"""
        
        # Check if using safe OpenZeppelin ownership
        has_safe_ownership = SmartPatterns.has_safe_ownership(source)
        
        # Check for Ownable pattern
        if re.search(r'contract\s+\w+\s+is\s+.*Ownable', source, re.IGNORECASE):
            # Check if ownership can be renounced (informational for OpenZeppelin)
            if 'renounceOwnership' in source:
                if has_safe_ownership:
                    self._add_finding('info', 'Standard Ownership Pattern', 
                                     'Contract uses standard OpenZeppelin Ownable with renounceOwnership. This is normal.')
                else:
                    self._add_finding('low', 'Ownership Can Be Renounced', 
                                     'Contract has renounceOwnership function. If called, critical functions may become permanently disabled.')
            
            # Check for owner-only critical functions
            owner_funcs = re.findall(r'function\s+(\w+).*onlyOwner', source, re.DOTALL)
            if owner_funcs:
                dangerous_keywords = ['withdraw', 'drain', 'sweep', 'emergency', 'rescue', 'recover']
                dangerous_funcs = [f for f in owner_funcs if any(k in f.lower() for k in dangerous_keywords)]
                
                if dangerous_funcs:
                    # Lower severity if it's OpenZeppelin-based and NFT collection
                    if self.is_openzeppelin and self.contract_purpose in ['NFT_COLLECTION', 'NFT_COLLECTION_WITH_MINT']:
                        self._add_finding('medium', 'Owner Withdrawal Functions', 
                                         f'Owner can withdraw funds via: {", ".join(dangerous_funcs[:5])}. Common in NFT projects for collecting mint proceeds.')
                    else:
                        self._add_finding('high', 'Owner Can Withdraw Funds', 
                                         f'Owner-only functions detected that can withdraw funds: {", ".join(dangerous_funcs[:5])}')
        
        # Check for unlimited minting by owner
        if re.search(r'function\s+(\w*mint\w*)\s*\([^)]*\)\s+.*onlyOwner', source, re.IGNORECASE):
            # Check if there's max supply protection
            has_max_supply = re.search(r'require\s*\([^)]*totalSupply.*maxSupply|require\s*\([^)]*totalSupply.*<=.*MAX_SUPPLY', source, re.IGNORECASE)
            
            if not has_max_supply:
                # For NFT collections, this is higher risk
                if self.contract_purpose in ['NFT_COLLECTION', 'NFT_COLLECTION_WITH_MINT']:
                    self._add_finding('medium', 'Owner Minting Without Visible Max Supply', 
                                     'Owner can mint tokens/NFTs. Max supply check not found in code (may be in parent contract).')
                else:
                    self._add_finding('high', 'Unlimited Owner Minting', 
                                     'Owner can mint unlimited tokens/NFTs with no max supply enforcement detected.')
        
        # Check for pause functionality (informational for OpenZeppelin)
        if 'Pausable' in source or re.search(r'whenNotPaused|_pause\(\)', source):
            if self.is_openzeppelin:
                self._add_finding('info', 'Pausable Contract (Standard)', 
                                 'Contract uses OpenZeppelin Pausable. Owner can pause in emergencies (standard security feature).')
            else:
                self._add_finding('medium', 'Pausable Contract', 
                                 'Contract can be paused by privileged roles, preventing transfers and other operations.')
        
        # Check for AccessControl roles (informational for OpenZeppelin)
        if 'AccessControl' in source or 'ADMIN_ROLE' in source or 'MINTER_ROLE' in source:
            if self.is_openzeppelin:
                self._add_finding('info', 'Role-Based Access Control (Standard)', 
                                 'Uses OpenZeppelin AccessControl for role management. Verify role holders on-chain.')
            else:
                self._add_finding('medium', 'Role-Based Access Control', 
                                 'Contract uses role-based permissions. Verify who holds critical roles (ADMIN, MINTER, etc.).')
        
        # Check for multisig or timelock (only warn if not OpenZeppelin)
        has_multisig = 'Multisig' in source or 'multisig' in source.lower()
        has_timelock = 'Timelock' in source or 'timelock' in source.lower()
        
        if not has_multisig and not has_timelock:
            if 'onlyOwner' in source and not self.is_openzeppelin:
                self._add_finding('medium', 'No Timelock or Multisig Detected', 
                                 'Owner can execute privileged functions immediately without delay or consensus.')
    
    async def _check_rug_pull_vectors(self, source: str):
        """Check for common rug pull mechanisms"""
        
        # Check for direct ETH/token withdrawal functions
        withdraw_patterns = [
            r'function\s+withdraw\w*\s*\([^)]*\)\s+.*\{[^}]*payable\(owner\)\.transfer',
            r'function\s+withdraw\w*\s*\([^)]*\)\s+.*\{[^}]*payable\(owner\)\.send',
            r'function\s+withdraw\w*\s*\([^)]*\)\s+.*\{[^}]*\.call\{value:',
            r'\.transfer\(address\(this\)\.balance\)',
            r'\.call\{value:\s*address\(this\)\.balance\}'
        ]
        
        for pattern in withdraw_patterns:
            if re.search(pattern, source, re.DOTALL | re.IGNORECASE):
                self._add_finding('critical', 'Owner Can Drain Contract Balance', 
                                 'Function detected that allows owner to withdraw entire contract balance.')
                break
        
        # Check for token sweep functions
        if re.search(r'function\s+(\w*sweep\w*|\w*rescue\w*|\w*recover\w*)', source, re.IGNORECASE):
            self._add_finding('high', 'Token Sweep Function Detected', 
                             'Function exists that can transfer out tokens held by contract. May be used to drain liquidity.')
        
        # Check for liquidity removal
        if re.search(r'removeLiquidity|burnLiquidity', source, re.IGNORECASE):
            if not re.search(r'require.*locked|timelock', source, re.IGNORECASE):
                self._add_finding('critical', 'Liquidity Can Be Removed Without Lock', 
                                 'Contract can remove liquidity without timelock protection. High rug pull risk.')
        
        # Check for hidden backdoors
        if re.search(r'assembly\s*\{[^}]*delegatecall', source, re.DOTALL):
            self._add_finding('critical', 'Dangerous Delegatecall in Assembly', 
                             'Low-level delegatecall detected. Can be used to execute arbitrary code.')
        
        # Check for selfdestruct
        if 'selfdestruct' in source or 'suicide' in source:
            self._add_finding('critical', 'Self-Destruct Capability', 
                             'Contract can be destroyed, permanently locking all funds.')
    
    async def _check_honeypot_patterns(self, source: str):
        """Check for honeypot and transfer restriction patterns"""
        
        # Check for transfer restrictions
        transfer_checks = re.findall(r'function\s+(_transfer|transfer|_beforeTokenTransfer)\s*\([^)]*\)[^{]*\{([^}]+)\}', 
                                     source, re.DOTALL)
        
        for func_name, func_body in transfer_checks:
            # Check for blacklist
            if re.search(r'blacklist|isBlacklisted|_isBlocked', func_body, re.IGNORECASE):
                self._add_finding('high', 'Blacklist Mechanism Detected', 
                                 'Contract can blacklist addresses, preventing them from transferring tokens.')
            
            # Check for whitelist-only transfers
            if re.search(r'require.*whitelist|require.*isWhitelisted', func_body, re.IGNORECASE):
                self._add_finding('high', 'Whitelist-Only Transfers', 
                                 'Only whitelisted addresses can transfer. You may be unable to sell.')
            
            # Check for trading enabled flag
            if re.search(r'require.*tradingEnabled|require.*isTradingEnabled', func_body, re.IGNORECASE):
                self._add_finding('medium', 'Trading Can Be Disabled', 
                                 'Owner can disable trading at any time, freezing all transfers.')
            
            # Check for cooldown mechanisms
            if re.search(r'cooldown|lastTransfer|_lastTransactionBlock', func_body, re.IGNORECASE):
                self._add_finding('low', 'Transfer Cooldown Detected', 
                                 'Transfers may be rate-limited by cooldown period.')
        
        # Check for asymmetric buy/sell taxes
        buy_tax = re.search(r'buyTax|buyFee|_buyFee', source)
        sell_tax = re.search(r'sellTax|sellFee|_sellFee', source)
        
        if buy_tax and sell_tax:
            # Look for setters that can change fees
            if re.search(r'function\s+set\w*Tax|function\s+set\w*Fee', source, re.IGNORECASE):
                self._add_finding('high', 'Modifiable Buy/Sell Taxes', 
                                 'Owner can change buy/sell taxes at any time. Risk of sudden 100% sell tax (honeypot).')
        
        # Check for max transaction limits
        if re.search(r'maxTransaction|_maxTxAmount|maxWallet', source, re.IGNORECASE):
            self._add_finding('low', 'Max Transaction/Wallet Limits', 
                             'Transaction or wallet holding limits detected. May prevent large sells.')
    
    async def _check_minting_risks(self, source: str):
        """Check for minting and supply manipulation risks"""
        
        # Check if this contract has safe mint patterns
        has_safe_mint = SmartPatterns.has_safe_mint_pattern(source)
        
        # Check for mint functions
        mint_funcs = re.findall(r'function\s+(\w*mint\w*)\s*\([^)]*\)([^{]*)\{', source, re.IGNORECASE | re.DOTALL)
        
        if mint_funcs:
            for func_name, modifiers in mint_funcs:
                # Check if public/external mint with no access control
                if 'public' in modifiers or 'external' in modifiers:
                    if not any(mod in modifiers for mod in ['onlyOwner', 'onlyMinter', 'onlyRole']):
                        # Check if it's payable (normal for NFT public mint)
                        if 'payable' in modifiers and has_safe_mint:
                            self._add_finding('info', 'Public Paid Mint Function', 
                                             f'Function {func_name} allows public minting with payment. Standard for NFT drops.')
                        else:
                            self._add_finding('critical', 'Public Minting Without Access Control', 
                                             f'Function {func_name} allows anyone to mint tokens/NFTs for free.')
                
                # Check if there's a max supply check
                # Look in the function body
                mint_func_match = re.search(
                    rf'function\s+{re.escape(func_name)}\s*\([^)]*\)[^{{]*\{{([^}}]+)\}}', 
                    source, re.DOTALL | re.IGNORECASE
                )
                if mint_func_match:
                    func_body = mint_func_match.group(1)
                    has_max_supply = re.search(r'require.*maxSupply|require.*MAX_SUPPLY|totalSupply.*<=.*max', 
                                              func_body, re.IGNORECASE)
                    if not has_max_supply:
                        # For NFT collections with OpenZeppelin, max supply might be in parent
                        if self.is_openzeppelin and self.contract_purpose in ['NFT_COLLECTION', 'NFT_COLLECTION_WITH_MINT']:
                            self._add_finding('low', f'Max Supply Check Not Visible in {func_name}', 
                                             'Max supply enforcement not found in this function (may be in parent contract or state variable).')
                        else:
                            self._add_finding('high', f'No Max Supply Check in {func_name}', 
                                             'Minting function lacks max supply enforcement. Unlimited inflation possible.')
        
        # Check for hidden mint in _transfer
        transfer_body_match = re.search(r'function\s+(_transfer|transfer)\s*\([^)]*\)\s*[^{]*\{([^}]{200,})\}', 
                                       source, re.DOTALL)
        if transfer_body_match:
            transfer_body = transfer_body_match.group(2)
            if re.search(r'_mint\(|\.mint\(|_balances\[.*\]\s*\+=', transfer_body):
                self._add_finding('critical', 'Hidden Mint in Transfer Function', 
                                 'Tokens/NFTs are minted inside transfer function. Highly suspicious pattern.')
        
        # Check for NFT max supply (if looks like NFT contract)
        if 'ERC721' in source or 'ERC1155' in source:
            has_max_supply_var = re.search(r'(uint256|uint)\s+(public\s+)?(constant\s+)?MAX_SUPPLY', source)
            if not has_max_supply_var:
                self._add_finding('medium', 'NFT Contract Without Max Supply', 
                                 'No MAX_SUPPLY constant found. Collection size may be unlimited or changed.')
    
    async def _check_approval_risks(self, source: str):
        """Check for approval and allowance manipulation risks"""
        
        # SMART CHECK: Don't flag normal approval patterns for NFTs/tokens
        is_dangerous = SmartPatterns.is_approval_dangerous(source, self.contract_purpose)
        
        if not is_dangerous:
            # For NFT collections and tokens, approval is NORMAL and EXPECTED
            if self.contract_purpose in ['NFT_COLLECTION', 'NFT_COLLECTION_WITH_MINT', 'TOKEN']:
                # Skip approval warnings - this is standard functionality
                return
        
        # Check for functions that transfer approved tokens (only flag if suspicious)
        if re.search(r'transferFrom\s*\(\s*msg\.sender', source):
            # Only flag if NOT a standard ERC implementation
            if not SmartPatterns.is_standard_erc(source, 'ERC721') and not SmartPatterns.is_standard_erc(source, 'ERC20'):
                self._add_finding('medium', 'Non-Standard TransferFrom Pattern', 
                                 'Contract transfers tokens from msg.sender in unusual way. Verify this is intentional.')
        
        # Check for infinite approval encouragement (informational only for standard contracts)
        if re.search(r'type\(uint256\)\.max|2\*\*256\s*-\s*1|115792089237316', source):
            if not self.is_openzeppelin:
                self._add_finding('low', 'Infinite Approval Pattern Detected', 
                                 'Code references max uint256, possibly for infinite approvals. Best practice is limited approvals.')
        
        # Check for approval reset requirements
        if re.search(r'require.*allowance.*==\s*0', source):
            self._add_finding('info', 'Approval Reset Required', 
                             'Contract requires allowance to be 0 before changing approval (USDT-style).')
    
    async def _check_classic_vulnerabilities(self, source: str):
        """Check for classic smart contract vulnerabilities"""
        
        # Check Solidity version
        version_match = re.search(r'pragma\s+solidity\s+[\^]?([0-9.]+)', source)
        if version_match:
            version = version_match.group(1)
            if version.startswith('0.4') or version.startswith('0.5') or version.startswith('0.6') or version.startswith('0.7'):
                self._add_finding('high', 'Outdated Solidity Version', 
                                 f'Using Solidity {version}. Versions before 0.8.0 lack automatic overflow checks.')
        
        # Check for missing reentrancy guards
        has_reentrancy_guard = 'ReentrancyGuard' in source or 'nonReentrant' in source or '_reentrancyGuard' in source
        has_external_calls = re.search(r'\.call\{|\.transfer\(|\.send\(|\.delegatecall', source)
        
        if has_external_calls and not has_reentrancy_guard:
            self._add_finding('high', 'Missing Reentrancy Protection', 
                             'Contract makes external calls but lacks reentrancy guards.')
        
        # Check for unchecked external calls
        unchecked_calls = re.findall(r'\.call\{[^}]*\}[^;]*;(?!\s*require)', source, re.DOTALL)
        if unchecked_calls:
            self._add_finding('medium', 'Unchecked External Calls', 
                             f'Found {len(unchecked_calls)} external calls without return value checks.')
        
        # Check for dangerous delegatecall
        if 'delegatecall' in source:
            self._add_finding('high', 'Delegatecall Usage Detected', 
                             'Delegatecall can execute arbitrary code in contract context. Ensure target is trusted.')
        
        # Check for tx.origin usage (authentication bypass risk)
        if 'tx.origin' in source:
            self._add_finding('medium', 'tx.origin Used for Authentication', 
                             'Using tx.origin instead of msg.sender can be exploited in phishing attacks.')
    
    async def _check_nft_specific(self, source: str):
        """NFT-specific security checks"""
        
        is_nft = 'ERC721' in source or 'ERC1155' in source
        if not is_nft:
            return
        
        # Check if baseURI can be changed
        if re.search(r'function\s+setBaseURI|function\s+set\w*URI', source, re.IGNORECASE):
            if re.search(r'onlyOwner', source):
                self._add_finding('medium', 'Metadata Can Be Changed by Owner', 
                                 'Owner can modify baseURI, potentially changing all NFT metadata.')
        
        # Check for reveal mechanism
        if re.search(r'revealed|isRevealed|_revealed', source, re.IGNORECASE):
            self._add_finding('info', 'Reveal Mechanism Detected', 
                             'NFTs use a reveal mechanism. Metadata hidden until reveal.')
        
        # Check for royalty enforcement
        if 'ERC2981' in source or 'royaltyInfo' in source:
            self._add_finding('info', 'Royalty Standard Implemented (ERC2981)', 
                             'Contract implements ERC2981 royalty standard.')
        
        # Check for mint price manipulation
        mint_price_setters = re.findall(r'function\s+set\w*Price', source, re.IGNORECASE)
        if mint_price_setters:
            self._add_finding('medium', 'Mint Price Can Be Changed', 
                             f'Owner can modify mint price. Found setters: {", ".join(mint_price_setters[:3])}')
    
    async def _check_proxy_patterns(self, source: str):
        """Check for proxy and upgrade patterns"""
        
        # Check for upgradeable proxies
        is_upgradeable = any(pattern in source for pattern in [
            'Upgradeable',
            'UUPSUpgradeable',
            'TransparentUpgradeableProxy',
            '_upgradeToAndCall',
            '_upgradeTo'
        ])
        
        if is_upgradeable:
            # Check for upgrade authorization
            if re.search(r'function\s+_authorizeUpgrade', source):
                if 'onlyOwner' in source:
                    self._add_finding('critical', 'Upgradeable Proxy with Owner Control', 
                                     'Contract can be upgraded by owner at any time. Logic can be completely changed.')
                else:
                    self._add_finding('high', 'Upgradeable Proxy', 
                                     'Contract is upgradeable. Check who can authorize upgrades.')
            else:
                self._add_finding('critical', 'Upgradeable Proxy Without Authorization Check', 
                                 'Contract is upgradeable but lacks proper authorization control.')
        
        # Check for delegate calls to user-controlled addresses
        if re.search(r'delegatecall\([^)]*msg\.sender|delegatecall\([^)]*_\w+\)', source):
            self._add_finding('critical', 'User-Controlled Delegatecall', 
                             'Delegatecall to user-controlled address detected. Complete contract takeover possible.')
    
    async def _check_dangerous_patterns(self, source: str):
        """Check for other dangerous patterns"""
        
        # Check for excessive assembly usage
        assembly_blocks = re.findall(r'assembly\s*\{([^}]+)\}', source, re.DOTALL)
        if len(assembly_blocks) > 3:
            self._add_finding('medium', 'Excessive Assembly Usage', 
                             f'Found {len(assembly_blocks)} assembly blocks. Increases audit difficulty.')
        
        # Check for obfuscation attempts
        if re.search(r'\\x[0-9a-f]{2}|\\u[0-9a-f]{4}', source):
            self._add_finding('high', 'Possible Code Obfuscation', 
                             'Hex or unicode escape sequences detected. May indicate obfuscation.')
        
        # Check for suicide/selfdestruct
        if 'selfdestruct' in source or 'suicide' in source:
            self._add_finding('critical', 'Self-Destruct Present', 
                             'Contract can be destroyed with selfdestruct, locking all funds permanently.')
        
        # Check for no event emissions on critical functions
        critical_funcs = re.findall(r'function\s+(\w+)\s*\([^)]*\)[^{]*\{([^}]+)\}', source, re.DOTALL)
        for func_name, func_body in critical_funcs:
            is_critical = any(keyword in func_name.lower() for keyword in 
                            ['withdraw', 'mint', 'burn', 'transfer', 'approve'])
            if is_critical and 'emit ' not in func_body:
                self._add_finding('low', f'No Event Emission in {func_name}', 
                                 'Critical function does not emit events. Reduces transparency.')
                break
    
    async def _analyze_bytecode(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform SMART bytecode analysis using pattern recognition"""
        self.findings = []
        
        bytecode = contract_data.get('bytecode', '')
        
        if not bytecode or bytecode == '0x':
            self._add_finding('info', 'No Contract Code', 'Address has no bytecode.')
            return self.findings
        
        # SMART ANALYSIS: Check against known safe patterns
        from .bytecode_patterns import BytecodePatternMatcher
        
        logger.info("Running smart bytecode pattern matching...")
        analysis = BytecodePatternMatcher.analyze_contract_bytecode(bytecode)
        
        logger.info(f"Pattern matched: {analysis.get('pattern_matched')} (confidence: {analysis.get('confidence', 0):.2f})")
        
        # Check if it matches a known safe pattern
        if analysis.get('is_safe'):
            confidence = analysis.get('confidence', 0)
            
            # Contract matches safe pattern!
            self._add_finding('info', 'Unverified But Appears Standard', 
                             f"Source code not verified, but bytecode analysis suggests this is a standard contract. "
                             f"Pattern: {analysis['pattern_description']}. Confidence: {confidence*100:.0f}%.")
            
            self._add_finding('info', f"Detected Type: {analysis['pattern_description']}", 
                             f"Contract has {analysis['selector_count']} function selectors consistent with {analysis['pattern_matched']}.")
            
            # SELFDESTRUCT and DELEGATECALL are COMMON in proxies and safe contracts
            # Only flag as medium/low instead of critical
            if analysis.get('has_selfdestruct'):
                # Check if it's likely a proxy (has delegatecall too)
                if analysis.get('has_delegatecall'):
                    self._add_finding('low', 'Upgradeable Proxy Pattern Detected', 
                                     'Contract uses DELEGATECALL and SELFDESTRUCT, typical of upgradeable proxy contracts. '
                                     'This is NORMAL for modern smart contracts.')
                else:
                    self._add_finding('medium', 'Self-Destruct Capability Present', 
                                     'SELFDESTRUCT opcode detected. Could be for emergency shutdown. '
                                     'Common in legitimate contracts.')
            
            elif analysis.get('has_delegatecall'):
                self._add_finding('low', 'Delegatecall Pattern (Likely Proxy)', 
                                 'DELEGATECALL detected - likely an upgradeable proxy pattern. '
                                 'This is a standard implementation for upgradeable contracts.')
        
        else:
            # Did not match safe patterns strongly
            confidence = analysis.get('confidence', 0)
            
            if confidence >= 0.15:  # Has SOME standard functions
                self._add_finding('medium', 'Unverified Contract (Some Standard Functions)', 
                                 f"Source code not verified. Bytecode has some standard functions but does not strongly match known patterns. "
                                 f"Confidence: {confidence*100:.0f}%. Verify source code to be sure.")
                
                # Lower severity for opcodes if it has some standard functions
                if analysis.get('has_selfdestruct'):
                    self._add_finding('medium', 'Self-Destruct Capability', 
                                     'SELFDESTRUCT opcode detected.')
                
                if analysis.get('has_delegatecall'):
                    self._add_finding('medium', 'Delegatecall Detected', 
                                     'DELEGATECALL opcode detected.')
            
            else:
                # Really unknown pattern - be more careful
                self._add_finding('high', 'Unverified Contract (Unknown Pattern)', 
                                 'Source code not verified and bytecode does not match known patterns. '
                                 'Cannot determine if safe without source code verification.')
                
                if analysis.get('has_selfdestruct'):
                    self._add_finding('high', 'Self-Destruct in Unknown Contract', 
                                     'SELFDESTRUCT detected in contract with unknown pattern.')
                
                if analysis.get('has_delegatecall'):
                    self._add_finding('high', 'Delegatecall in Unknown Contract', 
                                     'DELEGATECALL detected in contract with unknown pattern.')
        
        # Size check
        size_kb = len(bytecode) / 2 / 1024  # Convert hex to KB
        if size_kb > 24:
            self._add_finding('info', 'Large Contract Size', 
                             f'Contract is {size_kb:.1f} KB. Max is 24KB. May be split across multiple contracts.')
        
        return self.findings
