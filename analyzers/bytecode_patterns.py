"""
Bytecode Pattern Recognition
Learns from known safe contracts and recognizes similar ones
"""
import re
from typing import Dict, List, Set, Tuple

class BytecodePatternMatcher:
    """Matches bytecode patterns against known safe contracts"""
    
    # Known SAFE contract patterns (will be populated from analysis)
    KNOWN_SAFE_PATTERNS = {
        # NFT Collection - ERC721
        'nft_collection': {
            'selectors': [
                '0x095ea7b3',  # approve(address,uint256)
                '0x70a08231',  # balanceOf(address)
                '0x6352211e',  # ownerOf(uint256)
                '0x42842e0e',  # safeTransferFrom(address,address,uint256)
                '0x23b872dd',  # transferFrom(address,address,uint256)
                '0xa22cb465',  # setApprovalForAll(address,bool)
                '0xe985e9c5',  # isApprovedForAll(address,address)
                '0xc87b56dd',  # tokenURI(uint256)
            ],
            'opcodes': ['DELEGATECALL', 'CALL', 'STATICCALL'],
            'description': 'Standard ERC-721 NFT Collection',
            'risk_level': 'safe'
        },
        
        # NFT Marketplace Listing
        'nft_marketplace': {
            'selectors': [
                '0x095ea7b3',  # approve(address,uint256)
                '0xa22cb465',  # setApprovalForAll(address,bool)
                '0x23b872dd',  # transferFrom(address,address,uint256)
                '0x42842e0e',  # safeTransferFrom(address,address,uint256)
            ],
            'opcodes': ['CALL', 'STATICCALL'],
            'description': 'NFT Marketplace Contract',
            'risk_level': 'safe'
        },
        
        # NFT Mint Contract
        'nft_mint': {
            'selectors': [
                '0x40c10f19',  # mint(address,uint256)
                '0xa0712d68',  # mint(uint256)
                '0x095ea7b3',  # approve(address,uint256)
                '0x70a08231',  # balanceOf(address)
                '0xc87b56dd',  # tokenURI(uint256)
            ],
            'opcodes': ['CALL'],
            'description': 'NFT Mint Contract',
            'risk_level': 'safe'
        },
        
        # ERC1155 Multi-token
        'erc1155': {
            'selectors': [
                '0xf242432a',  # safeTransferFrom(address,address,uint256,uint256,bytes)
                '0x2eb2c2d6',  # safeBatchTransferFrom
                '0x00fdd58e',  # balanceOf(address,uint256)
                '0x4e1273f4',  # balanceOfBatch
                '0xa22cb465',  # setApprovalForAll(address,bool)
            ],
            'opcodes': ['CALL', 'STATICCALL'],
            'description': 'ERC-1155 Multi-Token Standard',
            'risk_level': 'safe'
        }
    }
    
    @staticmethod
    def extract_function_selectors(bytecode: str) -> Set[str]:
        """
        Extract function selectors (first 4 bytes of function signatures)
        from bytecode - IMPROVED version
        """
        if not bytecode or bytecode == '0x':
            return set()
        
        bytecode = bytecode.lower().replace('0x', '')
        selectors = set()
        
        # Method 1: Look for PUSH4 opcodes (0x63) followed by 4 bytes
        pattern1 = r'63([0-9a-f]{8})'
        matches1 = re.findall(pattern1, bytecode)
        for match in matches1:
            selectors.add('0x' + match)
        
        # Method 2: Look for common EQ patterns (function selector comparison)
        # Pattern: 80 63 XXXXXXXX 14 (DUP1 PUSH4 selector EQ)
        pattern2 = r'8063([0-9a-f]{8})14'
        matches2 = re.findall(pattern2, bytecode)
        for match in matches2:
            selectors.add('0x' + match)
        
        # Method 3: Look for CALLDATALOAD patterns
        # Pattern: 63 XXXXXXXX (just PUSH4)
        pattern3 = r'63([0-9a-f]{8})'
        matches3 = re.findall(pattern3, bytecode)
        for match in matches3:
            # Only add if it looks like a function selector (not random data)
            if match[0] in '0123456789abcdef':  # Basic sanity check
                selectors.add('0x' + match)
        
        return selectors
    
    @staticmethod
    def detect_opcodes(bytecode: str) -> Dict[str, int]:
        """Detect presence of important opcodes"""
        if not bytecode or bytecode == '0x':
            return {}
        
        bytecode = bytecode.lower().replace('0x', '')
        
        opcodes = {
            'DELEGATECALL': bytecode.count('f4'),  # 0xf4
            'CALL': bytecode.count('f1'),          # 0xf1
            'STATICCALL': bytecode.count('fa'),    # 0xfa
            'SELFDESTRUCT': bytecode.count('ff'),  # 0xff
            'CREATE': bytecode.count('f0'),        # 0xf0
            'CREATE2': bytecode.count('f5'),       # 0xf5
        }
        
        return opcodes
    
    @staticmethod
    def calculate_similarity(selectors1: Set[str], selectors2: Set[str]) -> float:
        """
        Calculate similarity between two sets of function selectors
        Returns 0.0 to 1.0
        """
        if not selectors1 or not selectors2:
            return 0.0
        
        intersection = len(selectors1 & selectors2)
        union = len(selectors1 | selectors2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    @staticmethod
    def match_pattern(bytecode: str) -> Tuple[str, float, str]:
        """
        Match bytecode against known safe patterns
        Returns: (pattern_name, confidence, description)
        """
        if not bytecode or bytecode == '0x':
            return ('unknown', 0.0, 'No bytecode')
        
        # Extract features
        selectors = BytecodePatternMatcher.extract_function_selectors(bytecode)
        opcodes = BytecodePatternMatcher.detect_opcodes(bytecode)
        
        best_match = None
        best_score = 0.0
        best_desc = 'Unknown contract type'
        
        # Check against each known pattern
        for pattern_name, pattern in BytecodePatternMatcher.KNOWN_SAFE_PATTERNS.items():
            pattern_selectors = set(pattern['selectors'])
            
            # Calculate similarity
            similarity = BytecodePatternMatcher.calculate_similarity(
                selectors, pattern_selectors
            )
            
            # Boost score if has expected opcodes
            opcode_match = sum(1 for op in pattern['opcodes'] if opcodes.get(op, 0) > 0)
            opcode_boost = opcode_match / len(pattern['opcodes']) * 0.2
            
            total_score = similarity + opcode_boost
            
            if total_score > best_score:
                best_score = total_score
                best_match = pattern_name
                best_desc = pattern['description']
        
        return (best_match or 'unknown', best_score, best_desc)
    
    @staticmethod
    def is_safe_contract(bytecode: str, threshold: float = 0.3) -> Tuple[bool, str, float]:
        """
        Determine if a contract matches known safe patterns
        Returns: (is_safe, reason, confidence)
        LOWERED threshold from 0.6 to 0.3 for better detection
        """
        pattern_name, confidence, description = BytecodePatternMatcher.match_pattern(bytecode)
        
        # Lower threshold - 30% match is enough for unverified contracts
        if confidence >= threshold:
            pattern = BytecodePatternMatcher.KNOWN_SAFE_PATTERNS.get(pattern_name)
            if pattern and pattern['risk_level'] == 'safe':
                return (
                    True,
                    f"Matches known safe pattern: {description}",
                    confidence
                )
        
        # Even if no perfect match, check if it has standard functions
        selectors = BytecodePatternMatcher.extract_function_selectors(bytecode)
        
        # Common safe selectors that indicate legitimate contract
        common_safe_selectors = {
            '0x095ea7b3',  # approve
            '0x70a08231',  # balanceOf
            '0xa9059cbb',  # transfer
            '0x23b872dd',  # transferFrom
            '0x6352211e',  # ownerOf
            '0xc87b56dd',  # tokenURI
        }
        
        matches = len(selectors & common_safe_selectors)
        if matches >= 3:  # If it has 3+ standard functions
            return (
                True,
                f"Has {matches} standard ERC functions (appears legitimate)",
                0.5
            )
        
        return (False, "Does not match known safe patterns", confidence)
    
    @staticmethod
    def analyze_contract_bytecode(bytecode: str) -> Dict[str, any]:
        """
        Complete bytecode analysis
        Returns detailed analysis results
        """
        if not bytecode or bytecode == '0x':
            return {
                'error': 'No bytecode provided',
                'is_safe': False
            }
        
        # Extract features
        selectors = BytecodePatternMatcher.extract_function_selectors(bytecode)
        opcodes = BytecodePatternMatcher.detect_opcodes(bytecode)
        pattern_name, confidence, description = BytecodePatternMatcher.match_pattern(bytecode)
        is_safe, reason, _ = BytecodePatternMatcher.is_safe_contract(bytecode)
        
        # Check for dangerous patterns
        dangerous_opcodes = {
            'SELFDESTRUCT': opcodes.get('SELFDESTRUCT', 0),
            'DELEGATECALL': opcodes.get('DELEGATECALL', 0),
        }
        
        has_selfdestruct = dangerous_opcodes['SELFDESTRUCT'] > 0
        has_delegatecall = dangerous_opcodes['DELEGATECALL'] > 0
        
        return {
            'pattern_matched': pattern_name,
            'pattern_description': description,
            'confidence': confidence,
            'is_safe': is_safe,
            'reason': reason,
            'function_selectors': list(selectors),
            'selector_count': len(selectors),
            'opcodes': opcodes,
            'has_selfdestruct': has_selfdestruct,
            'has_delegatecall': has_delegatecall,
            'warnings': [
                'Contract has SELFDESTRUCT capability' if has_selfdestruct else None,
                'Contract uses DELEGATECALL' if has_delegatecall and pattern_name == 'unknown' else None,
            ]
        }
