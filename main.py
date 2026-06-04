from model_engine import ModelEngine
from agent_pool import AgentPool
from global_scheduler import GlobalScheduler
from model_pool import ModelPool
from model_resource import ModelResource, ModelType
from agent import Agent
from task import Task
from logger import logger
from dotenv import load_dotenv  # 如果用 .env 文件需要这个
import os
import time
import random
import psutil
import threading
import shutil
from emailbot import EmailBot
import yaml
from typing import Dict, Any, Optional



LONG_CHECK_INTERVAL = 5
SHORT_CHECK_INTERVAL = 0.1
TASK_FOLDER = "tasks"
CPU_LIMIT = 80
MAX_AGENT_LIMIT = 100
stop_flag = False
agent_id_counter = 1
DEPENDENCY_ROOT = "output"

# 全局核心实例
model_engine = ModelEngine()
agent_pool = AgentPool()
model_pool = ModelPool()

# 全局调度器
global_scheduler = GlobalScheduler(agent_pool, model_pool)


# 加载环境变量（推荐：会自动读取项目根目录的 .env 文件）
load_dotenv()

def resolve_env(value):
    """
    解析环境变量
    支持格式：
    - env::VAR_NAME
    - ${VAR_NAME}
    - $VAR_NAME
    """
    if isinstance(value, str):
        # 格式1: env::VAR_NAME
        if value.startswith("env::"):
            env_key = value[5:]
            return os.getenv(env_key)
        # 格式2: ${VAR_NAME}
        elif value.startswith("${") and value.endswith("}"):
            env_key = value[2:-1]
            return os.getenv(env_key)
        # 格式3: $VAR_NAME
        elif value.startswith("$"):
            env_key = value[1:]
            return os.getenv(env_key)
    return value


def resolve_nested_env(obj):
    """递归解析嵌套对象中的环境变量"""
    if isinstance(obj, dict):
        return {k: resolve_nested_env(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_nested_env(item) for item in obj]
    else:
        return resolve_env(obj)


def load_config(config_path: str = "config.yaml"): 
    """
    从 YAML 配置文件加载所有配置
    自动处理环境变量（env::XXX、${XXX}、$XXX）
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        包含所有配置的字典
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 递归解析环境变量
    config = resolve_nested_env(config)
        
    # 加载模型配置
    defaults_config = config.get("model_pool", {}).get("defaults", {})
    models_config = config.get("model_pool", {}).get("models", [])
    
    for m in models_config:
        # 合并默认配置
        final_config = {**defaults_config, **m}
        
        try:
            # 转换 model_type 字符串为枚举
            model_type_str = final_config.get("model_type")
            model_type = ModelType[model_type_str] if model_type_str in ModelType.__members__ else None
            
            if model_type is None:
                print(f"⚠️ 警告: 未知的模型类型 '{model_type_str}'，跳过模型 {final_config.get('model_id')}")
                continue
            
            # 创建 ModelResource 对象（支持所有新参数）
            model = ModelResource(
                model_id=final_config.get("model_id"),
                model_name=final_config.get("model_name"),
                model_type=model_type,
                api_key=final_config.get("api_key"),
                endpoint=final_config.get("endpoint"),
                temperature=final_config.get("temperature", 0.7),
                max_tokens=final_config.get("max_tokens", 2000),
                top_p=final_config.get("top_p", 1.0),
                frequency_penalty=final_config.get("frequency_penalty", 0.0),
                presence_penalty=final_config.get("presence_penalty", 0.0),
                timeout=final_config.get("timeout", 60),
                system_prompt=final_config.get("system_prompt", None),
                disable_proxy=final_config.get("disable_proxy", False),
                max_threads=final_config.get("max_threads", 1),
                model_group=final_config.get("model_group"),
                extra_config={k: v for k, v in final_config.items() 
                             if k not in ["model_id", "model_name", "model_type", "api_key", 
                                        "endpoint", "temperature", "max_tokens", "top_p",
                                        "frequency_penalty", "presence_penalty", "timeout",
                                        "system_prompt", "disable_proxy","max_threads","model_group"]}
            )
            model_pool.add_model(model)
            print(f"✅ 加载模型: {model.model_name} ({model.model_type.value})")
            
        except Exception as e:
            print(f"❌ 加载模型失败 {final_config.get('model_id')}: {e}")
    
    # 返回完整配置
    return {
        # 邮箱配置
        "imap_server": config.get("imap", {}).get("server"),
        "imap_port": config.get("imap", {}).get("port"),
        "smtp_server": config.get("smtp", {}).get("server"),
        "smtp_port": config.get("smtp", {}).get("port"),
        "email_address": config.get("email", {}).get("bee_address"),
        "email_password": config.get("email", {}).get("bee_password"),
        "master_email": config.get("email", {}).get("master_email"),
        
        # 检查间隔
        "check_min": config.get("check", {}).get("min_interval", 3),
        "check_max": config.get("check", {}).get("max_interval", 8),
        
        # 任务目录
        "task_dir": config.get("task", {}).get("dir", "tasks")
    } 

# 保留原有MD任务解析、文件移动函数
def read_tasks_from_md(task_file_path):
    if not os.path.exists(task_file_path):
        return []
    with open(task_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    tasks = []
    current_task = None
    multiline_key = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("---"):
            continue
        if line.startswith("## 任务"):
            if current_task is not None:
                tasks.append(current_task)
            current_task = {}
            current_task["依赖文件"] = []
            multiline_key = None
            continue
        if line.startswith("- **") and "：" in line:
            if current_task is None:
                continue
            line = line.lstrip("- ").strip()
            key_part, value = line.split("：", 1)
            key = key_part.replace("**", "").strip()

            # ✅ 禁止把“依赖文件”解析成字符串
            if key == "依赖文件":
                multiline_key = "依赖文件"
                continue
            
            current_task[key] = value.strip()
            multiline_key = key if key in ["任务要求"] else None
            continue
        if multiline_key and current_task is not None and line:
            # 如果是依赖文件，按列表存储
            if multiline_key == "依赖文件":
                # 去掉可能的引号，加入列表
                clean_line = line.strip().strip('"').strip("'")
                current_task["依赖文件"].append(clean_line)
            else:
                # 普通多行字段（接口/编程要求）
                current_task[multiline_key] += "\n" + line
    if current_task is not None:
        tasks.append(current_task)
    return tasks

def move_file_rename_if_exists(src_file, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    filename = os.path.basename(src_file)
    name, ext = os.path.splitext(filename)
    count = 1
    dst_file = os.path.join(dst_dir, filename)
    while os.path.exists(dst_file):
        dst_file = os.path.join(dst_dir, f"{name}_{count}{ext}")
        count += 1
    shutil.move(src_file, dst_file)
    return dst_file

def _save_task_result(task, result):
    # 创建任务输出目录
    output_dir = DEPENDENCY_ROOT
    cleaned_filepath = task.filepath.strip()
    if cleaned_filepath:
        final_file_dir = os.path.join(output_dir, cleaned_filepath)
    else:
        final_file_dir = output_dir  # 不拼接子目录

    # 自动创建目录
    os.makedirs(final_file_dir, exist_ok=True)

    # 处理文件名：为空则用默认名
    cleaned_filename = task.filename.strip()
    if not cleaned_filename:
        filename = f"task_{task.task_id}_result.md"
    else:
        filename = cleaned_filename

    final_file_path = os.path.join(final_file_dir, filename)
        
    # 生成结果文件
    with open(final_file_path, "w", encoding="utf-8") as f:
        f.write(f"{result}")

def scan_and_dispatch(email_bot):
    global stop_flag, agent_id_counter
    if stop_flag:
        return

    cpu_usage = 0
    memory_percent = 0
    try:    # 获取当前进程对象
        p = psutil.Process()
        # CPU检测单次采样，获取当前进程对应CPU核心占用率
        cpu_usage = p.cpu_percent(interval=0.1)

        # 获取系统内存信息
        memory = psutil.virtual_memory()
        # 内存占用百分比（直接可用）
        memory_percent = memory.percent
    except Exception:
        print(f"\n无法取得“CPU使用率”或“内存占用比例”\n")
 
    print(f"\n[监控] CPU使用率: {cpu_usage}%",f"内存占用比例：{memory_percent}%\n")
    if cpu_usage >= CPU_LIMIT:
        agent_pool.free_usless_agents()
        return
    print(f"\n[监控] 一共有{agent_pool.agent_count}只小蜜蜂在快乐地帮你干活\n")
    print(f"\n[监控] {global_scheduler.get_tasks_info()}\n")

    email_bot.system_status = f"CPU使用率: {cpu_usage}%\n内存占用比例：{memory_percent}%\n一共有{agent_pool.agent_count}只小蜜蜂在快乐地帮你干活\n{global_scheduler.get_tasks_info()}"

    # 扫描任务文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    task_dir = os.path.join(current_dir, TASK_FOLDER)
    task_done_dir = os.path.join(task_dir, "done")
    os.makedirs(task_done_dir, exist_ok=True)

    if os.path.exists(task_dir):
        files = [f for f in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, f)) and not f.startswith('.')]
        for filename in files:
            print(f"[新任务] 处理任务清单:{filename}")
            file_path = os.path.join(task_dir, filename)
            tlist = read_tasks_from_md(file_path)
            for idx, fields in enumerate(tlist, 1):
                taskNO = fields.get('任务编号', '')
                filepath = fields.get('文件存储路径', '')
                filename = fields.get('文件名', '')
                tasktype = fields.get('任务类型', '')
                dependency_files = fields.get("依赖文件", [])                
                prompt_content = f"任务要求：{fields.get('任务要求', '')}"
                task = Task(taskNO, f"{prompt_content}",filepath,filename,tasktype,dependency_files)
                global_scheduler.add_task(task)
            print(f"[新任务] 新增{len(tlist)}个任务\n")
            move_file_rename_if_exists(file_path, task_done_dir)

    # 三方资源匹配调度
    if not stop_flag:  
        # 每次匹配都检查CPU
        cpu_usage = 0
        try:    # 获取当前cpu_usage
            cpu_usage = psutil.cpu_percent(interval=0.1)
        except Exception:
            pass
        
        if cpu_usage >= CPU_LIMIT:
            return

        if global_scheduler.get_pending_task_count() <= 0:
            return

        if len(agent_pool.agents) > MAX_AGENT_LIMIT:
            return

        can_start_tasks = global_scheduler.get_tasks_can_start()
        if not can_start_tasks:
            return

        task = can_start_tasks.pop(0)
        idle_model = model_pool.get_idle_model(task.tasktype)
        if not idle_model:
            return

        # 无空闲Agent时，按需新建
        idle_agents = agent_pool.idle_agents()
        if not idle_agents:
            new_agent = Agent(agent_id_counter, model_engine, model_pool)
            #new_agent.start()
            agent_pool.register(new_agent)
            agent_id_counter += 1            

        idle_agents = agent_pool.idle_agents()
        agent = idle_agents[0]

        if not idle_model.occupy(agent.agent_id):
            return

        def on_task_done(agent, task, model, result, error=None):
            if error:
                # 异常情况
                task.status = "pending"  #"failed"
                task.result = f"异常：{str(error)}"

                print(f"[Error] Agent{agent.agent_id}:{task.title} 任务异常: {str(error)}\n")
                # 写入系统日志
                logger.log(
                    agent_id=agent.agent_id,
                    task_id=task.task_id,
                    model_type=model.model_type,
                    content="任务执行异常",
                    result=str(error),
                    status="failed"
                )
            else:
                # 正常完成
                global_scheduler.dissmis_task(task)
                task.result = result
                _save_task_result(task, result)
                
                print(f"Agent{agent.agent_id} 任务完成: {task.title}\n{result[:30]}...\n")
                # 写入系统日志
                logger.log(
                    agent_id=agent.agent_id,
                    task_id=task.task_id,
                    model_type=model.model_type,
                    content=f"标题：{task.title}\n保存到：\\output\\{task.filepath}\\{task.filename}\n",
                    result=f"{result[:300]}...\n",
                    status="success"
                )
            if agent.current_model_id:
                agent.model_pool.release_model(agent.current_model_id)
            agent.current_model_id = None
            agent.is_idle = True
            
        try:
            model_engine._cleanup_finished_threads()
        except Exception as e:
            print(f"清理时出错: {e}")

        threading.Thread(
            target=agent.execute_task,
            args=(task, idle_model, on_task_done),  # 👈 传入回调
            daemon=True
        ).start()
    
def monitor_loop(email_bot):
    global stop_flag
    while not stop_flag:
        scan_and_dispatch(email_bot)
        if stop_flag:
            break
        can_start_tasks = global_scheduler.get_tasks_can_start()
        if not can_start_tasks:
            time.sleep(LONG_CHECK_INTERVAL)
        else:
            time.sleep(SHORT_CHECK_INTERVAL)

def email_bot_loop(email_bot):
    global stop_flag
    print("初始化邮件机器人")
    
    while not stop_flag:
        try:
            email_bot.check_emails()  # 收邮件 + 处理命令
        except Exception as e:
            print(f"⚠️邮件收取异常: {str(e)}")
        
        # 动态等待：不定时随机
        interval = email_bot.get_current_interval()
        for _ in range(interval):
            if stop_flag:
                return
            time.sleep(1)

def main():
    global stop_flag

    print("===== 全局双向资源调度系统启动 =====")
    cfg = load_config()

    #创建1个邮件服务器
    email_bot = EmailBot(cfg)

    # 启动线程1：系统定时调度
    t1 = threading.Thread(target=monitor_loop, args=(email_bot,), daemon=True)
    # 启动线程2：邮件机器人（随机间隔）
    t2 = threading.Thread(target=email_bot_loop, args=(email_bot,), daemon=True)

    t1.start()
    t2.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        print("\n🛑 正在停止调度系统...\n")
        
        # ✅ 等待线程结束
        print("等待监控线程结束...\n")
        t1.join(timeout=10)
        print("等待邮件线程结束...\n")
        t2.join(timeout=10)
        
        # 在等待任务完成时，添加进度显示
        print("等待正在执行的任务完成...")
        timeout = 30
        start_time = time.time()
        last_count = -1

        while global_scheduler.get_running_task_count() > 0 and time.time() - start_time < timeout:
            current_count = global_scheduler.get_running_task_count()
            if current_count != last_count:
                print(f"  还有 {current_count} 个任务正在执行...")
                last_count = current_count
            time.sleep(1)

        if global_scheduler.get_running_task_count() > 0:
            print(f"⚠️ 超时，仍有 {global_scheduler.get_running_task_count()} 个任务未完成")
        else:
            print("✅ 所有任务已完成")
    
if __name__ == "__main__":
    main()
