"""Connector abstraction layer for Omega Federation Router.

All connectors expose a unified interface:
- health(): Check connector availability
- execute(payload): Execute a request and return structured response
- checkpoint(): Save connector state to the runtime bus
- disconnect(): Clean up resources

This layer ensures all providers (Google Drive, GitHub, MikroTik, LLM, Termux)
behave consistently within the Omega permission gate framework.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Connector(ABC):
    """Base connector interface for Omega Federation Router."""

    def __init__(self, connector_id: str, config: Optional[Dict[str, Any]] = None):
        self.connector_id = connector_id
        self.config = config or {}
        self.state = {}

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Check connector availability and health status.
        
        Returns:
            {
                "status": "ok" | "degraded" | "offline",
                "connector_id": str,
                "timestamp": ISO8601,
                "details": {...}
            }
        """
        pass

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a request through this connector.
        
        Args:
            payload: Request payload with route, action, and parameters
            
        Returns:
            {
                "status": "ok" | "error",
                "connector_id": str,
                "result": {...},
                "timestamp": ISO8601
            }
        """
        pass

    @abstractmethod
    def checkpoint(self) -> Dict[str, Any]:
        """Save connector state to the runtime continuity spine.
        
        Returns:
            {
                "connector_id": str,
                "state": {...},
                "timestamp": ISO8601
            }
        """
        pass

    def disconnect(self) -> Dict[str, Any]:
        """Clean up resources. Override if needed.
        
        Returns:
            {"status": "disconnected", "connector_id": str}
        """
        return {"status": "disconnected", "connector_id": self.connector_id}
