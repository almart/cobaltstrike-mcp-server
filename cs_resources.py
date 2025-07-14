"""MCP resources for Cobalt Strike data access."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP
    from cs_client import CobaltStrikeClient

logger = logging.getLogger(__name__)


def add_cobalt_strike_resources(mcp_server: FastMCP, cs_client: CobaltStrikeClient) -> None:
    """Add MCP resources to the Cobalt Strike server.
    
    Args:
        mcp_server: The FastMCP server instance to add resources to
        cs_client: The authenticated Cobalt Strike client
    """
    
    @mcp_server.resource("cobalt-strike://beacons/active")
    async def active_beacons_resource() -> str:
        """Get current active beacons in JSON format.
        
        Returns:
            JSON representation of all active beacons
        """
        try:
            client = cs_client.get_authenticated_client()
            response = await client.get("/api/v1/beacons")
            if response.status_code == 200:
                return response.text
            else:
                return json.dumps({
                    "error": "Failed to fetch beacons",
                    "status_code": response.status_code,
                    "message": "Unable to retrieve active beacon data"
                })
        except Exception as e:
            return json.dumps({
                "error": "Exception occurred",
                "exception": str(e),
                "message": "Error while fetching beacon data"
            })

    @mcp_server.resource("cobalt-strike://config/server-info")
    async def server_info_resource() -> str:
        """Get Cobalt Strike server information and configuration.
        
        Returns:
            JSON representation of server information
        """
        try:
            client = cs_client.get_authenticated_client()
            # Fallback: try other endpoints to get basic info
            localip_response = await client.get("/api/v1/config/localip")
            if localip_response.status_code == 200:
                version_data = {"version": "available", "api_status": "operational", "local_ip": localip_response.text}
            else:
                version_data = {"version": "unknown", "api_status": "limited"}
                
            # Add comprehensive server information
            server_info = {
                "cobalt_strike": {
                    "version": version_data,
                    "api_base_url": cs_client.base_url,
                    "health_status": "connected"
                },
                "mcp_server": {
                    "name": "Cobalt Strike API",
                    "authenticated": True,
                    "transport": "MCP",
                    "capabilities": [
                        "tools", "prompts", "resources"
                    ]
                },
                "api_endpoints": {
                    "base_url": cs_client.base_url,
                    "api_docs": f"{cs_client.base_url}/v3/api-docs",
                    "health_check": f"{cs_client.base_url}/api/v1/version",
                    "authentication": f"{cs_client.base_url}/api/auth/login"
                },
                "resources": {
                    "beacons": "cobalt-strike://beacons/active",
                    "server_info": "cobalt-strike://config/server-info",
                    "activity_logs": "cobalt-strike://logs/recent-activity",
                    "listeners": "cobalt-strike://listeners/active"
                }
            }

            response = await client.get("/api/v1/config/systeminformation")
            if response.status_code == 200:
                system_information = response.text
                server_info["cobalt_strike"]["system_information"] = system_information

            return json.dumps(server_info, indent=2)
        except Exception as e:
            return json.dumps({
                "error": "Exception occurred",
                "exception": str(e),
                "message": "Error while fetching server information"
            })

    @mcp_server.resource("cobalt-strike://logs/recent-activity")
    async def recent_activity_resource() -> str:
        """Get recent Cobalt Strike activity logs.
        
        Returns:
            JSON representation of recent activities
        """
        try:
            client = cs_client.get_authenticated_client()
            response = await client.get("/api/v1/tasks")
            if response.status_code == 200:
                tasks_data = response.json()
                
                # Process and limit task data
                recent_tasks = tasks_data[:50] if isinstance(tasks_data, list) else tasks_data
                
                activity_summary = {
                    "metadata": {
                        "timestamp": "recent",
                        "total_tasks_shown": len(recent_tasks) if isinstance(recent_tasks, list) else 1,
                        "total_tasks_available": len(tasks_data) if isinstance(tasks_data, list) else 1,
                        "note": "Limited to 50 most recent tasks for performance"
                    },
                    "activities": recent_tasks
                }
                
                return json.dumps(activity_summary, indent=2)
            else:
                return json.dumps({
                    "error": "Failed to fetch activity logs",
                    "status_code": response.status_code,
                    "message": "Unable to retrieve recent activity data"
                })
        except Exception as e:
            return json.dumps({
                "error": "Exception occurred",
                "exception": str(e),
                "message": "Error while fetching activity logs"
            })

    @mcp_server.resource("cobalt-strike://listeners/active")
    async def active_listeners_resource() -> str:
        """Get current active listeners in JSON format.
        
        Returns:
            JSON representation of all active listeners
        """
        try:
            client = cs_client.get_authenticated_client()
            response = await client.get("/api/v1/listeners")
            if response.status_code == 200:
                listeners_data = response.json()
                
                listener_summary = {
                    "metadata": {
                        "total_listeners": len(listeners_data) if isinstance(listeners_data, list) else 1,
                        "status": "active",
                        "last_updated": "real-time"
                    },
                    "listeners": listeners_data
                }
                
                return json.dumps(listener_summary, indent=2)
            else:
                return json.dumps({
                    "error": "Failed to fetch listeners",
                    "status_code": response.status_code,
                    "message": "Unable to retrieve listener data"
                })
        except Exception as e:
            return json.dumps({
                "error": "Exception occurred",
                "exception": str(e),
                "message": "Error while fetching listener data"
            })

    @mcp_server.resource("cobalt-strike://stats/dashboard")
    async def dashboard_stats_resource() -> str:
        """Get Cobalt Strike dashboard statistics and summary.
        
        Returns:
            JSON representation of dashboard statistics
        """
        try:
            client = cs_client.get_authenticated_client()
            
            # Fetch multiple endpoints for comprehensive stats
            endpoints = {
                "beacons": "/api/v1/beacons",
                "listeners": "/api/v1/listeners",
                "tasks": "/api/v1/tasks"
            }
            
            stats = {
                "dashboard": {
                    "timestamp": "real-time",
                    "status": "operational"
                }
            }
            
            # Gather statistics from each endpoint
            for name, endpoint in endpoints.items():
                try:
                    response = await client.get(endpoint)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list):
                            stats[name] = {
                                "count": str(len(data)),
                                "status": "available"
                            }
                        else:
                            stats[name] = {
                                "count": "1",
                                "status": "available"
                            }
                    else:
                        stats[name] = {
                            "count": "0",
                            "status": "unavailable",
                            "error_code": str(response.status_code)
                        }
                except Exception as endpoint_error:
                    stats[name] = {
                        "count": "0",
                        "status": "error",
                        "error": str(endpoint_error)
                    }
            
            return json.dumps(stats, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": "Exception occurred",
                "exception": str(e),
                "message": "Error while fetching dashboard statistics"
            })

    logger.info("Added MCP resources: beacons, server-info, activity-logs, listeners, dashboard-stats")