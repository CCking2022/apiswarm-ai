import os
import threading
from typing import List
from task import Task
from agent_pool import AgentPool
from model_pool import ModelPool

class GlobalScheduler:
    def __init__(self, a_pool: AgentPool, model_pool: ModelPool):
        self.agent_pool = a_pool
        self.model_pool = model_pool
        self.task_queue: List[Task] = []
        self.finished_task_queue: List[Task] = []
        self.lock = threading.Lock()
        self.DEPENDENCY_ROOT = "output"

    def add_task(self, task: Task) -> None:
        with self.lock:
            self.task_queue.append(task)

    def dissmis_task(self, task: Task) -> None:
        #将任务从 task_queue 移动到 finished_task_queue
        #线程安全，确保任务存在且仅移动一次
        with self.lock:
            # 检查任务是否在待执行队列中
            if task in self.task_queue:
                # 从原队列移除
                self.task_queue.remove(task)
                # 添加到已完成队列
                self.finished_task_queue.append(task)
        
    def get_pending_task_count(self) -> int:
        # 初始化计数器
        pending_count = 0

        # 遍历任务队列统计状态
        for task in self.task_queue:
            if task.status == "pending":
                pending_count += 1

        return pending_count

    def get_running_task_count(self) -> int:
        running_count = 0
        # 遍历任务队列统计状态
        for task in self.task_queue:
            if task.status == "running":
                running_count += 1
        return running_count

    def get_tasks_info(self) -> str:
        # 线程安全：加锁保证统计过程中队列不被修改
        with self.lock:
            # 初始化计数器
            pending_count = 0
            running_count = 0
            finished_count = 0

            # 统计 待处理 + 执行中 任务（来自 task_queue）
            for task in self.task_queue:
                if task.status == "pending":
                    pending_count += 1
                elif task.status == "running":
                    running_count += 1

            # 统计 已完成 任务（来自 finished_task_queue）
            finished_count = len(self.finished_task_queue)

        # 按要求格式返回字符串
        return f"待处理: {pending_count} 个, 执行中: {running_count} 个, 已完成: {finished_count} 个"

    def get_tasks_can_start(self) -> List[Task]:
        """
        获取所有依赖文件都已存在的任务（线程安全）
        返回列表：所有dependency_files全部存在的任务
        """
        with self.lock:
            # 筛选符合条件的任务
            can_start_tasks = []

            for task in self.task_queue:
                # 跳过非待执行状态的任务
                if task.status != "pending":
                    continue
                # 检查所有依赖文件是否都存在
                all_deps_exist = True
                for dep_file in task.dependency_files:
                    # 拼接完整路径：output/相对路径
                    dep_full_path = os.path.join(self.DEPENDENCY_ROOT, dep_file)                    
                    if not os.path.isfile(dep_full_path):
                        all_deps_exist = False
                        break
                if all_deps_exist:
                    can_start_tasks.append(task)
            return can_start_tasks
        
