import threading
from model_engine import ModelEngine
from model_pool import ModelPool
from logger import logger
import os

DEPENDENCY_ROOT = "output"

class Agent: 
    def __init__(self, agent_id: int, model_engine: ModelEngine, model_pool: ModelPool):
        self.agent_id = agent_id
        self.model_engine = model_engine
        self.model_pool = model_pool
        self.is_idle = True
        self.current_model_id = None

    def run(self):
        while True:
            pass

    def execute_task(self, task, model, callback):
        self.is_idle = False
        self.current_model_id = model.model_id
        task.status = "running"
        try:
            print(f"Agent{self.agent_id} 任务开始: {task.title}...\n")
            # 写入系统日志
            logger.log(
                agent_id=self.agent_id,
                task_id=task.task_id,
                model_type=model.model_type,
                content="开始执行任务",
                result=f"标题：{task.title}\n{task.content}",
                status="running"
            )
            prompt_str = task.content
            for dep_file in task.dependency_files:
                # 拼接完整路径：output/相对路径
                dep_full_path = os.path.join(DEPENDENCY_ROOT, dep_file)                    
                if os.path.isfile(dep_full_path):
                    with open(dep_full_path, "r", encoding="utf-8") as f:
                        all_text = f.read()  # 一次性读取所有内容
                    prompt_str += f"\n{dep_file}:\n" + all_text + "\n"
                print(f"{prompt_str}")        

            result = self.model_engine.call(model, prompt_str)
            if not result:
                callback(self,task,model,"","异常，返回为空")
            else:
                callback(self,task,model,result)
        except Exception as e:
            callback(self,task,model,"",e)


    def is_free(self):
        return self.is_idle
