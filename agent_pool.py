from typing import List
from agent import Agent

class AgentPool:
    def __init__(self):
        self.agents: List[Agent] = []

    def register(self, agent: Agent):
        self.agents.append(agent)

    def idle_agents(self) -> List[Agent]:
        return [ag for ag in self.agents if ag.is_free()]

    def free_usless_agents(self):
        idle_list = self.idle_agents()
        # 保留一半空闲Agent，避免频繁创建销毁
        keep_num = max(2, len(self.agents) // 2)
        need_remove = idle_list[keep_num:]
        for ag in need_remove:
            if ag in self.agents:
                self.agents.remove(ag)

    @property
    def agent_count(self):
        return len(self.agents)
