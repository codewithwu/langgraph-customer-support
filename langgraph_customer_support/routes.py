"""条件路由"""

from langgraph_customer_support.state import State


def route_query(state: State) -> str:
    """根据情感倾向和问题分类进行路由。"""
    if state["sentiment"] == "消极":
        return "escalate"
    elif state["category"] == "技术支持":
        return "handle_technical"
    elif state["category"] == "账单问题":
        return "handle_billing"
    else:
        return "handle_general"
