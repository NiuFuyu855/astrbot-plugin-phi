import os
import json

class Config:
    def __init__(self, plugin_dir):
        self.config_dir = os.path.join(plugin_dir, "config")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "config": {
                "autoOpenApi": True,
                "openPhiPluginApi": True,
                "rejectPhiPluginApi": False
            }
        }
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        if not os.path.exists(self.config_file):
            self.save_config(self.default_config)
            self.config = self.default_config
        else:
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                self.config = self.default_config
    
    def save_config(self, config):
        """保存配置文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_user_cfg(self, section, key):
        """获取用户配置"""
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return None
    
    def modify(self, section, key, value):
        """修改配置"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config(self.config)
