import os
import pytest
from src.utils import pdf_utils

SAMPLE_PATH = os.path.join("data", "sample", "sample.pdf")

@pytest.mark.skipif(not os.path.exists(SAMPLE_PATH), reason="示例 PDF 不存在，跳过基础测试")
def test_open_and_extract():
    pdf = pdf_utils.open_document(SAMPLE_PATH)
    assert pdf.page_count > 0
    text, needs_ocr = pdf_utils.extract_page_text(pdf, 0)
    assert isinstance(text, str)
    assert isinstance(needs_ocr, bool)
