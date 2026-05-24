"""LLM 实例"""

from langchain_agent.agents.base import get_singleton_client

from langgraph_customer_support.config import LLM_PROVIDER

llm = get_singleton_client(llm_provider=LLM_PROVIDER)
