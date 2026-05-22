# This file makes the app directory a Python package and re-exports the root agent
# so ADK tooling can discover it automatically.

from .agent import root_agent as agent

__all__ = ["agent"]
