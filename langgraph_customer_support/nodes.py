"""图节点定义"""

from langchain.messages import HumanMessage, SystemMessage

from langgraph_customer_support.llm import llm
from langgraph_customer_support.prompts import SYSTEM_PROMPT
from langgraph_customer_support.state import State


def categorize(state: State) -> dict:
    """将客户问题分类为：技术支持、账单问题或一般咨询。"""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"请将以下客户问题分类为以下类别之一：技术支持、账单问题、一般咨询。问题：{state['query']}"
        ),
    ]
    category = llm.invoke(messages).content
    return {"category": category}


def analyze_sentiment(state: State) -> dict:
    """分析客户问题的情感倾向：积极、中性或消极。"""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f'请分析以下客户问题的情感倾向，只回答"积极"、"中性"或"消极"。问题：{state["query"]}'
        ),
    ]
    sentiment = llm.invoke(messages).content
    return {"sentiment": sentiment}


def handle_technical(state: State) -> dict:
    """提供技术支持回复。"""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"请为以下问题提供技术支持回复。问题：{state['query']}"),
    ]
    response = llm.invoke(messages).content
    return {"response": response}


def handle_billing(state: State) -> dict:
    """提供账单支持回复。"""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"请为以下问题提供账单相关的支持回复。问题：{state['query']}"
        ),
    ]
    response = llm.invoke(messages).content
    return {"response": response}


def handle_general(state: State) -> dict:
    """提供一般咨询回复。"""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"请为以下问题提供一般性的支持回复。问题：{state['query']}"
        ),
    ]
    response = llm.invoke(messages).content
    return {"response": response}


def escalate(state: State) -> dict:
    """因情感消极，将问题升级转交人工客服。"""
    return {"response": "该问题因情感消极已被升级转交人工客服处理。"}
