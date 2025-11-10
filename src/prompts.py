from typing import Dict

BASE_TEMPLATE = """
你是一个中文AI助手。请用简洁的中文解释这段英文内容，绝对不要用英文回答：

{page_text}

要求：
1. 必须用中文回答
2. 解释要简单易懂
3. 如果有专业术语，用中文解释其含义
""".strip()

DEPTH_MAPPING = {
    "入门": "面向初学者，降低术语密度，更多背景解释",
    "标准": "保持原文专业度，适度解释关键概念",
    "进阶": "面向有经验读者，保留技术深度，可补充推导或细节"
}

STYLE_MAPPING = {
    "直译": "尽可能保持原句结构与术语原貌，必要时补充括号解释",
    "意译": "关注语义与可读性，适度重组句子，避免冗长"
}

def build_page_prompt(page_text: str, translation_style: str = "", tech_depth: str = "",
                      glossary: Dict[str, str] = None, summary_mode: bool = False, domain: str = "计算机") -> str:
    # 大幅减少输入长度，追求最快速度
    return BASE_TEMPLATE.format(
        page_text=page_text[:2000]  # 减少到2000字符，大幅提升速度
    )
