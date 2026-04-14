"""Contract Analysis Discord Cog"""
import discord
from discord import app_commands
from discord.ext import commands
import logging
import asyncio
from typing import Optional
import re
import time
from collections import defaultdict

from analyzers.contract_fetcher import ContractFetcher
from analyzers.static_analyzer import StaticAnalyzer
from analyzers.onchain_checker import OnChainChecker
from analyzers.risk_engine import RiskEngine
from config import RATE_LIMIT_WINDOW, RATE_LIMIT_MAX

logger = logging.getLogger(__name__)

class ContractAnalysis(commands.Cog):
    """Cog for contract security analysis commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.fetcher = ContractFetcher()
        self.static_analyzer = StaticAnalyzer()
        self.onchain_checker = OnChainChecker()
        self.risk_engine = RiskEngine()
        
        # Rate limiting: user_id -> list of timestamps
        self.rate_limit_cache = defaultdict(list)
        self.rate_limit_window = RATE_LIMIT_WINDOW
        self.rate_limit_max = RATE_LIMIT_MAX
    
    def is_valid_address(self, address: str) -> bool:
        """Validate Ethereum address format"""
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, address))
    
    def check_rate_limit(self, user_id: int) -> tuple[bool, int]:
        """
        Check if user has exceeded rate limit
        Returns: (is_allowed, seconds_until_reset)
        """
        now = time.time()
        
        # Clean old timestamps
        self.rate_limit_cache[user_id] = [
            ts for ts in self.rate_limit_cache[user_id]
            if now - ts < self.rate_limit_window
        ]
        
        # Check limit
        if len(self.rate_limit_cache[user_id]) >= self.rate_limit_max:
            oldest = self.rate_limit_cache[user_id][0]
            reset_in = int(self.rate_limit_window - (now - oldest))
            return False, reset_in
        
        # Add current timestamp
        self.rate_limit_cache[user_id].append(now)
        return True, 0
    
    async def create_embed(self, title: str, description: str, color: discord.Color) -> discord.Embed:
        """Create a formatted embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        embed.set_footer(text="Tempo Contract Analyzer | Not financial advice. Always DYOR.")
        return embed
    
    @app_commands.command(
        name="analyze-contract",
        description="Analyze a Tempo blockchain smart contract for security risks"
    )
    @app_commands.describe(
        contract_address="The contract address on Tempo blockchain (0x...)"
    )
    async def analyze_contract(
        self,
        interaction: discord.Interaction,
        contract_address: str
    ):
        """Analyze a smart contract for security vulnerabilities"""
        
        # Check rate limit
        allowed, reset_in = self.check_rate_limit(interaction.user.id)
        if not allowed:
            embed = discord.Embed(
                title="⏱️ Rate Limit Exceeded",
                description=f"You can analyze up to {self.rate_limit_max} contracts per {self.rate_limit_window} seconds.\n\n"
                           f"Please try again in **{reset_in} seconds**.",
                color=0xFFA500  # Orange
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Defer the response since analysis takes time
        await interaction.response.defer(thinking=True)
        
        try:
            # Validate address format
            contract_address = contract_address.strip()
            if not self.is_valid_address(contract_address):
                embed = await self.create_embed(
                    title="❌ Invalid Address",
                    description=f"The address `{contract_address}` is not a valid Ethereum address.\n\n"
                               f"Expected format: `0x` followed by 40 hexadecimal characters",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Send initial status
            status_embed = await self.create_embed(
                title="🔍 Analyzing Contract",
                description=f"**Address:** `{contract_address}`\n\n"
                           f"⏳ Fetching contract data from Tempo blockchain...",
                color=discord.Color.blue()
            )
            status_msg = await interaction.followup.send(embed=status_embed)
            
            # Step 1: Fetch contract data
            logger.info(f"Fetching contract data for {contract_address}")
            contract_data = await self.fetcher.fetch_contract(contract_address)
            
            if contract_data.get('error'):
                embed = await self.create_embed(
                    title="❌ Contract Not Found",
                    description=f"**Address:** `{contract_address}`\n\n"
                               f"Error: {contract_data['error']}\n\n"
                               f"Please verify:\n"
                               f"• The address is correct\n"
                               f"• The contract exists on Tempo blockchain\n"
                               f"• The contract is deployed (not just an EOA)",
                    color=discord.Color.red()
                )
                await status_msg.edit(embed=embed)
                return
            
            # Update status
            status_embed.description = (
                f"**Address:** `{contract_address}`\n"
                f"**Status:** Contract found!\n\n"
                f"⏳ Performing static code analysis..."
            )
            await status_msg.edit(embed=status_embed)
            
            # Step 2: Static Analysis
            logger.info(f"Running static analysis for {contract_address}")
            static_findings = await self.static_analyzer.analyze(contract_data)
            
            # Update status
            status_embed.description = (
                f"**Address:** `{contract_address}`\n"
                f"**Status:** Static analysis complete!\n\n"
                f"⏳ Checking on-chain state..."
            )
            await status_msg.edit(embed=status_embed)
            
            # Step 3: On-Chain Analysis
            logger.info(f"Running on-chain checks for {contract_address}")
            onchain_findings = await self.onchain_checker.check(contract_address, contract_data)
            
            # Update status
            status_embed.description = (
                f"**Address:** `{contract_address}`\n"
                f"**Status:** On-chain analysis complete!\n\n"
                f"⏳ Generating security report..."
            )
            await status_msg.edit(embed=status_embed)
            
            # Step 4: Risk Scoring and Report Generation
            logger.info(f"Generating risk report for {contract_address}")
            report = await self.risk_engine.generate_report(
                contract_address,
                contract_data,
                static_findings,
                onchain_findings
            )
            
            # Step 5: Send Results
            await self.send_report(interaction, status_msg, report)
            
        except asyncio.TimeoutError:
            embed = await self.create_embed(
                title="⏱️ Analysis Timeout",
                description=f"Analysis of `{contract_address}` took too long.\n"
                           f"This may happen with very large or complex contracts.\n\n"
                           f"Please try again or contact support if this persists.",
                color=discord.Color.orange()
            )
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error analyzing contract {contract_address}: {e}", exc_info=True)
            embed = await self.create_embed(
                title="❌ Analysis Error",
                description=f"An unexpected error occurred during analysis:\n"
                           f"```{str(e)[:500]}```\n\n"
                           f"Please try again or contact support.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    
    async def send_report(self, interaction, status_msg, report):
        """Send the analysis report in formatted embeds"""
        
        # Determine color based on risk level (exact hex codes)
        risk_colors = {
            'critical': 0xFF0000,  # Red
            'high': 0xFF0000,      # Red
            'medium': 0xFFFF00,    # Yellow
            'low': 0x00FF00,       # Green
            'safe': 0x00FF00       # Green
        }
        color = risk_colors.get(report['risk_level'], 0x0099FF)
        
        # Truncate address for title
        short_addr = f"{report['address'][:6]}...{report['address'][-4:]}"
        
        # Main Report Embed
        main_embed = discord.Embed(
            title=f"Tempo Contract Analysis: {short_addr}",
            color=color
        )
        
        # Contract Type and Verification
        main_embed.add_field(
            name="📄 Contract Type",
            value=report['contract_type'],
            inline=True
        )
        
        main_embed.add_field(
            name="✅ Verification Status",
            value=report['verified'],
            inline=True
        )
        
        main_embed.add_field(
            name="\u200b",  # Empty field for spacing
            value="\u200b",
            inline=True
        )
        
        # Risk Summary with specific format
        risk_summary = self._format_risk_summary(report)
        main_embed.add_field(
            name="🛡️ Risk Summary",
            value=risk_summary,
            inline=False
        )
        
        # Key Findings section
        if report['total_issues'] > 0:
            key_findings = self._format_key_findings(report)
            
            # Split if too long (Discord 1024 char limit per field)
            if len(key_findings) > 1024:
                chunks = self._split_findings(key_findings)
                for i, chunk in enumerate(chunks):
                    field_name = "🔍 Key Findings" if i == 0 else "🔍 Key Findings (cont.)"
                    main_embed.add_field(
                        name=field_name,
                        value=chunk,
                        inline=False
                    )
            else:
                main_embed.add_field(
                    name="🔍 Key Findings",
                    value=key_findings,
                    inline=False
                )
        
        # Recommendations section
        recommendations = self._format_recommendations(report)
        main_embed.add_field(
            name="💡 Recommendations",
            value=recommendations,
            inline=False
        )
        
        # Footer with exact text
        main_embed.set_footer(
            text="Analysis powered by AI static + on-chain checks. Always DYOR. Not financial advice. This is not a substitute for professional audit."
        )
        
        # Full address in description
        main_embed.description = f"**Full Address:** `{report['address']}`"
        
        # Delete status message and send report
        await status_msg.delete()
        await interaction.followup.send(embed=main_embed)
    
    def _format_risk_summary(self, report: dict) -> str:
        """Format risk summary with color-coded messages"""
        level = report['risk_level']
        
        if level in ['safe', 'low']:
            return (
                f"**✅ SAFE** - This contract appears safe based on static and on-chain analysis. "
                f"No major risks detected.\n\n"
                f"**Risk Score:** {report['risk_score']}/100 (Low)"
            )
        elif level == 'medium':
            issues_text = self._get_summary_issues(report, ['medium'])
            return (
                f"**⚠️ WARNING** - Moderate risks detected.\n\n"
                f"{issues_text}\n\n"
                f"**Risk Score:** {report['risk_score']}/100 (Medium)"
            )
        else:  # high or critical
            return (
                f"**⚠️ HIGH RISK - Potential for asset/fund loss!**\n\n"
                f"This contract exhibits dangerous patterns that could result in loss of funds or assets.\n\n"
                f"**Risk Score:** {report['risk_score']}/100 (CRITICAL)"
            )
    
    def _get_summary_issues(self, report: dict, severities: list) -> str:
        """Get brief summary of issues by severity"""
        issues = []
        for severity in severities:
            key = f"{severity}_findings"
            if report.get(key):
                count = len(report[key])
                issues.append(f"• {count} {severity.upper()} issue(s)")
        return "\n".join(issues) if issues else "Minor issues detected"
    
    def _format_key_findings(self, report: dict) -> str:
        """Format key findings in plain English with explanations"""
        findings = []
        
        # Critical findings first
        for finding in report.get('critical_findings', [])[:3]:  # Top 3 critical
            findings.append(f"🔴 **CRITICAL:** {finding}")
        
        # High findings
        for finding in report.get('high_findings', [])[:3]:  # Top 3 high
            findings.append(f"🟠 **HIGH:** {finding}")
        
        # Medium findings
        for finding in report.get('medium_findings', [])[:2]:  # Top 2 medium
            findings.append(f"🟡 **MEDIUM:** {finding}")
        
        if not findings:
            return "✅ No significant security issues detected."
        
        return "\n\n".join(findings)
    
    def _split_findings(self, text: str) -> list:
        """Split long findings into chunks under 1024 chars"""
        chunks = []
        current = ""
        
        for line in text.split("\n\n"):
            if len(current) + len(line) + 2 > 1024:
                chunks.append(current)
                current = line
            else:
                current += "\n\n" + line if current else line
        
        if current:
            chunks.append(current)
        
        return chunks
    
    def _format_recommendations(self, report: dict) -> str:
        """Format recommendations based on risk level"""
        level = report['risk_level']
        
        if level in ['safe', 'low']:
            return (
                "✅ **Proceed with caution:**\n"
                "• Contract appears relatively safe\n"
                "• Still recommended to start with small amounts\n"
                "• Verify the contract does what you expect\n"
                "• Check for professional audit reports"
            )
        elif level == 'medium':
            return (
                "⚠️ **Exercise caution:**\n"
                "• Review the identified risks carefully\n"
                "• Only interact if you understand the implications\n"
                "• Use small test amounts first\n"
                "• Check team reputation and social channels\n"
                "• Wait for professional audit if possible"
            )
        else:  # high or critical
            return (
                "🛑 **DO NOT APPROVE OR SEND FUNDS:**\n"
                "• This contract has critical security issues\n"
                "• High risk of losing your assets/funds\n"
                "• If already interacted, revoke approvals immediately\n"
                "• Wait for professional security audit\n"
                "• Avoid until issues are addressed"
            )

async def setup(bot):
    """Setup function for cog"""
    await bot.add_cog(ContractAnalysis(bot))
