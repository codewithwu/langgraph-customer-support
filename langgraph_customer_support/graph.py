"""工作流图定义"""

from langgraph.graph import END, START, StateGraph

from langgraph_customer_support.nodes import (
    analyze_sentiment,
    categorize,
    escalate,
    handle_billing,
    handle_general,
    handle_technical,
)
from langgraph_customer_support.routes import route_query
from langgraph_customer_support.state import State

# 构建状态图
workflow = StateGraph(State)

# 注册节点
workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_technical", handle_technical)
workflow.add_node("handle_billing", handle_billing)
workflow.add_node("handle_general", handle_general)
workflow.add_node("escalate", escalate)

# 定义边
workflow.add_edge(START, "categorize")
workflow.add_edge("categorize", "analyze_sentiment")
workflow.add_conditional_edges(
    "analyze_sentiment",
    route_query,
    {
        "handle_technical": "handle_technical",
        "handle_billing": "handle_billing",
        "handle_general": "handle_general",
        "escalate": "escalate",
    },
)
workflow.add_edge("handle_technical", END)
workflow.add_edge("handle_billing", END)
workflow.add_edge("handle_general", END)
workflow.add_edge("escalate", END)

# 编译图
graph = workflow.compile()
