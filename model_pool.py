import threading
from typing import List, Optional, Dict, Any
from model_resource import ModelResource, ModelType, ModelGroup

class ModelPool:
    """
    模型池，管理多个模型资源的分配和回收
    支持按类型筛选、负载均衡、健康检查等功能
    """
    
    def __init__(self):
        self.pool: List[ModelResource] = []
        self.lock = threading.RLock()  # 使用可重入锁，支持嵌套调用
        
    def add_model(self, model: ModelResource) -> None:
        """
        添加模型到池中
        
        Args:
            model: 模型资源对象
        """
        with self.lock:
            self.pool.append(model)
            print(f"✅ 添加模型: {model.model_name} ({model.model_type.value}, {model.model_group})")
    
    def remove_model(self, model_id: str) -> bool:
        """
        从池中移除模型
        
        Args:
            model_id: 模型ID
            
        Returns:
            是否成功移除
        """
        with self.lock:
            for i, model in enumerate(self.pool):
                if model.model_id == model_id:
                    removed = self.pool.pop(i)
                    print(f"🗑️ 移除模型: {removed.model_name} ({removed.model_type.value})")
                    return True
            return False
    
    def get_idle_model(self, task_type: Optional[ModelGroup] = None) -> Optional[ModelResource]:
        """
        获取空闲的模型，可选按类型筛选
        
        Args:
            model_type: 可选，指定模型类型
            
        Returns:
            空闲的模型资源，如果没有则返回 None
        """
        with self.lock:
            for model in self.pool:
                if model.is_idle():
                    if task_type is None or task_type=="" or model.model_group == task_type or model.model_group == ModelGroup.GROUP_HYBRID.value:
                        return model
            return None

    def get_model_by_id(self, model_id: str) -> Optional[ModelResource]:
        """
        根据模型ID获取模型（不改变占用状态）
        
        Args:
            model_id: 模型ID
            
        Returns:
            模型资源，如果不存在则返回 None
        """
        with self.lock:
            for model in self.pool:
                if model.model_id == model_id:
                    return model
            return None
    
    def get_models_by_type(self, model_type: ModelType) -> List[ModelResource]:
        """
        获取指定类型的所有模型
        
        Args:
            model_type: 模型类型
            
        Returns:
            该类型的所有模型列表
        """
        with self.lock:
            return [m for m in self.pool if m.model_type == model_type]
    
    def occupy_model(self, model_id: str, agent_id: int) -> bool:
        """
        占用指定模型
        
        Args:
            model_id: 模型ID
            agent_id: 占用的代理ID
            
        Returns:
            是否成功占用
        """
        with self.lock:
            model = self.get_model_by_id(model_id)
            if model and model.occupy(agent_id):
                print(f"🔒 占用模型: {model.model_name} (Agent: {agent_id})")
                return True
            return False
    
    def release_model(self, model_id: str) -> bool:
        """
        释放指定模型
        
        Args:
            model_id: 模型ID
            
        Returns:
            是否成功释放
        """
        with self.lock:
            for model in self.pool:
                if model.model_id == model_id:
                    agent_id = model.bind_agent_id
                    model.release()
                    print(f"🔓 释放模型: {model.model_name} (Agent: {agent_id})")
                    return True
            return False
    
    def release_all_models(self) -> int:
        """
        释放所有被占用的模型
        
        Returns:
            释放的模型数量
        """
        with self.lock:
            released_count = 0
            for model in self.pool:
                if not model.is_idle():
                    model.release()
                    released_count += 1
            print(f"🔓 释放了 {released_count} 个模型")
            return released_count
    
    def get_idle_count(self) -> int:
        """
        获取空闲模型数量
        
        Args:
            model_type: 可选，指定模型类型
            
        Returns:
            空闲模型数量
        """
        with self.lock:
            count = 0
            for m in self.pool:
                if m.is_idle():
                    count += m.max_threads
            return count
    
    def get_busy_count(self, model_type: Optional[ModelType] = None) -> int:
        """
        获取繁忙模型数量
        
        Args:
            model_type: 可选，指定模型类型
            
        Returns:
            繁忙模型数量
        """
        with self.lock:
            if model_type:
                return sum(1 for m in self.pool if not m.is_idle() and m.model_type == model_type)
            return sum(1 for m in self.pool if not m.is_idle())
    
    def get_total_count(self, model_type: Optional[ModelType] = None) -> int:
        """
        获取模型总数
        
        Args:
            model_type: 可选，指定模型类型
            
        Returns:
            模型总数
        """
        with self.lock:
            if model_type:
                return sum(1 for m in self.pool if m.model_type == model_type)
            return len(self.pool)
    
    def list_all_models(self) -> List[ModelResource]:
        """
        获取所有模型的列表（副本）
        
        Returns:
            所有模型列表的副本
        """
        with self.lock:
            return self.pool.copy()
    
    def get_pool_status(self) -> Dict[str, Any]:
        """
        获取池状态摘要
        
        Returns:
            包含池统计信息的字典
        """
        with self.lock:
            total = len(self.pool)
            idle = self.get_idle_count()
            busy = total - idle
            
            # 按类型统计
            type_stats = {}
            for model in self.pool:
                type_name = model.model_type.value
                if type_name not in type_stats:
                    type_stats[type_name] = {"total": 0, "idle": 0, "busy": 0}
                type_stats[type_name]["total"] += 1
                if model.is_idle():
                    type_stats[type_name]["idle"] += 1
                else:
                    type_stats[type_name]["busy"] += 1
            
            return {
                "total": total,
                "idle": idle,
                "busy": busy,
                "by_type": type_stats,
                "models": [
                    {
                        "id": m.model_id,
                        "name": m.model_name,
                        "type": m.model_type.value,
                        "status": "idle" if m.is_idle() else f"busy (agent: {m.bind_agent_id})",
                        "stats": m.get_stats() if hasattr(m, 'get_stats') else None
                    }
                    for m in self.pool
                ]
            }
    
    def print_pool_status(self) -> None:
        """打印池状态信息"""
        status = self.get_pool_status()
        print("\n" + "="*50)
        print(f"📊 模型池状态")
        print("="*50)
        print(f"总数: {status['total']} | 空闲: {status['idle']} | 繁忙: {status['busy']}")
        print("-"*50)
        
        if status['by_type']:
            print("按类型统计:")
            for type_name, stats in status['by_type'].items():
                print(f"  • {type_name}: 总数={stats['total']}, 空闲={stats['idle']}, 繁忙={stats['busy']}")
        
        print("-"*50)
        print("模型详情:")
        for model_info in status['models']:
            print(f"  • {model_info['name']} ({model_info['type']}): {model_info['status']}")
        print("="*50 + "\n")
    
    def clear_pool(self) -> int:
        """
        清空模型池
        
        Returns:
            清空的模型数量
        """
        with self.lock:
            count = len(self.pool)
            self.pool.clear()
            print(f"🧹 清空模型池，移除了 {count} 个模型")
            return count
    
