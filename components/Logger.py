import logging
import os

class Logger:
    def __init__(self, plugin_dir):
        self.logger = logging.getLogger("phi-plugin")
        self.logger.setLevel(logging.INFO)
        
        # 创建日志目录
        log_dir = os.path.join(plugin_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建文件处理器
        log_file = os.path.join(log_dir, "phi-plugin.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def mark(self, message):
        """标记信息"""
        self.logger.info(message)
    
    def error(self, message):
        """错误信息"""
        self.logger.error(message)
    
    def warning(self, message):
        """警告信息"""
        self.logger.warning(message)
    
    def debug(self, message):
        """调试信息"""
        self.logger.debug(message)
