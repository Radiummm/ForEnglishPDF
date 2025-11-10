import streamlit as st
from pathlib import Path
import hashlib
from src.utils import pdf_utils

st.set_page_config(page_title="上传 PDF", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stSelectbox > div > div { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

st.title("PDF 上传")

st.subheader("1. 选择内容领域")
domain = st.selectbox("请选择文档领域", ["计算机", "数学", "物理", "经济", "医学", "其他"], index=0)
st.session_state["domain"] = domain

st.subheader("2. 上传 PDF 文件")
uploaded_file = st.file_uploader("选择 PDF 文件", type=["pdf"], accept_multiple_files=False)

if uploaded_file:
    with st.spinner("正在处理文件..."):
        uploads_dir = Path("data/uploads")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        save_path = uploads_dir / uploaded_file.name
        save_path.write_bytes(uploaded_file.read())

        # 基础信息存 Session
        st.session_state["pdf_path"] = str(save_path)
        pdf_doc = pdf_utils.open_document(str(save_path))
        st.session_state["page_count"] = pdf_doc.page_count
        st.session_state["doc_hash"] = hashlib.sha256(save_path.read_bytes()).hexdigest()[:16]
        
    st.success(f"文件上传成功：{uploaded_file.name} ({pdf_doc.page_count} 页)")
    
    if st.button("开始阅读", type="primary", use_container_width=True):
        st.switch_page("pages/02_阅读与对话.py")
