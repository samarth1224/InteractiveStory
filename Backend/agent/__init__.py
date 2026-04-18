"""
Agent package for the Interactive Story AI engine.

Sub-packages are imported lazily by the modules that need them
(primarily ``runner.py``) to avoid eagerly instantiating LLM agents
at import time.
"""
