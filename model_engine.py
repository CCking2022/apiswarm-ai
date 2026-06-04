import requests
import json
import time
from typing import Optional, Dict, Any
from model_resource import ModelResource, ModelType
import threading

class ModelEngine:
    """
    统一的大模型调用引擎
    支持 OpenAI 标准接口格式，覆盖国内外主流大模型
    """
    
    # 定义需要特殊处理的模型类型
    SPECIAL_MODELS = {
        ModelType.OLLAMA,           # Ollama 本地模型
        ModelType.COHERE,           # Cohere 使用自有格式
        ModelType.ANTHROPIC,        # Claude 需要特殊 headers
        ModelType.GOOGLE,           # Google Gemini 特殊格式（可选）
    }
    
    # OpenAI 兼容的模型（使用统一接口）
    OPENAI_COMPATIBLE = {
        ModelType.OPENAI,
        ModelType.ALIYUN_DASHSCOPE,
        ModelType.VOLC_ARK,
        ModelType.ZHIPU,
        ModelType.NVIDIA,
        ModelType.BAIDU_WENXIN,
        ModelType.TENCENT_HUNYUAN,
        ModelType.MOONSHOT,
        ModelType.DEEPSEEK,
        ModelType.MINIMAX,
        ModelType.MISTRAL,
        ModelType.GROQ,
        ModelType.PERPLEXITY,
        ModelType.TOGETHER,
        ModelType.VLLM,
        ModelType.LOCALAI,
        ModelType.TGI,
        ModelType.LLAMACPP,
        ModelType.DIFY,
        ModelType.AZURE_OPENAI,
    }

    def __init__(self):
        # 为每个线程/请求创建独立的连接池
        self.active_sessions = {}  # 存储活跃的session
        self.session_lock = threading.RLock()
        self.session_counter = 0
        
    def _get_session_for_thread(self):
        """为当前线程获取专属session（不会影响其他线程）"""
        thread_id = threading.current_thread().ident
        
        with self.session_lock:
            if thread_id not in self.active_sessions:
                session = requests.Session()
                # 配置：允许复用但限制数量
                adapter = requests.adapters.HTTPAdapter(
                    pool_connections=1,
                    pool_maxsize=1,
                    max_retries=0
                )
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                self.active_sessions[thread_id] = session
                self.session_counter += 1
                
                # 监控：如果session过多，打印警告但不清理
                if self.session_counter > 100:
                    print(f"⚠️ 警告：活跃session数 {self.session_counter}")
            
            return self.active_sessions[thread_id]
    
    def _cleanup_finished_threads(self):
        """清理已结束线程的session（只清理已经结束的）"""
        with self.session_lock:
            active_thread_ids = {t.ident for t in threading.enumerate()}
            finished_threads = []
            
            for thread_id in list(self.active_sessions.keys()):
                if thread_id not in active_thread_ids:
                    # 线程已结束，可以安全关闭session
                    try:
                        self.active_sessions[thread_id].close()
                    except:
                        pass
                    finished_threads.append(thread_id)
            
            for thread_id in finished_threads:
                del self.active_sessions[thread_id]
                self.session_counter -= 1
            
            if finished_threads:
                print(f"✅ 清理了 {len(finished_threads)} 个已完成线程的session")
    
    def call(self, model: ModelResource, prompt: str, max_retries: int = 3) -> str:
        """
        统一的模型调用方法
        
        Args:
            model: 模型资源对象
            prompt: 输入提示词
            max_retries: 最大重试次数
            
        Returns:
            模型返回的文本内容
        """
        
        # 记录调用开始
        start_time = time.time()
        
        try:
            # 特殊模型处理
            if model.model_type in self.SPECIAL_MODELS:
                result = self._call_special_model(model, prompt)
            else:
                # 标准 OpenAI 接口格式调用
                result = self._call_openai_compatible(model, prompt, max_retries)            
            return result
            
        except Exception as e:
            return str(e)
    
    def _call_openai_compatible(self, model: ModelResource, prompt: str, max_retries: int) -> str:
        """
        调用 OpenAI 兼容接口的模型
        适用模型：
        - 国外：OpenAI (GPT-4/GPT-3.5)、Azure OpenAI、Groq、Mistral AI、DeepSeek、Perplexity、Together AI
        - 国内：阿里云通义千问、智谱GLM、火山方舟、百度文心、腾讯混元、讯飞星火(部分)、MiniMax、月之暗面Kimi
        - 开源部署：vLLM、LocalAI、Text Generation Inference (TGI)
        """
        # 获取当前线程的专属session（不会影响其他线程）
        session = self._get_session_for_thread()
    
        headers = {
            "Authorization": f"Bearer {model.api_key}",
            "Content-Type": "application/json",
            "Connection": "close"
        }
        
        # 标准 OpenAI 格式请求体
        payload = {
            "model": model.model_name,
            "messages": [
                {"role": "system", "content": model.system_prompt} if model.system_prompt else None,
                {"role": "user", "content": prompt}
            ],
            "temperature": model.temperature,
            "max_tokens": model.max_tokens,
            "top_p": model.top_p,
            "frequency_penalty": model.frequency_penalty,
            "presence_penalty": model.presence_penalty,
            "stream": False,
            "user_id" : f"user_{threading.current_thread().ident}" 
        }
        # 移除 None 值
        payload["messages"] = [m for m in payload["messages"] if m is not None]
        
        # 特殊配置
        proxies = None
        timeout = model.timeout 
        
        # 国内服务或指定禁用代理的模型需要禁用代理
        if model.disable_proxy or model.model_type in [ModelType.VOLC_ARK, ModelType.ALIYUN_DASHSCOPE]:
            proxies = {"http": None, "https": None}
        
        # 重试机制
        for attempt in range(max_retries):
            response = None
            try:
                # 发送请求
                response = session.post(
                    model.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=timeout,
                    proxies=proxies
                )
                
                # 检查 HTTP 状态码
                response.raise_for_status()
                
                # 解析响应
                result = response.json()
                
                # 标准 OpenAI 格式解析
                if "choices" in result and len(result["choices"]) > 0:
                    message = result["choices"][0].get("message", {})
                    content = message.get("content", "")
                    
                    # 检查是否被拒绝
                    finish_reason = result["choices"][0].get("finish_reason")
                    if finish_reason == "content_filter":
                        print("⚠️ 内容被安全过滤器拦截\n")
                        return ""
                    elif finish_reason == "length":
                        print(f"⚠️ 输出被截断（达到 max_tokens={model.max_tokens} 限制）\n")
                    
                    return content.strip()
                
                # 部分国产模型返回格式略有差异
                elif "output" in result:
                    # 阿里云通义千问等
                    if "text" in result["output"]:
                        return result["output"]["text"].strip()
                    elif "choices" in result["output"]:
                        return result["output"]["choices"][0].get("text", "").strip()
                    else:
                        return str(result["output"]).strip()
                        
                elif "data" in result and "response" in result["data"]:
                    # 某些特殊格式
                    return result["data"]["response"].strip()
                    
                elif "text" in result:
                    # 简单格式
                    return result["text"].strip()
                    
                else:
                    print(f"⚠️ 未知的响应格式: {list(result.keys())}\n")
                    return ""
                    
            except requests.exceptions.ConnectionError as e:
                print(f"🔥 连接错误 (尝试 {attempt+1}/{max_retries}): {e}\n")
                if attempt == max_retries - 1:
                    print(f"❌ 无法连接到 {model.model_type.value} 服务，请检查网络和端点配置\n")
                    return ""
                time.sleep(2 ** attempt)  # 指数退避
                
            except requests.exceptions.Timeout:
                print(f"⏳ 请求超时 (尝试 {attempt+1}/{max_retries})\n")
                if attempt == max_retries - 1:
                    print(f"❌ {model.model_type.value} 请求超时，当前 timeout={model.timeout}秒，请适当增加\n")
                    return ""
                time.sleep(2 ** attempt)
                
            except requests.exceptions.HTTPError as e:
                status_code = response.status_code if 'response' in locals() else 0
                
                if status_code == 401:
                    print(f"🔑 API Key 无效或已过期，请检查 {model.model_type.value} 的认证信息\n")
                elif status_code == 403:
                    print(f"🚫 无权访问 {model.model_type.value}，请检查 API Key 权限\n")
                elif status_code == 404:
                    print(f"❓ 模型 '{model.model_name}' 不存在，请检查模型名称和 endpoint\n")
                elif status_code == 429:
                    print(f"📊 {model.model_type.value} 请求频率超限，请降低请求速度或升级套餐\n")
                    if attempt < max_retries - 1:
                        wait_time = min(5 * (2 ** attempt), 30)  # 最大等待30秒
                        print(f"⏰ 等待 {wait_time} 秒后重试...\n")
                        time.sleep(wait_time)
                        continue
                elif 500 <= status_code <= 599:
                    print(f"🔧 {model.model_type.value} 服务器错误 ({status_code})，可能是临时故障\n")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                else:
                    print(f"🔥 HTTP {status_code} 错误: {e}\n")
                
                if attempt == max_retries - 1:
                    return ""
                time.sleep(2 ** attempt)
                
            except json.JSONDecodeError as e:
                print(f"📄 响应解析失败 (尝试 {attempt+1}/{max_retries}): {e}\n")
                if 'response' in locals():
                    print(f"原始响应（前200字符）: {response.text[:200]}\n")
                if attempt == max_retries - 1:
                    return ""
                time.sleep(2 ** attempt)
                
            except Exception as e:
                print(f"💥 未知错误 (尝试 {attempt+1}/{max_retries}): {type(e).__name__}: {e}\n")
                if attempt == max_retries - 1:
                    print(f"❌ {model.model_type.value} 调用彻底失败，请检查配置\n")
                    return ""
                time.sleep(2 ** attempt)
            finally:
                # 关键：关闭响应，释放连接
                if response is not None:
                    response.close()
        return ""
    
    def _call_special_model(self, model: ModelResource, prompt: str) -> str:
        """
        处理不兼容 OpenAI 格式的特殊模型
        """
        if model.model_type == ModelType.OLLAMA:
            return self._call_ollama(model, prompt)
        elif model.model_type == ModelType.COHERE:
            return self._call_cohere(model, prompt)
        elif model.model_type == ModelType.ANTHROPIC:
            return self._call_anthropic(model, prompt)
        elif model.model_type == ModelType.GOOGLE:
            return self._call_google(model, prompt)
        else:
            print(f"⚠️ 未实现的特殊模型: {model.model_type.value}\n")
            return ""
    
    def _call_ollama(self, model: ModelResource, prompt: str) -> str:
        """Ollama 本地模型调用"""
        try:
            payload = {
                "model": model.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": model.temperature,
                    "num_predict": model.max_tokens,
                    "top_p": model.top_p,
                }
            }
            
            # 添加可选参数
            if hasattr(model, 'system_prompt') and model.system_prompt:
                payload["system"] = model.system_prompt
            
            endpoint = model.endpoint or "http://localhost:11434/api/generate"
            
            response = requests.post(
                endpoint,
                json=payload,
                timeout=model.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # 检查响应
            if "response" in result:
                return result["response"].strip()
            elif "message" in result and "content" in result["message"]:
                return result["message"]["content"].strip()
            else:
                print(f"⚠️ Ollama 未知响应格式: {list(result.keys())}\n")
                return ""
            
        except requests.exceptions.ConnectionError:
            print("🔥 Ollama 连接失败，请确认服务是否启动: ollama serve\n")
        except requests.exceptions.Timeout:
            print(f"⏳ Ollama 请求超时（{model.timeout}秒），模型可能推理较慢\n")
        except Exception as e:
            print(f"🔥 Ollama 错误: {e}\n")
        return ""
    
    def _call_cohere(self, model: ModelResource, prompt: str) -> str:
        """Cohere 模型调用（使用自有格式）"""
        try:
            payload = {
                "model": model.model_name,
                "message": prompt,
                "temperature": model.temperature,
                "max_tokens": model.max_tokens,
                "stream": False
            }
            
            # 添加 system prompt 如果存在
            if model.system_prompt:
                payload["preamble"] = model.system_prompt
            
            headers = {
                "Authorization": f"Bearer {model.api_key}",
                "Content-Type": "application/json"
            }
            
            endpoint = model.endpoint or "https://api.cohere.ai/v1/chat"
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=model.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # Cohere 返回格式
            if "text" in result:
                return result["text"].strip()
            elif "message" in result and "content" in result["message"]:
                return result["message"]["content"].strip()
            else:
                print(f"⚠️ Cohere 未知响应格式: {list(result.keys())}\n")
                return ""
            
        except Exception as e:
            print(f"🔥 Cohere 错误: {e}\n")
        return ""
    
    def _call_anthropic(self, model: ModelResource, prompt: str) -> str:
        """Anthropic Claude 模型调用（特殊 headers）"""
        try:
            # 构建消息列表
            messages = []
            if model.system_prompt:
                # Claude 的 system prompt 在顶层参数中
                system = model.system_prompt
            else:
                system = None
            
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": model.model_name,
                "messages": messages,
                "max_tokens": model.max_tokens,
                "temperature": model.temperature,
                "top_p": model.top_p,
                "stream": False
            }
            
            # 添加 system prompt（Claude 特有）
            if system:
                payload["system"] = system
            
            headers = {
                "x-api-key": model.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            
            endpoint = model.endpoint or "https://api.anthropic.com/v1/messages"
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=model.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # Claude 返回格式
            if "content" in result and len(result["content"]) > 0:
                return result["content"][0].get("text", "").strip()
            else:
                print(f"⚠️ Claude 未知响应格式: {list(result.keys())}\n")
                return ""
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print("🔑 Claude API Key 无效\n")
            elif response.status_code == 429:
                print("📊 Claude 请求频率超限，请稍后重试\n")
            else:
                print(f"🔥 Claude HTTP 错误: {e}\n")
        except Exception as e:
            print(f"🔥 Anthropic 错误: {e}\n")
        return ""
    
    def _call_google(self, model: ModelResource, prompt: str) -> str:
        """Google Gemini 模型调用"""
        try:
            # Gemini API 格式
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": model.temperature,
                    "maxOutputTokens": model.max_tokens,
                    "topP": model.top_p,
                }
            }
            
            # 添加 system instruction（Gemini 1.5+）
            if model.system_prompt:
                payload["systemInstruction"] = {
                    "parts": [{"text": model.system_prompt}]
                }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Gemini 使用 API key 在 URL 参数中
            endpoint = model.endpoint or f"https://generativelanguage.googleapis.com/v1beta/models/{model.model_name}:generateContent"
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                params={"key": model.api_key},
                timeout=model.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # 解析 Gemini 响应
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
            
            print(f"⚠️ Gemini 未知响应格式: {list(result.keys())}\n")
            return ""
            
        except Exception as e:
            print(f"🔥 Google Gemini 错误: {e}\n")
        return ""
