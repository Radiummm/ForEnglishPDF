import streamlit as st
from pathlib import Path
from src.config import get_settings, clear_settings_cache
from src.services.llm_client import get_llm_provider
from src.utils import pdf_utils
from src.utils.cache_utils import PageCache

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 1rem;
    }
    .chat-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
    }
    .pdf-container {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">PDF 阅读与对话</h1>', unsafe_allow_html=True)

settings = get_settings()
cache = PageCache()

# 校验是否已上传
pdf_path = st.session_state.get("pdf_path")
if not pdf_path:
    st.warning("请先上传 PDF 文件")
    if st.button("去上传文件", type="primary"):
        st.switch_page("pages/01_上传与配置.py")
    st.stop()

page_count = st.session_state.get("page_count", 0)
doc_hash = st.session_state.get("doc_hash", "")
domain = st.session_state.get("domain", "计算机")

llm = get_llm_provider(settings)

try:
    pdf_doc = pdf_utils.open_document(pdf_path)
except Exception as e:
    st.error(f"无法打开PDF: {e}")
    st.stop()

# 两列布局，左侧聊天，右侧PDF浏览器
col_chat, col_pdf = st.columns([1, 1])

with col_chat:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.subheader("AI 对话")
    
    # 会话历史
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # 使用 container 实现独立滚动
    chat_container = st.container(height=600)
    with chat_container:
        for role, content in st.session_state["chat_history"]:
            with st.chat_message(role):
                st.markdown(content)

    user_input = st.chat_input("输入问题...")
    st.markdown('</div>', unsafe_allow_html=True)
    if user_input:
        st.session_state["chat_history"].append(("user", user_input))
        with st.spinner("AI 回复中..."):
            try:
                answer = llm.generate_structured(user_input)
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                answer = f"❌ 调用失败\n\n**错误**: {type(e).__name__}: {str(e)}\n\n请检查 `.env` 配置和网络连接。\n\n详细：\n```\n{error_detail}\n```"
        st.session_state["chat_history"].append(("assistant", answer))
        st.rerun()

with col_pdf:
    st.markdown('<div class="pdf-container">', unsafe_allow_html=True)
    st.subheader("PDF 浏览器")
    st.caption(f"共 {page_count} 页 - 点击按钮发送该页内容到 AI")
    
    # PDF 页面浏览器：独立滚动容器
    pdf_container = st.container(height=600)
    with pdf_container:
        for i in range(page_count):
            col_btn, col_img = st.columns([1, 4])
            with col_btn:
                if st.button(f"发送\n第 {i+1} 页", key=f"send_{i}", use_container_width=True, type="secondary"):
                    page_text, needs_ocr = pdf_utils.extract_page_text(pdf_doc, i)
                    if needs_ocr:
                        page_img_temp = pdf_utils.render_page_image(pdf_doc, i)
                        ocr_text = pdf_utils.ocr_page_image(page_img_temp)
                        if len(ocr_text.strip()) > len(page_text.strip()):
                            page_text = ocr_text
                    
                    # 简化缓存键（不含翻译风格等）
                    cache_key = cache.make_key(doc_hash=doc_hash, page_index=i, 
                                               translation_style="", tech_depth="", glossary={})
                    cached = cache.get(cache_key)
                    
                    if cached:
                        st.session_state["chat_history"].append(("user", f"[发送第 {i+1} 页]"))
                        st.session_state["chat_history"].append(("assistant", cached))
                    else:
                        st.session_state["chat_history"].append(("user", f"[发送第 {i+1} 页]"))
                        with st.spinner(f"AI 分析第 {i+1} 页..."):
                            prompt = f"请帮我解释以下英文页面内容（领域：{domain}）：\n\n{page_text[:15000]}"
                            try:
                                result = llm.generate_structured(prompt)
                                cache.set(cache_key, result)
                            except Exception as e:
                                import traceback
                                error_detail = traceback.format_exc()
                                result = f"❌ 解析失败\n\n**错误类型**: {type(e).__name__}\n**错误信息**: {str(e)}\n\n请检查：\n1. `.env` 文件中是否配置了有效的 API Key\n2. 网络连接是否正常\n3. API Key 是否有效且未过期\n\n详细错误：\n```\n{error_detail}\n```"
                            st.session_state["chat_history"].append(("assistant", result))
                    st.rerun()
            
            with col_img:
                page_img = pdf_utils.render_page_image(pdf_doc, i)
                st.image(page_img, caption=f"第 {i+1} 页", use_column_width=True)
            
            st.divider()
    
    st.markdown('</div>', unsafe_allow_html=True)
