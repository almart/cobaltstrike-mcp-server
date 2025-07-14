"""MCP prompts for Cobalt Strike operations and analysis."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP

logger = logging.getLogger(__name__)


def add_cobalt_strike_prompts(mcp_server: FastMCP) -> None:
    """Add MCP prompts to the Cobalt Strike server.
    
    Args:
        mcp_server: The FastMCP server instance to add prompts to
    """
    
    @mcp_server.prompt()
    async def cobalt_strike_analysis(beacon_id: str = "", task_type: str = "general") -> str:
        """Analyze Cobalt Strike beacon data and generate security insights.
        
        Args:
            beacon_id: Specific beacon ID to analyze (optional)
            task_type: Type of analysis (general, lateral_movement, persistence, data_exfil)
        
        Returns:
            Formatted analysis prompt for the AI assistant
        """
        prompt_base = """You are a cybersecurity analyst reviewing Cobalt Strike beacon activity. 
        
Your task is to analyze the provided beacon data and identify:
1. Potential security risks and vulnerabilities
2. Attack patterns and techniques used
3. Next steps for adversary simulation
4. Timeline of activities and progression

"""
        
        if beacon_id:
            prompt_base += f"\nFocus your analysis on beacon ID: {beacon_id}\n"
        
        analysis_context = {
            "general": "Provide a comprehensive overview of all beacon activities.",
            "lateral_movement": "Focus on lateral movement techniques and credential harvesting.",
            "persistence": "Analyze persistence mechanisms and backdoor installations.",
            "data_exfil": "Examine data exfiltration attempts and sensitive file access."
        }
        
        specific_context = analysis_context.get(task_type, analysis_context["general"])
        prompt_base += f"\nAnalysis Focus: {specific_context}\n"
        
        prompt_base += """
Please structure your analysis as follows:
- Executive Summary
- Technical Details
- Risk Assessment
- Recommendations
- Next Steps

Use the available Cobalt Strike MCP tools to gather the necessary data for your analysis.
"""
        
        return prompt_base

    @mcp_server.prompt()
    async def red_team_operation_plan(target_scope: str = "", objectives: str = "") -> str:
        """Generate a red team operation planning prompt.
        
        Args:
            target_scope: Target environment scope (e.g., "internal network", "web applications")
            objectives: Operation objectives (e.g., "privilege escalation", "data access")
        
        Returns:
            Structured prompt for red team operation planning
        """
        prompt = """You are a red team operations specialist planning a security assessment using Cobalt Strike.

**Operation Planning Framework:**

1. **Reconnaissance Phase**
   - Network discovery and enumeration
   - Service identification and vulnerability assessment
   - Initial access vector identification

2. **Initial Access**
   - Payload delivery and execution
   - Beacon establishment and communication
   - Initial foothold verification

3. **Post-Exploitation**
   - Privilege escalation opportunities
   - Lateral movement pathways
   - Persistence mechanism deployment

4. **Objectives Achievement**
   - Data identification and access
   - System compromise demonstration
   - Impact assessment

5. **Documentation and Reporting**
   - Activity logging and evidence collection
   - Risk assessment and business impact
   - Remediation recommendations

"""
        
        if target_scope:
            prompt += f"\n**Target Scope:** {target_scope}\n"
        
        if objectives:
            prompt += f"\n**Primary Objectives:** {objectives}\n"
        
        prompt += """
**Available Tools:**
Use the Cobalt Strike MCP tools to execute this operation plan systematically. Focus on:
- Beacon management and tasking
- Command execution and data collection
- Operational security and stealth
- Comprehensive documentation

Plan your approach step-by-step and use the appropriate MCP tools for each phase.
"""
        
        return prompt

    @mcp_server.prompt()
    async def incident_response_analysis(incident_type: str = "unknown", severity: str = "medium") -> str:
        """Generate an incident response analysis prompt for Cobalt Strike activities.
        
        Args:
            incident_type: Type of incident (malware, breach, suspicious_activity, etc.)
            severity: Incident severity level (low, medium, high, critical)
        
        Returns:
            Structured incident response analysis prompt
        """
        prompt = f"""You are an incident response analyst investigating a security incident involving Cobalt Strike activity.

**Incident Details:**
- Type: {incident_type}
- Severity: {severity.upper()}
- Investigation Tool: Cobalt Strike MCP Server

**Investigation Framework:**

1. **Initial Assessment**
   - Scope of compromise determination
   - Timeline establishment
   - Affected systems identification

2. **Evidence Collection**
   - Beacon activity analysis
   - Command execution history
   - File system artifacts
   - Network communication patterns

3. **Threat Analysis**
   - Attack vector identification
   - Tactics, Techniques, and Procedures (TTPs)
   - Indicators of Compromise (IOCs)
   - Attribution assessment

4. **Impact Assessment**
   - Data exposure evaluation
   - System compromise extent
   - Business impact analysis
   - Regulatory implications

5. **Containment and Remediation**
   - Immediate containment actions
   - Eradication strategies
   - Recovery procedures
   - Lessons learned

**Analysis Approach:**
Use the Cobalt Strike MCP tools to systematically gather evidence and analyze the incident. Focus on:
- Comprehensive beacon activity review
- Timeline reconstruction
- Attack pattern identification
- Forensic evidence preservation

Document all findings with supporting evidence from the MCP tools.
"""
        
        return prompt

    logger.info("Added MCP prompts: cobalt_strike_analysis, red_team_operation_plan, incident_response_analysis")