import uuid
import time

class Task:
    def __init__(self, title: str, content: str, filepath: str, filename: str, tasktype: str, dependency_files: list, schedule_type="once"):
        self.task_id = f"task_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        self.title = title
        self.content = content
        self.filepath = filepath
        self.filename = filename
        self.tasktype = tasktype
        self.dependency_files = dependency_files # 列表格式，存储多个依赖文件
        self.schedule_type = schedule_type
        self.target_agent_id = None
        self.status = "pending"
        self.result = ""

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "content": self.content,
            "filepath": self.filepath, 
            "filename": self.filename,
            "tasktype": self.tasktype,
            "dependency_files": self.dependency_files, # 自动转成可序列化列表
            "schedule_type": self.schedule_type,
            "target_agent_id": self.target_agent_id,
            "status": self.status,
            "result": self.result
        }

    @staticmethod
    def from_dict(data):
        t = Task(
            title=data.get("title", ""),
            content=data.get("content", ""),
            filepath=data.get("filepath", ""), 
            filename=data.get("filename", ""),
            tasktype=data.get("tasktype",""),
            dependency_files=data.get("dependency_files", []),            
            schedule_type=data.get("schedule_type", "once"),
        )
        t.task_id = data.get("task_id", t.task_id)
        t.target_agent_id = data.get("target_agent_id")
        t.status = data.get("status", "pending")
        t.result = data.get("result", "")
        return t
