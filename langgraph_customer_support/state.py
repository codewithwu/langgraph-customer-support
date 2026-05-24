"""图状态定义"""

from typing import TypedDict


class State(TypedDict):
    """工作流状态，所有节点共享此数据结构。"""

    query: str  # 客户问题
    category: str  # 问题分类：技术支持、账单问题、一般咨询
    sentiment: str  # 情感倾向：积极、中性、消极
    response: str  # 回复内容
