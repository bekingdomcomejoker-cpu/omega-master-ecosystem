"""GitHub connector for Omega Federation Router.

Handles repository search, commits, archival, and integration with
the OMEGA_SOVEREIGN_LEDGER for version control and audit trails.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pathlib import Path

from connectors_base import Connector
from bus_writer import append_jsonl, BUS_FILE, utc_now


class GitHubConnector(Connector):
    """GitHub API connector for repo operations."""

    def __init__(self, connector_id: str = "github", config: Optional[Dict[str, Any]] = None):
        super().__init__(connector_id, config or {})
        
        # Load config from file if available
        config_path = Path(__file__).parent.parent / "config" / "github_config.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                file_config = json.load(f)
                self.config.update(file_config.get("github", {}))
        
        self.api_token = self.config.get("api_token", "")
        self.api_url = self.config.get("api_url", "https://api.github.com")
        self.owner = self.config.get("owner", "")
        self.state = {
            "connected": bool(self.api_token),
            "last_operation": None,
            "rate_limit_remaining": None,
        }

    def health(self) -> Dict[str, Any]:
        """Check GitHub API availability."""
        if not self.api_token:
            return {
                "status": "offline",
                "connector_id": self.connector_id,
                "timestamp": utc_now(),
                "details": {"error": "No API token configured"},
            }

        try:
            import requests
            headers = {"Authorization": f"token {self.api_token}"}
            response = requests.get(f"{self.api_url}/user", headers=headers, timeout=5)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "status": "ok",
                    "connector_id": self.connector_id,
                    "timestamp": utc_now(),
                    "details": {
                        "user": user_data.get("login"),
                        "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
                    },
                }
            else:
                return {
                    "status": "degraded",
                    "connector_id": self.connector_id,
                    "timestamp": utc_now(),
                    "details": {"error": f"HTTP {response.status_code}"},
                }
        except Exception as e:
            return {
                "status": "offline",
                "connector_id": self.connector_id,
                "timestamp": utc_now(),
                "details": {"error": str(e)},
            }

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a GitHub operation."""
        action = payload.get("action", "search")
        
        if action == "search":
            return self._search_repos(payload)
        elif action == "get_commits":
            return self._get_commits(payload)
        elif action == "create_commit":
            return self._create_commit(payload)
        else:
            return {
                "status": "error",
                "connector_id": self.connector_id,
                "result": {"error": f"Unknown action: {action}"},
                "timestamp": utc_now(),
            }

    def _search_repos(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Search GitHub repositories."""
        try:
            import requests
            query = payload.get("query", "")
            headers = {"Authorization": f"token {self.api_token}"}
            
            response = requests.get(
                f"{self.api_url}/search/repositories",
                headers=headers,
                params={"q": query, "per_page": 10},
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                self.state["last_operation"] = "search"
                self.state["rate_limit_remaining"] = response.headers.get("X-RateLimit-Remaining")
                
                append_jsonl(
                    BUS_FILE,
                    {
                        "event": "github_search",
                        "connector_id": self.connector_id,
                        "query": query,
                        "results_count": len(data.get("items", [])),
                        "timestamp": utc_now(),
                    },
                )
                
                return {
                    "status": "ok",
                    "connector_id": self.connector_id,
                    "result": {
                        "total_count": data.get("total_count", 0),
                        "repositories": [
                            {
                                "name": repo.get("name"),
                                "url": repo.get("html_url"),
                                "stars": repo.get("stargazers_count"),
                            }
                            for repo in data.get("items", [])
                        ],
                    },
                    "timestamp": utc_now(),
                }
            else:
                return {
                    "status": "error",
                    "connector_id": self.connector_id,
                    "result": {"error": f"HTTP {response.status_code}"},
                    "timestamp": utc_now(),
                }
        except Exception as e:
            return {
                "status": "error",
                "connector_id": self.connector_id,
                "result": {"error": str(e)},
                "timestamp": utc_now(),
            }

    def _get_commits(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Get commits from a repository."""
        try:
            import requests
            repo = payload.get("repo", "")
            headers = {"Authorization": f"token {self.api_token}"}
            
            response = requests.get(
                f"{self.api_url}/repos/{self.owner}/{repo}/commits",
                headers=headers,
                params={"per_page": 10},
                timeout=10,
            )
            
            if response.status_code == 200:
                commits = response.json()
                self.state["last_operation"] = "get_commits"
                
                append_jsonl(
                    BUS_FILE,
                    {
                        "event": "github_get_commits",
                        "connector_id": self.connector_id,
                        "repo": repo,
                        "commit_count": len(commits),
                        "timestamp": utc_now(),
                    },
                )
                
                return {
                    "status": "ok",
                    "connector_id": self.connector_id,
                    "result": {
                        "commits": [
                            {
                                "sha": c.get("sha", "")[:8],
                                "message": c.get("commit", {}).get("message", ""),
                                "author": c.get("commit", {}).get("author", {}).get("name", ""),
                            }
                            for c in commits
                        ]
                    },
                    "timestamp": utc_now(),
                }
            else:
                return {
                    "status": "error",
                    "connector_id": self.connector_id,
                    "result": {"error": f"HTTP {response.status_code}"},
                    "timestamp": utc_now(),
                }
        except Exception as e:
            return {
                "status": "error",
                "connector_id": self.connector_id,
                "result": {"error": str(e)},
                "timestamp": utc_now(),
            }

    def _create_commit(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a commit in a repository (placeholder)."""
        return {
            "status": "ok",
            "connector_id": self.connector_id,
            "result": {"message": "Commit creation not yet implemented"},
            "timestamp": utc_now(),
        }

    def checkpoint(self) -> Dict[str, Any]:
        """Save GitHub connector state."""
        checkpoint = {
            "connector_id": self.connector_id,
            "state": self.state,
            "timestamp": utc_now(),
        }
        append_jsonl(BUS_FILE, checkpoint)
        return checkpoint
