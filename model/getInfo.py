import os
import json

class GetInfo:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.info_dir = os.path.join(plugin_dir, "resources", "info")
    
    async def init(self):
        """初始化信息"""
        # 确保信息目录存在
        if not os.path.exists(self.info_dir):
            os.makedirs(self.info_dir)
        
        # 这里可以实现信息初始化逻辑
        # 例如加载曲目信息、定数表等
        pass
    
    def get_song_info(self, song_name):
        """获取曲目信息"""
        # 这里可以实现获取曲目信息的逻辑
        pass
    
    def get_chart_info(self, song_name, difficulty):
        """获取谱面信息"""
        # 这里可以实现获取谱面信息的逻辑
        pass

# 创建全局实例
plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
getInfo = GetInfo(plugin_dir)
