"""
Smart Pattern Recognition
Distinguishes legitimate patterns from malicious ones
"""
import re

class SmartPatterns:
    """Recognizes legitimate vs malicious patterns"""
    
    # Known safe contracts and standards
    OPENZEPPELIN_PATTERNS = [
        r'@openzeppelin/contracts',
        r'OpenZeppelin',
        r'SPDX-License-Identifier:\s*MIT',
    ]
    
    # Standard ERC patterns (legitimate)
    STANDARD_ERC_PATTERNS = {
        'ERC721': [
            r'function\s+approve\s*\(\s*address\s+to\s*,\s*uint256\s+tokenId\s*\)',
            r'function\s+setApprovalForAll\s*\(\s*address\s+operator\s*,\s*bool\s+approved\s*\)',
            r'function\s+transferFrom\s*\(\s*address\s+from\s*,\s*address\s+to\s*,\s*uint256\s+tokenId\s*\)',
            r'function\s+ownerOf\s*\(\s*uint256\s+tokenId\s*\)',
            r'function\s+tokenURI\s*\(\s*uint256\s+tokenId\s*\)',
        ],
        'ERC1155': [
            r'function\s+setApprovalForAll\s*\(\s*address\s+operator\s*,\s*bool\s+approved\s*\)',
            r'function\s+safeTransferFrom',
            r'function\s+balanceOf\s*\(\s*address\s+account\s*,\s*uint256\s+id\s*\)',
        ],
        'ERC20': [
            r'function\s+approve\s*\(\s*address\s+spender\s*,\s*uint256\s+amount\s*\)',
            r'function\s+transfer\s*\(\s*address\s+to\s*,\s*uint256\s+amount\s*\)',
            r'function\s+allowance\s*\(\s*address\s+owner\s*,\s*address\s+spender\s*\)',
        ]
    }
    
    # Legitimate ownership patterns (OpenZeppelin Ownable)
    SAFE_OWNERSHIP_PATTERNS = [
        r'contract\s+Ownable\s*\{',  # OpenZeppelin Ownable
        r'import.*Ownable\.sol',
        r'function\s+renounceOwnership\s*\(\s*\)\s+public\s+virtual\s+onlyOwner',
        r'function\s+transferOwnership\s*\(\s*address\s+newOwner\s*\)\s+public\s+virtual\s+onlyOwner',
    ]
    
    # Legitimate mint patterns (not necessarily dangerous)
    SAFE_MINT_PATTERNS = [
        r'function\s+mint.*public\s+payable',  # Public paid mint
        r'require\s*\(\s*msg\.value\s*>=',  # Requires payment
        r'require\s*\(\s*totalSupply.*<.*maxSupply',  # Has max supply check
        r'require\s*\(\s*_mintAmount\s*\+\s*totalSupply.*<=.*MAX_SUPPLY',
    ]
    
    # Known safe marketplace contracts
    KNOWN_MARKETPLACES = [
        'opensea',
        'rarible',
        'looksrare',
        'blur',
        'x2y2',
        'nftrade',
        'element',
    ]
    
    @staticmethod
    def is_openzeppelin_based(source: str) -> bool:
        """Check if contract uses OpenZeppelin (generally safer)"""
        for pattern in SmartPatterns.OPENZEPPELIN_PATTERNS:
            if re.search(pattern, source, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def is_standard_erc(source: str, erc_type: str) -> bool:
        """Check if contract implements standard ERC properly"""
        if erc_type not in SmartPatterns.STANDARD_ERC_PATTERNS:
            return False
        
        patterns = SmartPatterns.STANDARD_ERC_PATTERNS[erc_type]
        matches = sum(1 for p in patterns if re.search(p, source))
        
        # If it implements most of the standard functions, it's likely legitimate
        return matches >= len(patterns) * 0.6  # 60% threshold
    
    @staticmethod
    def has_safe_ownership(source: str) -> bool:
        """Check if ownership pattern is standard OpenZeppelin"""
        for pattern in SmartPatterns.SAFE_OWNERSHIP_PATTERNS:
            if re.search(pattern, source, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def has_safe_mint_pattern(source: str) -> bool:
        """Check if mint pattern is legitimate (paid, max supply, etc.)"""
        safe_indicators = 0
        
        for pattern in SmartPatterns.SAFE_MINT_PATTERNS:
            if re.search(pattern, source, re.IGNORECASE):
                safe_indicators += 1
        
        # If it has multiple safe indicators, likely legitimate
        return safe_indicators >= 2
    
    @staticmethod
    def detect_contract_purpose(source: str) -> str:
        """Detect the main purpose of the contract"""
        
        # NFT Collection
        if 'ERC721' in source or 'ERC1155' in source:
            if re.search(r'function\s+mint', source, re.IGNORECASE):
                return 'NFT_COLLECTION_WITH_MINT'
            return 'NFT_COLLECTION'
        
        # Token
        if 'ERC20' in source:
            if re.search(r'Uniswap|Pancake|swap', source, re.IGNORECASE):
                return 'DEX_TOKEN'
            return 'TOKEN'
        
        # Marketplace
        if any(market in source.lower() for market in SmartPatterns.KNOWN_MARKETPLACES):
            return 'MARKETPLACE'
        
        # Staking
        if re.search(r'stake|staking|reward', source, re.IGNORECASE):
            return 'STAKING'
        
        # Vault/Treasury
        if re.search(r'vault|treasury', source, re.IGNORECASE):
            return 'VAULT'
        
        return 'UNKNOWN'
    
    @staticmethod
    def is_approval_dangerous(source: str, contract_purpose: str) -> bool:
        """
        Check if approval pattern is dangerous in this context
        NFT collections and marketplaces SHOULD have approval functions
        """
        
        # Approvals are EXPECTED and SAFE for:
        if contract_purpose in ['NFT_COLLECTION', 'NFT_COLLECTION_WITH_MINT', 'MARKETPLACE', 'TOKEN']:
            return False
        
        # Check for unusual approval patterns
        unusual_patterns = [
            r'approve.*delegatecall',  # Delegatecall in approve
            r'approve.*selfdestruct',  # Selfdestruct in approve
            r'transferFrom.*msg\.sender.*owner',  # Transfers without approval check
        ]
        
        for pattern in unusual_patterns:
            if re.search(pattern, source, re.IGNORECASE | re.DOTALL):
                return True
        
        return False
    
    @staticmethod
    def calculate_confidence_score(source: str) -> float:
        """
        Calculate confidence that this is a legitimate contract
        Returns 0.0 (definitely malicious) to 1.0 (definitely safe)
        """
        score = 0.5  # Start neutral
        
        # Positive indicators
        if SmartPatterns.is_openzeppelin_based(source):
            score += 0.2
        
        if SmartPatterns.is_standard_erc(source, 'ERC721'):
            score += 0.15
        elif SmartPatterns.is_standard_erc(source, 'ERC20'):
            score += 0.15
        
        if SmartPatterns.has_safe_ownership(source):
            score += 0.1
        
        if 'SPDX-License-Identifier' in source:
            score += 0.05
        
        # Negative indicators
        if 'selfdestruct' in source:
            score -= 0.3
        
        if re.search(r'delegatecall.*assembly', source, re.IGNORECASE | re.DOTALL):
            score -= 0.2
        
        # Obfuscation
        if re.search(r'\\x[0-9a-f]{2}', source):
            score -= 0.15
        
        return max(0.0, min(1.0, score))
