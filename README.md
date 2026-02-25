# phi-plugin

适用于 AstrBot 的 Phigros 信息查询插件，支持查询分数等信息统计，以及猜曲目等小游戏。

## 功能

### 用户功能
- `/phi help` - 获取帮助
- `/phi bind <sessionToken>` - 绑定 sessionToken
- `/phi unbind` - 解绑 sessionToken
- `/phi clean` - 删除所有记录
- `/phi update` - 更新存档
- `/phi rks` - 查询 RKS
- `/phi x30` - 查询 1Good B30
- `/phi fc30` - 查询 FC B30
- `/phi info` - 查询个人统计信息
- `/phi lmtacc [0-100]` - 计算限制最低 ACC 后的 RKS
- `/phi lvscore <定数范围> <难度>` - 获取区间成绩
- `/phi chap <章节名称|help>` - 获取章节成绩
- `/phi list <-dif 定数范围> <-acc ACC范围> <EZ|HD|IN|AT> <NEW|C|B|A|S|V|FC|PHI>` - 获取区间每首曲目的成绩
- `/phi hisb30` - 根据历史记录计算 B30 变化情况
- `/phi best1 [+]` - 查询文字版 B30（或更多）
- `/phi score <曲名> [-dif 难度] [-or acc|score|fc|time] [-unrank]` - 获取单曲成绩
- `/phi suggest` - 获取可以让 RKS+0.01 的曲目及其所需 ACC
- `/phi ranklist [名次]` - 获取 RKS 排行榜
- `/phi rankfind <rks>` - 获取有多少人大于查询 RKS
- `/phi data` - 获取用户 data 数量
- `/phi guess` - 猜曲绘游戏
- `/phi ltr` - 开字母游戏
- `/phi tipgame` - 提示猜曲游戏
- `/phi song <曲名>` - 查询曲目信息
- `/phi chart <曲名> [难度=IN]` - 查询谱面信息
- `/phi tag <曲名> [难度=IN] <标签>` - 查看谱面标签
- `/phi settag <曲名> [难度=IN] <标签>` - 给谱面打标签
- `/phi comment <曲名> [难度=IN] <内容>` - 评论曲目
- `/phi recmt <评论ID>` - 查看并确认是否删评
- `/phi mycmt` - 查看自己的云端评论
- `/phi table <定数>` - 查询定数表
- `/phi new` - 查询更新的曲目
- `/phi tips` - 随机 tips
- `/phi jrrp` - 今日人品
- `/phi alias <曲名>` - 查询某一曲目的别名
- `/phi rand [定数] [难度]` - 随机曲目
- `/phi randclg [课题总值] [难度] ([曲目定数范围])` - 随机课题
- `/phi 曲绘 <曲名>` - 查询曲绘
- `/phi search <条件 值>` - 检索曲库中的曲目
- `/phi theme [0-2]` - 切换绘图主题
- `/phi sign` - 签到获取 Notes
- `/phi task` - 查看自己的任务
- `/phi retask` - 刷新任务
- `/phi send <目标> <数量>` - 送给目标 Note

### 管理功能
- `/phi backup [back]` - 备份存档文件
- `/phi restore` - 从备份中还原
- `/phi setnick <原名> ---> <别名>` - 设置歌曲别名
- `/phi delnick <别名>` - 删除歌曲别名
- `/phi 强制更新` - 强制更新插件

## 安装

1. 在 AstrBot 插件目录中克隆本仓库：
   ```bash
   cd AstrBot/data/plugins
   git clone https://github.com/Catrong/phi-plugin.git
   ```

2. 安装依赖：
   ```bash
   cd phi-plugin
   pip install -r requirements.txt
   ```

3. 重启 AstrBot，插件会自动加载。

## 配置

插件会在首次运行时自动创建必要的目录结构：
- `data/userdata/` - 存储用户数据
- `data/cache/` - 存储缓存数据
- `data/backup/` - 存储备份文件

## 使用说明

1. **绑定 sessionToken**：使用 `/phi bind <sessionToken>` 命令绑定你的 Phigros sessionToken。
2. **更新存档**：使用 `/phi update` 命令更新你的游戏存档。
3. **查询 RKS**：使用 `/phi rks` 命令查询你的 RKS 和 B30。
4. **玩游戏**：使用 `/phi guess`、`/phi ltr`、`/phi tipgame` 等命令玩游戏。
5. **其他功能**：根据需要使用其他命令。

## 注意事项

- 本插件需要有效的 Phigros sessionToken 才能查询个人数据。
- 部分功能需要网络连接才能正常使用。
- 如有问题，请在 GitHub Issues 中反馈。

## 贡献

欢迎提交 Pull Request 和 Issue 来帮助改进本插件！

## 许可证

MIT
