"""Risk scoring and report generation engine"""
import logging
from typing import Dict, List, Any
from config import RISK_WEIGHTS

logger = logging.getLogger(__name__)

class RiskEngine:
    """Generates risk scores and reports from analysis findings"""
    
    def __init__(self):
        pass
    
    async def generate_report(
        self,
        address: str,
        contract_data: Dict[str, Any],
        static_findings: List[Dict[str, Any]],
        onchain_findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        
        # Combine all findings
        all_findings = static_findings + onchain_findings
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(all_findings)
        risk_level = self._get_risk_level(risk_score)
        risk_emoji = self._get_risk_emoji(risk_level)
        
        # Categorize findings by severity
        critical = [f for f in all_findings if f['severity'] == 'critical']
        high = [f for f in all_findings if f['severity'] == 'high']
        medium = [f for f in all_findings if f['severity'] == 'medium']
        low = [f for f in all_findings if f['severity'] == 'low']
        info = [f for f in all_findings if f['severity'] == 'info']
        
        # Format findings for display
        critical_formatted = [self._format_finding(f) for f in critical]
        high_formatted = [self._format_finding(f) for f in high]
        medium_formatted = [self._format_finding(f) for f in medium]
        low_formatted = [self._format_finding(f) for f in low]
        
        # Generate recommendation
        recommendation = self._generate_recommendation(risk_level, critical, high)
        
        # Determine contract type
        contract_type = self._determine_contract_type(contract_data, all_findings)
        
        report = {
            'address': address,
            'contract_type': contract_type,
            'verified': '✅ Yes' if contract_data.get('verified') else '❌ No',
            'compiler': contract_data.get('compiler_version', 'Unknown'),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_emoji': risk_emoji,
            'total_issues': len(critical) + len(high) + len(medium) + len(low),
            'critical_findings': critical_formatted,
            'high_findings': high_formatted,
            'medium_findings': medium_formatted,
            'low_findings': low_formatted,
            'info_findings': info,
            'recommendation': recommendation
        }
        
        return report
    
    def _calculate_risk_score(self, findings: List[Dict[str, Any]]) -> int:
        """Calculate overall risk score (0-100)"""
        total_score = 0
        
        # Count findings by severity
        critical_count = sum(1 for f in findings if f.get('severity') == 'critical')
        high_count = sum(1 for f in findings if f.get('severity') == 'high')
        
        for finding in findings:
            severity = finding.get('severity', 'info')
            weight = RISK_WEIGHTS.get(severity, 0)
            total_score += weight
        
        # SMART ADJUSTMENT: Reduce score for informational findings
        # "info" findings should not heavily impact score
        info_count = sum(1 for f in findings if f.get('severity') == 'info')
        if info_count > 5:
            # Too many info findings - likely a well-documented standard contract
            total_score = max(0, total_score - (info_count - 5) * 2)
        
        # If no critical or high findings, cap score lower
        if critical_count == 0 and high_count == 0:
            total_score = min(total_score, 40)  # Max "medium" risk if no critical/high
        
        # Cap at 100
        return min(total_score, 100)
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to risk level"""
        if score >= 80:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 25:
            return 'medium'
        elif score >= 10:
            return 'low'
        else:
            return 'safe'
    
    def _get_risk_emoji(self, level: str) -> str:
        """Get emoji for risk level"""
        emojis = {
            'critical': '⚫',
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
            'safe': '✅'
        }
        return emojis.get(level, '❓')
    
    def _format_finding(self, finding: Dict[str, Any]) -> str:
        """Format a finding for display"""
        title = finding.get('title', 'Unknown Issue')
        description = finding.get('description', '')
        
        return f"**{title}**\n{description}"
    
    def _generate_recommendation(self, risk_level: str, critical: List, high: List) -> str:
        """Generate overall recommendation"""
        
        if risk_level == 'critical':
            return (
                "⛔ **DO NOT INTERACT** with this contract.\n\n"
                f"Found {len(critical)} CRITICAL issues that can lead to complete loss of funds. "
                "This contract exhibits extremely dangerous patterns commonly used in scams and rug pulls.\n\n"
                "**Action:** Avoid this contract entirely. If you already interacted, revoke approvals immediately."
            )
        
        elif risk_level == 'high':
            return (
                "🚨 **HIGH RISK** - Exercise extreme caution.\n\n"
                f"Found {len(critical)} critical and {len(high)} high-risk issues. "
                "This contract has significant security concerns that could result in loss of funds.\n\n"
                "**Action:** Only interact if you fully understand the risks and trust the team. "
                "Consider waiting for a professional audit."
            )
        
        elif risk_level == 'medium':
            return (
                "⚠️ **MODERATE RISK** - Proceed with caution.\n\n"
                "This contract has some concerning patterns but may be legitimate. "
                "Common issues include centralized control or potential for abuse by owner.\n\n"
                "**Action:** DYOR on the team. Check for audit reports, team doxx, and community reputation. "
                "Start with small amounts."
            )
        
        elif risk_level == 'low':
            return (
                "✅ **LOW RISK** - Appears relatively safe.\n\n"
                "No major security issues detected. Minor concerns present but not critical.\n\n"
                "**Action:** Still DYOR. This analysis is automated and may miss some issues. "
                "Check for professional audits and verify contract source code."
            )
        
        else:  # safe
            return (
                "✅ **SAFE** - No significant issues detected.\n\n"
                "Contract appears to follow best practices with no major red flags.\n\n"
                "**Action:** While this analysis found no issues, always DYOR. "
                "Verify the contract is doing what you expect and check for professional audits."
            )
    
    def _determine_contract_type(self, contract_data: Dict[str, Any], findings: List[Dict]) -> str:
        """Determine the type of contract"""
        
        source = contract_data.get('source_code', '')
        
        if not source:
            return '❓ Unknown (Unverified)'
        
        # Check for common patterns
        if 'ERC721' in source:
            if any('mint' in f.get('title', '').lower() for f in findings):
                return '🎨 ERC-721 NFT Mint Contract'
            return '🎨 ERC-721 NFT Collection'
        
        if 'ERC1155' in source:
            return '🎨 ERC-1155 Multi-Token'
        
        if 'ERC20' in source or '_transfer' in source:
            if 'presale' in source.lower() or 'ico' in source.lower():
                return '💰 ERC-20 Token Presale'
            if 'staking' in source.lower():
                return '💰 ERC-20 Staking Contract'
            if 'uniswap' in source.lower() or 'pancake' in source.lower():
                return '💱 ERC-20 DEX Token'
            return '💰 ERC-20 Token'
        
        if 'Proxy' in source or 'proxy' in source.lower():
            return '🔄 Upgradeable Proxy'
        
        if 'Vault' in source or 'vault' in source.lower():
            return '🏦 Vault Contract'
        
        if 'Timelock' in source or 'timelock' in source.lower():
            return '⏰ Timelock Controller'
        
        if 'Multisig' in source or 'multisig' in source.lower():
            return '👥 Multisig Wallet'
        
        # Default
        return '📄 Smart Contract'
