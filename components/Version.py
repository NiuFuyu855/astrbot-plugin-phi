class Version:
    ver = "1.0.0"
    
    @staticmethod
    def get_version():
        """获取版本号"""
        return Version.ver
    
    @staticmethod
    def check_update():
        """检查更新"""
        # 这里可以实现版本检查逻辑
        return False
