from __future__ import annotations
from typing import Protocol, Optional
from dataclasses import dataclass
import os
from tenacity import retry, stop_after_attempt, wait_exponential, wait_fixed
from src.config import Settings, get_settings

try:
    import google.generativeai as genai
except ImportError:  # allow missing during initial install
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

class LLMProvider(Protocol):
    def generate_structured(self, prompt: str) -> str: ...

@dataclass
class GeminiProvider:
    api_key: str
    model_name: str = "gemini-2.5-pro"

    def __post_init__(self):
        if genai:
            genai.configure(api_key=self.api_key)
            # 配置网络优化
            import os
            os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(0.5))  # 快速重试，减少等待
    def generate_structured(self, prompt: str) -> str:
        if not genai:
            return "未安装 google-generativeai 包，请先安装依赖。"
        
        # 网页版 Gemini 同等速度配置
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,     # 最快速度设置
            top_p=0.95,
            top_k=40,
            max_output_tokens=800,    # 限制输出，提升速度
            candidate_count=1,        # 只生成一个候选
            stop_sequences=[],        # 无停止序列
        )
        
        # 添加安全设置，避免被过滤导致延迟
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # 添加超时设置，避免网络卡住
        try:
            response = model.generate_content(
                prompt,
                request_options={'timeout': 30}  # 30秒超时
            )
        except Exception as e:
            # 网络问题时的友好提示
            if "timeout" in str(e).lower() or "network" in str(e).lower():
                return "网络连接超时，请检查网络或稍后重试。如果问题持续，建议切换到其他模型。"
            raise
        return response.text or "(模型未返回文本)"

@dataclass
class EnterpriseGatewayProvider:
    url: str
    key: Optional[str]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def generate_structured(self, prompt: str) -> str:
        # Placeholder: adapt to enterprise internal API spec
        import requests
        headers = {"Authorization": f"Bearer {self.key}"} if self.key else {}
        payload = {"prompt": prompt, "format": "markdown"}
        resp = requests.post(self.url.rstrip("/") + "/v1/generate", json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("text") or data.get("output") or "(网关未返回文本)"


@dataclass 
class ClaudeProvider:
    api_key: str
    model_name: str = "claude-3-5-sonnet-20241022"
    _client: Optional[object] = None

    def __post_init__(self):
        if anthropic and not self._client:
            try:
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except Exception:
                self._client = None

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(0.1))
    def generate_structured(self, prompt: str) -> str:
        if not anthropic:
            return "未安装 anthropic 包，请运行: pip install anthropic"
        
        if not self._client:
            try:
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                return f"Claude 初始化失败: {type(e).__name__}: {str(e)}"
        
        try:
            resp = self._client.messages.create(
                model=self.model_name,
                max_tokens=800,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text or "(模型未返回文本)"
        except Exception as e:
            raise


@dataclass
class SiliconFlowProvider:
    api_key: str
    model_name: str = "Qwen/QwQ-32B-Preview"
    _client: Optional[object] = None

    def __post_init__(self):
        if OpenAI and not self._client:
            try:
                # 硅基流动使用兼容 OpenAI 的接口
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.siliconflow.cn/v1",
                    timeout=30
                )
            except Exception:
                self._client = None

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(0.1))
    def generate_structured(self, prompt: str) -> str:
        if not OpenAI:
            return "未安装 openai 包"
        
        if not self._client:
            try:
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.siliconflow.cn/v1",
                    timeout=30
                )
            except Exception as e:
                return f"硅基流动初始化失败: {type(e).__name__}: {str(e)}"
        
        try:
            resp = self._client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个中文AI助手，必须用中文回答所有问题。绝对不要用英文回答。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,    # 快速响应
                max_tokens=800,     # 限制输出长度
                top_p=0.8,
            )
            content = resp.choices[0].message.content
            return content or "(模型未返回文本)"
        except Exception as e:
            # 提供更详细的错误信息
            return f"硅基流动API调用失败: {type(e).__name__}: {str(e)}\n\n可能原因:\n1. 模型名称不正确: {self.model_name}\n2. API Key权限问题\n3. 网络连接问题\n\n请检查硅基流动控制台的模型列表"


@dataclass
class QwenProvider:
    api_key: str
    model_name: str = "qwen-plus"
    _client: Optional[object] = None

    def __post_init__(self):
        if OpenAI and not self._client:
            try:
                # 通义千问使用兼容 OpenAI 的接口
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                )
            except Exception:
                self._client = None

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(0.2))
    def generate_structured(self, prompt: str) -> str:
        if not OpenAI:
            return "未安装 openai 包"
        
        if not self._client:
            try:
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                )
            except Exception as e:
                return f"Qwen 初始化失败: {type(e).__name__}: {str(e)}"
        
        try:
            resp = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=800,
                top_p=0.8,
            )
            content = resp.choices[0].message.content
            return content or "(模型未返回文本)"
        except Exception as e:
            raise


@dataclass
class DeepSeekProvider:
    api_key: str
    model_name: str = "deepseek-chat"
    _client: Optional[object] = None

    def __post_init__(self):
        if OpenAI and not self._client:
            try:
                # DeepSeek 使用兼容 OpenAI 的接口
                self._client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
            except Exception:
                self._client = None

    @retry(stop=stop_after_attempt(1), wait=wait_fixed(0.1))  # 几乎无重试延迟，追求速度
    def generate_structured(self, prompt: str) -> str:
        if not OpenAI:
            return "## 错误\n未安装 openai 包。"
        
        if not self._client:
            try:
                self._client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
            except Exception as e:
                return f"## DeepSeek 初始化失败\n\n{type(e).__name__}: {str(e)}"
        
        try:
            resp = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,    # 最低随机性，最快速度
                max_tokens=500,     # 大幅限制输出长度，追求速度
                top_p=0.9,          # 优化参数
                frequency_penalty=0, # 减少重复，提升效率
                presence_penalty=0,  # 优化生成速度
            )
            content = resp.choices[0].message.content
            return content or "(模型未返回文本)"
        except Exception as e:
            raise


@dataclass
class OpenAIProvider:
    api_key: str
    model_name: str = "gpt-4o-mini"
    _client: Optional[object] = None

    def __post_init__(self):
        if OpenAI and not self._client:
            try:
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                # Fallback: set client to None and handle in generate_structured
                self._client = None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def generate_structured(self, prompt: str) -> str:
        if not OpenAI:
            return (
                "## 错误\n未安装 openai 包。\n\n"
                "请运行：`pip install openai`"
            )
        
        if not self._client:
            # Retry initialization if it failed before
            try:
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                return f"## OpenAI 初始化失败\n\n错误：{type(e).__name__}: {str(e)}\n\n请检查 API Key 和网络连接。"
        
        try:
            resp = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            content = resp.choices[0].message.content
            return content or "(模型未返回文本)"
        except Exception as e:
            raise


def get_llm_provider(settings: Optional[Settings] = None) -> LLMProvider:
    s = settings or get_settings()
    # 优先级：企业网关 > 硅基流动 > Qwen > Claude > DeepSeek > Gemini > OpenAI
    if s.ENTERPRISE_GATEWAY_URL:
        return EnterpriseGatewayProvider(url=s.ENTERPRISE_GATEWAY_URL, key=s.ENTERPRISE_GATEWAY_KEY)
    
    # 硅基流动 (国内访问，多模型支持，性价比高)
    if s.USE_SILICONFLOW and s.SILICONFLOW_API_KEY:
        return SiliconFlowProvider(api_key=s.SILICONFLOW_API_KEY, model_name=s.SILICONFLOW_MODEL_NAME)
    
    # 通义千问 Qwen (国内访问稳定，速度快)
    if s.USE_QWEN and s.QWEN_API_KEY:
        return QwenProvider(api_key=s.QWEN_API_KEY, model_name=s.QWEN_MODEL_NAME)
    
    # Claude 配置 (最推荐用于文档解释)
    if s.USE_CLAUDE and s.CLAUDE_API_KEY:
        return ClaudeProvider(api_key=s.CLAUDE_API_KEY, model_name=s.CLAUDE_MODEL_NAME)
    
    # DeepSeek 独立配置
    if s.USE_DEEPSEEK and s.DEEPSEEK_API_KEY:
        return DeepSeekProvider(api_key=s.DEEPSEEK_API_KEY, model_name=s.DEEPSEEK_MODEL_NAME)
    
    # 兼容旧的配置方式：如果 OPENAI_MODEL_NAME 是 deepseek-chat
    if s.OPENAI_API_KEY and s.OPENAI_MODEL_NAME == "deepseek-chat":
        return DeepSeekProvider(api_key=s.OPENAI_API_KEY, model_name=s.OPENAI_MODEL_NAME)
    
    if s.GOOGLE_API_KEY:
        return GeminiProvider(api_key=s.GOOGLE_API_KEY, model_name=s.MODEL_NAME)
    if s.OPENAI_API_KEY:
        return OpenAIProvider(api_key=s.OPENAI_API_KEY, model_name=s.OPENAI_MODEL_NAME)
    return GeminiProvider(api_key="", model_name=s.MODEL_NAME)  # will produce fallback message

