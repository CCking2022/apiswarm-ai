import time
from enum import Enum
from typing import Optional, Dict, Any

class ModelGroup(Enum):
    """大模型业务分组常量类"""
    GROUP_LITERATURE = "LITERATURE"        # 文学创作组：剧本、小说、文案、故事创作
    GROUP_PROGRAMMING = "PROGRAMMING"      # 程序编程组：代码编写、调试、算法、架构开发
    GROUP_HYBRID = "HYBRID"                # 综合全能组：所有复合型需求
    GROUP_LONG_TEXT = "LONG_TEXT"          # 长文本处理组：超大文档精读、内容汇总分析
    GROUP_LIGHT_WEIGHT = "LIGHT_WEIGHT"    # 轻量交互组：日常对话、图文音视频快速交互

class ModelType(Enum):
    """支持的大模型类型枚举"""
    
    # 本地部署
    OLLAMA = "ollama"
    
    # 国内主流大模型
    ALIYUN_DASHSCOPE = "aliyun"       # 阿里百炼平台
    VOLC_ARK = "volc"                 # 火山方舟（豆包）
    ZHIPU = "zhipu"                   # 智谱AI（GLM系列）
    BAIDU_WENXIN = "baidu_wenxin"     # 百度文心一言
    TENCENT_HUNYUAN = "tencent_hunyuan"  # 腾讯混元
    MOONSHOT = "moonshot"             # 月之暗面（Kimi）
    DEEPSEEK = "deepseek"             # 深度求索（DeepSeek）
    MINIMAX = "minimax"               # MiniMax（abab系列）
    NVIDIA = "nvidia"                 # NVIDIA NIM
    STEPFUN = "stepfun"               # 阶跃星辰
    LINGYI = "lingyi"                 # 零一万物（Yi系列）
    
    # 国外主流大模型
    OPENAI = "openai"                 # OpenAI（GPT系列）
    ANTHROPIC = "anthropic"           # Anthropic（Claude系列）
    GOOGLE = "google"                 # Google（Gemini系列）
    COHERE = "cohere"                 # Cohere
    MISTRAL = "mistral"               # Mistral AI
    GROQ = "groq"                     # Groq（超快推理）
    PERPLEXITY = "perplexity"         # Perplexity
    TOGETHER = "together"             # Together AI
    REPLICATE = "replicate"           # Replicate
    FIREWORKS = "fireworks"           # Fireworks AI
    
    # 开源部署方案（OpenAI兼容接口）
    VLLM = "vllm"                     # vLLM 部署
    LOCALAI = "localai"               # LocalAI 部署
    TGI = "tgi"                       # Hugging Face TGI
    LLAMACPP = "llamacpp"             # llama.cpp 服务器
    
    # 云平台
    AZURE_OPENAI = "azure_openai"     # Azure OpenAI
    GCP_VERTEX = "gcp_vertex"         # Google Cloud Vertex AI
    
    # 其他
    DIFY = "dify"                     # Dify 平台
    FASTCHAT = "fastchat"             # FastChat
    ANYSCALE = "anyscale"             # Anyscale


class ModelResource:
    """
    模型资源类，封装大模型的配置信息
    
    支持 OpenAI 兼容接口的参数：
    - temperature: 温度参数 (0-2)，控制随机性
    - max_tokens: 最大生成token数
    - top_p: 核采样参数 (0-1)
    - frequency_penalty: 频率惩罚 (-2 到 2)
    - presence_penalty: 存在惩罚 (-2 到 2)
    - timeout: 请求超时时间（秒）
    - system_prompt: 系统提示词
    - disable_proxy: 是否禁用代理（国内服务常用）
    """
    
    def __init__(self, 
                 model_id: str, 
                 model_name: str, 
                 model_type: ModelType,
                 api_key: str = None, 
                 endpoint: str = None,
                 # 新增可选参数 - 与 model_engine.py 配套
                 temperature: float = 0.7,
                 max_tokens: int = 2000,
                 top_p: float = 1.0,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0,
                 timeout: int = 60,
                 system_prompt: str = None,
                 disable_proxy: bool = False,
                 max_threads:int = 1,
                 model_group:ModelGroup = ModelGroup.GROUP_HYBRID,
                 # 扩展参数字典（用于特殊配置）
                 extra_config: Dict[str, Any] = None):
        
        # 基础配置
        self.model_id = model_id
        self.model_name = model_name
        self.model_type = model_type
        self.api_key = api_key
        self.endpoint = endpoint
        
        # OpenAI 兼容参数（与 model_engine.py 配套）
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.timeout = timeout
        self.system_prompt = system_prompt
        self.disable_proxy = disable_proxy
        self.max_threads = max_threads
        self.model_group = model_group
        
        # 扩展配置（用于特殊模型的特定参数）
        self.extra_config = extra_config or {}
        
        # 资源管理
        self.is_busy = False
        self.bind_agent_id = None
        self.create_time = time.time()
        
        # 统计信息（可选）
        self.total_calls = 0
        self.success_calls = 0
        self.failed_calls = 0
        self.last_error = None

    def occupy(self, agent_id: int) -> bool:
        """占用模型资源"""
        if self.is_busy:
            return False
        if self.max_threads<=0:
            self.is_busy = True
            return False
        self.max_threads-=1
        if self.max_threads<=0:
            self.is_busy = True
        self.bind_agent_id = agent_id
        return True

    def release(self) -> None:
        if self.max_threads<=0:
            self.max_threads = 1
        else:
            self.max_threads+=1
        """释放模型资源"""
        self.is_busy = False
        self.bind_agent_id = None

    def is_idle(self) -> bool:
        """检查模型是否空闲"""
        return not self.is_busy

