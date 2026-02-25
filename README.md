# astrbot-plugin-phi

适用于 AstrBot 的 Phigros 信息查询插件，支持查询分数等信息统计，以及猜曲目等小游戏。

## 功能特性

- **核心查分功能**：查询 B30、RKS、个人信息等
- **曲目查询**：查询曲目信息、谱面详情、曲绘等
- **娱乐功能**：猜曲绘、开字母、提示猜曲等小游戏
- **管理功能**：备份恢复、设置别名、禁用功能等
- **排行榜**：查看 RKS 排行榜、查询排名等
- **任务系统**：签到、任务管理、Notes 转账等

## 安装说明

1. 在 AstrBot 插件目录下克隆本仓库：
   ```bash
   git clone --depth=1 https://github.com/Catrong/phi-plugin.git ./plugins/phi-plugin/
   ```

2. 进入插件目录并安装依赖：
   ```bash
   cd ./plugins/phi-plugin/
   pnpm install
   ```

3. **重要**：使用主人权限执行以下指令下载曲绘，否则相关曲绘将无法正常展示：
   ```
   phi下载曲绘
   ```

## 基本指令

以下指令前缀均为 `phi`，例如：`phi帮助`

### 用户功能
- `帮助` - 获取帮助
- `绑定 [token]` - 绑定 sessionToken（支持国服/国际服）
- `解绑` - 解绑 sessionToken
- `b30/rks/pgr` - 查询 B30 成绩
- `info` - 查询个人信息
- `score [曲目]` - 查询单曲成绩
- `data` - 获取 data 数量
- `rand [条件]` - 随机曲目
- `song [曲目]` - 查询曲目信息
- `chart [曲目] [难度]` - 查询谱面详情
- `table [定数]` - 查询定数表
- `ill [曲目]` - 查询曲绘
- `sign` - 签到获取 Notes
- `task` - 查看任务
- `retask` - 刷新任务
- `send [目标] [数量]` - 转账 Notes
- `jrrp` - 今日人品
- `tips` - 随机 tips

### 管理功能
- `备份` - 备份存档文件
- `恢复` - 从备份中恢复
- `设置别名 [原名] [别名]` - 设置歌曲别名
- `删除别名 [别名]` - 删除歌曲别名
- `下载曲绘` - 下载曲绘到本地
- `设置 [功能] [参数]` - 修改插件设置
- `更新插件` - 更新插件

## 注意事项

1. 使用前请确保已绑定有效的 sessionToken
2. 首次使用请先执行 `phi下载曲绘` 指令
3. 部分功能需要主人权限才能执行
4. 如遇到问题，请检查网络连接或查看插件日志

## 适配说明

本插件由 [Catrong/phi-plugin](https://github.com/Catrong/phi-plugin) 适配而来，专为 AstrBot 平台优化。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本插件！