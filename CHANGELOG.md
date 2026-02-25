# 将 phi-plugin 转换为 AstrBot 插件

## 1. 项目结构搭建

### 1.1 创建基本文件结构
- `main.py` - 插件主文件，包含插件类和所有指令处理
- `metadata.yaml` - 插件元数据信息
- `requirements.txt` - 依赖管理文件
- `data/` - 数据存储目录
  - `userdata/` - 用户数据
  - `cache/` - 缓存数据
  - `backup/` - 备份文件
- `utils/` - 工具函数
  - `phigros_api.py` - Phigros API 调用
  - `data_manager.py` - 数据管理
  - `image_generator.py` - 图片生成
  - `game_manager.py` - 游戏管理

## 2. 核心功能实现

### 2.1 基础架构
- 创建 `PhiPlugin` 类继承自 `Star` 基类
- 使用 `@register` 装饰器注册插件
- 实现 `__init__` 方法初始化插件
- 实现 `terminate` 方法处理插件卸载

### 2.2 指令系统
- 使用 `@filter.command` 装饰器注册所有指令
- 实现以下核心指令：
  - `phi help` - 获取帮助
  - `phi bind` - 绑定 sessionToken
  - `phi unbind` - 解绑 sessionToken
  - `phi update` - 更新存档
  - `phi rks` - 查询 RKS
  - `phi score` - 查询单曲成绩
  - `phi suggest` - 获取推分建议
  - `phi rand` - 随机曲目
  - `phi guess` - 猜曲绘游戏
  - `phi ltr` - 开字母游戏
  - `phi tipgame` - 提示猜曲游戏
  - `phi song` - 查询曲目信息
  - `phi chart` - 查询谱面信息
  - `phi table` - 查询定数表
  - `phi sign` - 签到
  - `phi task` - 查看任务

### 2.3 数据管理
- 实现用户数据存储和管理
- 实现 sessionToken 管理
- 实现备份和还原功能
- 实现排行榜功能

### 2.4 游戏功能
- 实现猜曲绘游戏
- 实现开字母游戏
- 实现提示猜曲游戏
- 实现随机曲目功能
- 实现随机课题功能

### 2.5 工具函数
- 实现 Phigros API 调用
- 实现数据解析和处理
- 实现图片生成（如果需要）
- 实现消息处理和回复

## 3. 依赖管理

### 3.1 核心依赖
- `requests` - 网络请求
- `pyyaml` - YAML 解析
- `Pillow` - 图像处理（如果需要）
- `numpy` - 数据处理（如果需要）

### 3.2 依赖文件
创建 `requirements.txt` 文件，包含所有必要的依赖库

## 4. 插件配置

### 4.1 元数据配置
创建 `metadata.yaml` 文件，填写插件的元数据信息：
- 插件名称
- 作者
- 描述
- 版本
- 仓库地址
- 指令信息

### 4.2 配置项
- 指令前缀配置
- 数据存储路径配置
- API 配置

## 5. 测试和调试

### 5.1 功能测试
- 测试所有指令的功能
- 测试数据存储和读取
- 测试游戏功能
- 测试排行榜功能

### 5.2 性能优化
- 优化 API 调用
- 优化数据处理
- 优化图片生成（如果需要）

## 6. 部署和发布

### 6.1 安装说明
- 提供详细的安装步骤
- 提供依赖安装说明
- 提供配置说明

### 6.2 发布准备
- 确保所有功能正常工作
- 确保代码结构清晰
- 确保文档完整

## 7. 注意事项

### 7.1 兼容性
- 确保与 AstrBot 兼容
- 确保与不同平台兼容

### 7.2 安全性
- 确保 sessionToken 安全存储
- 确保数据传输安全

### 7.3 性能
- 确保插件运行流畅
- 确保资源使用合理

## 8. 预期成果

- 完整的 AstrBot 插件，实现与原始 phi-plugin 基本一致的功能
- 清晰的代码结构和文档
- 良好的用户体验
- 稳定的性能