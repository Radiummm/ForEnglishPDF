from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    GOOGLE_API_KEY: Optional[str] = None
    MODEL_NAME: str = "gemini-2.5-pro"
    ENTERPRISE_GATEWAY_URL: Optional[str] = None
    ENTERPRISE_GATEWAY_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    
    # DeepSeek 独立配置
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL_NAME: str = "deepseek-chat"
    USE_DEEPSEEK: bool = False  # 明确的开关
    
    # Claude 配置 (最推荐用于文档解释)
    CLAUDE_API_KEY: Optional[str] = None
    CLAUDE_MODEL_NAME: str = "claude-3-5-sonnet-20241022"
    USE_CLAUDE: bool = False
    
    # 通义千问 Qwen 配置 (国内访问稳定)
    QWEN_API_KEY: Optional[str] = None
    QWEN_MODEL_NAME: str = "qwen-plus"
    USE_QWEN: bool = False
    
    # 硅基流动 SiliconFlow 配置 (国内访问，多模型支持)
    SILICONFLOW_API_KEY: Optional[str] = None
    SILICONFLOW_MODEL_NAME: str = "Qwen/QwQ-32B-Preview"
    USE_SILICONFLOW: bool = False

    # Pydantic v2 style configuration
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> "Settings":
    return Settings()


# 添加清除缓存的函数
def clear_settings_cache():
    get_settings.cache_clear()
