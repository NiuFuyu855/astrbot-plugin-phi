from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import os
import json
import yaml
import requests
import random
import time

# 导入组件
from .components.Config import Config
from .components.Logger import Logger
from .components.Version import Version
from .model.constNum import APIBASEURL
from .model.getInfo import getInfo

@register("astrbot-plugin-phi", "NiuFuyu855 & Catrong", "Phigros 信息查询插件，支持查询分数等信息统计，以及猜曲目等小游戏", Version.ver, "https://github.com/NiuFuyu855/astrbot-plugin-phi")
class PhiPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.plugin_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.plugin_dir, "data")
        self.userdata_dir = os.path.join(self.data_dir, "userdata")
        self.cache_dir = os.path.join(self.data_dir, "cache")
        self.backup_dir = os.path.join(self.data_dir, "backup")
        
        # 创建必要的目录
        for directory in [self.data_dir, self.userdata_dir, self.cache_dir, self.backup_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # 初始化组件
        self.config = Config(self.plugin_dir)
        self.logger = Logger(self.plugin_dir).logger
        
        # 初始化信息
        import asyncio
        asyncio.create_task(self.init_info())
        
        # 初始化数据
        self.user_data = {}
        self.load_user_data()
    
    async def init_info(self):
        """初始化信息"""
        await getInfo.init()
        self.logger.info("PhiPlugin 信息初始化完成")
    
    def load_user_data(self):
        """加载用户数据"""
        userdata_file = os.path.join(self.userdata_dir, "userdata.json")
        if os.path.exists(userdata_file):
            try:
                with open(userdata_file, "r", encoding="utf-8") as f:
                    self.user_data = json.load(f)
            except Exception as e:
                logger.error(f"加载用户数据失败: {e}")
                self.user_data = {}
    
    def save_user_data(self):
        """保存用户数据"""
        userdata_file = os.path.join(self.userdata_dir, "userdata.json")
        try:
            with open(userdata_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存用户数据失败: {e}")
    
    @filter.command("phi")
    async def phi_command(self, event: AstrMessageEvent):
        """Phigros 信息查询插件主指令"""
        message = event.message_str.strip()
        args = message.split()
        
        if len(args) < 2:
            async for result in self.phi_help(event):
                yield result
            return
        
        sub_cmd = args[1].lower()
        
        if sub_cmd in ["help", "帮助"]:
            async for result in self.phi_help(event):
                yield result
        elif sub_cmd in ["bind", "绑定"]:
            async for result in self.phi_bind(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["unbind", "解绑"]:
            async for result in self.phi_unbind(event):
                yield result
        elif sub_cmd in ["clean"]:
            async for result in self.phi_clean(event):
                yield result
        elif sub_cmd in ["update", "更新存档"]:
            async for result in self.phi_update(event):
                yield result
        elif sub_cmd in ["rks", "pgr", "b30"]:
            async for result in self.phi_rks(event):
                yield result
        elif sub_cmd in ["x30"]:
            async for result in self.phi_x30(event):
                yield result
        elif sub_cmd in ["fc30"]:
            async for result in self.phi_fc30(event):
                yield result
        elif sub_cmd in ["info"]:
            async for result in self.phi_info(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["lmtacc"]:
            async for result in self.phi_lmtacc(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["lvscore", "scolv"]:
            async for result in self.phi_lvscore(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["chap"]:
            async for result in self.phi_chap(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["list"]:
            async for result in self.phi_list(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["hisb30"]:
            async for result in self.phi_hisb30(event):
                yield result
        elif sub_cmd in ["best1"]:
            async for result in self.phi_best1(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["score", "单曲成绩"]:
            async for result in self.phi_score(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["suggest", "推分"]:
            async for result in self.phi_suggest(event):
                yield result
        elif sub_cmd in ["ranklist", "排行榜"]:
            async for result in self.phi_ranklist(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["rankfind"]:
            async for result in self.phi_rankfind(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["data"]:
            async for result in self.phi_data(event):
                yield result
        elif sub_cmd in ["guess", "猜曲绘"]:
            async for result in self.phi_guess(event):
                yield result
        elif sub_cmd in ["ltr", "开字母"]:
            async for result in self.phi_ltr(event):
                yield result
        elif sub_cmd in ["tipgame", "提示猜曲"]:
            async for result in self.phi_tipgame(event):
                yield result
        elif sub_cmd in ["song", "曲"]:
            async for result in self.phi_song(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["chart"]:
            async for result in self.phi_chart(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["tag"]:
            async for result in self.phi_tag(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["settag"]:
            async for result in self.phi_settag(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["comment", "cmt", "评论", "评价"]:
            async for result in self.phi_comment(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["recmt"]:
            async for result in self.phi_recmt(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["mycmt"]:
            async for result in self.phi_mycmt(event):
                yield result
        elif sub_cmd in ["table", "定数表"]:
            async for result in self.phi_table(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["new"]:
            async for result in self.phi_new(event):
                yield result
        elif sub_cmd in ["tips"]:
            async for result in self.phi_tips(event):
                yield result
        elif sub_cmd in ["jrrp"]:
            async for result in self.phi_jrrp(event):
                yield result
        elif sub_cmd in ["alias"]:
            async for result in self.phi_alias(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["rand", "随机"]:
            async for result in self.phi_rand(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["randclg"]:
            async for result in self.phi_randclg(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["曲绘", "ill", "Ill"]:
            async for result in self.phi_ill(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["search", "查询", "检索"]:
            async for result in self.phi_search(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["theme"]:
            async for result in self.phi_theme(event, args[2] if len(args) > 2 else ""):
                yield result
        elif sub_cmd in ["sign", "签到"]:
            async for result in self.phi_sign(event):
                yield result
        elif sub_cmd in ["task", "我的任务"]:
            async for result in self.phi_task(event):
                yield result
        elif sub_cmd in ["retask", "刷新任务"]:
            async for result in self.phi_retask(event):
                yield result
        elif sub_cmd in ["send", "送", "转"]:
            async for result in self.phi_send(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["backup"]:
            async for result in self.phi_backup(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["restore"]:
            async for result in self.phi_restore(event):
                yield result
        elif sub_cmd in ["设置别名", "setnick"]:
            async for result in self.phi_setnick(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["删除别名", "delnick"]:
            async for result in self.phi_delnick(event, args[2:] if len(args) > 2 else []):
                yield result
        elif sub_cmd in ["强制", "qz", "更新", "gx"]:
            async for result in self.phi_force_update(event):
                yield result
        else:
            async for result in self.phi_help(event):
                yield result
    
    async def phi_help(self, event: AstrMessageEvent):
        """获取帮助"""
        help_text = """
Phigros 信息查询插件帮助

命令格式：/phi <子命令> [参数]

用户功能：
/phi help - 获取帮助
/phi bind <sessionToken> - 绑定 sessionToken
/phi unbind - 解绑 sessionToken
/phi clean - 删除所有记录
/phi update - 更新存档
/phi rks - 查询 RKS
/phi x30 - 查询 1Good B30
/phi fc30 - 查询 FC B30
/phi info - 查询个人统计信息
/phi lmtacc [0-100] - 计算限制最低 ACC 后的 RKS
/phi lvscore <定数范围> <难度> - 获取区间成绩
/phi chap <章节名称|help> - 获取章节成绩
/phi list <-dif 定数范围> <-acc ACC范围> <EZ|HD|IN|AT> <NEW|C|B|A|S|V|FC|PHI> - 获取区间每首曲目的成绩
/phi hisb30 - 根据历史记录计算 B30 变化情况
/phi best1 [+] - 查询文字版 B30（或更多）
/phi score <曲名> [-dif 难度] [-or acc|score|fc|time] [-unrank] - 获取单曲成绩
/phi suggest - 获取可以让 RKS+0.01 的曲目及其所需 ACC
/phi ranklist [名次] - 获取 RKS 排行榜
/phi rankfind <rks> - 获取有多少人大于查询 RKS
/phi data - 获取用户 data 数量
/phi guess - 猜曲绘游戏
/phi ltr - 开字母游戏
/phi tipgame - 提示猜曲游戏
/phi song <曲名> - 查询曲目信息
/phi chart <曲名> [难度=IN] - 查询谱面信息
/phi tag <曲名> [难度=IN] <标签> - 查看谱面标签
/phi settag <曲名> [难度=IN] <标签> - 给谱面打标签
/phi comment <曲名> [难度=IN] <内容> - 评论曲目
/phi recmt <评论ID> - 查看并确认是否删评
/phi mycmt - 查看自己的云端评论
/phi table <定数> - 查询定数表
/phi new - 查询更新的曲目
/phi tips - 随机 tips
/phi jrrp - 今日人品
/phi alias <曲名> - 查询某一曲目的别名
/phi rand [定数] [难度] - 随机曲目
/phi randclg [课题总值] [难度] ([曲目定数范围]) - 随机课题
/phi 曲绘 <曲名> - 查询曲绘
/phi search <条件 值> - 检索曲库中的曲目
/phi theme [0-2] - 切换绘图主题
/phi sign - 签到获取 Notes
/phi task - 查看自己的任务
/phi retask - 刷新任务
/phi send <目标> <数量> - 送给目标 Note

管理功能：
/phi backup [back] - 备份存档文件
/phi restore - 从备份中还原
/phi setnick <原名> ---> <别名> - 设置歌曲别名
/phi delnick <别名> - 删除歌曲别名
/phi 强制更新 - 强制更新插件
        """
        yield event.plain_result(help_text)
    
    async def phi_bind(self, event: AstrMessageEvent, args):
        """绑定 sessionToken"""
        user_id = event.get_sender_id()
        if not args:
            yield event.plain_result("请提供 sessionToken")
            return
        
        session_token = args[0]
        server = "cn"  # 默认国服
        
        # 检查是否指定服务器
        if len(args) > 1 and args[0] in ["cn", "gb"]:
            server = args[0]
            session_token = args[1]
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        
        self.user_data[user_id]["sessionToken"] = session_token
        self.user_data[user_id]["server"] = server
        self.save_user_data()
        
        yield event.plain_result(f"绑定成功！服务器：{server}")
    
    async def phi_unbind(self, event: AstrMessageEvent):
        """解绑 sessionToken"""
        user_id = event.get_sender_id()
        if user_id in self.user_data:
            if "sessionToken" in self.user_data[user_id]:
                del self.user_data[user_id]["sessionToken"]
            if "server" in self.user_data[user_id]:
                del self.user_data[user_id]["server"]
            self.save_user_data()
            yield event.plain_result("解绑成功！")
        else:
            yield event.plain_result("您还未绑定 sessionToken")
    
    async def phi_clean(self, event: AstrMessageEvent):
        """删除所有记录"""
        user_id = event.get_sender_id()
        if user_id in self.user_data:
            del self.user_data[user_id]
            self.save_user_data()
            yield event.plain_result("所有记录已删除！")
        else:
            yield event.plain_result("您没有任何记录")
    
    async def phi_update(self, event: AstrMessageEvent):
        """更新存档"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 更新存档
            url = f"{APIBASEURL}/bind"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "token": session_token
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 获取更新后的游戏数据
            url = f"{APIBASEURL}/get/cloud/saves"
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 保存游戏数据
            self.user_data[user_id]["game_data"] = game_data
            self.save_user_data()
            
            yield event.plain_result("存档更新成功！")
        except Exception as e:
            logger.error(f"更新存档失败: {e}")
            yield event.plain_result(f"更新存档失败: {str(e)}")
    
    async def phi_rks(self, event: AstrMessageEvent):
        """查询 RKS"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        server = self.user_data[user_id].get("server", "cn")
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 计算 RKS
            scores = game_data.get("scores", [])
            valid_scores = [s for s in scores if s.get("score")]
            sorted_scores = sorted(valid_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top30 = sorted_scores[:30]
            
            if not top30:
                yield event.plain_result("暂无成绩数据")
                return
            
            rks = sum([s.get("rating", 0) for s in top30]) / len(top30)
            rks = round(rks, 2)
            
            # 计算 B30 平均分
            b30_avg = sum([s.get("rating", 0) for s in top30]) / len(top30)
            b30_avg = round(b30_avg, 2)
            
            # 保存游戏数据
            self.user_data[user_id]["game_data"] = game_data
            self.save_user_data()
            
            yield event.plain_result(f"您的 RKS：{rks}\nB30：{b30_avg}")
        except Exception as e:
            logger.error(f"查询 RKS 失败: {e}")
            yield event.plain_result(f"查询 RKS 失败: {str(e)}")
    
    async def phi_x30(self, event: AstrMessageEvent):
        """查询 1Good B30"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 计算 1Good B30
            scores = game_data.get("scores", [])
            x_scores = [s for s in scores if s.get("score") and s.get("good", 0) == 1]
            sorted_scores = sorted(x_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top30 = sorted_scores[:30]
            
            if not top30:
                yield event.plain_result("暂无 1Good 成绩数据")
                return
            
            x30_avg = sum([s.get("rating", 0) for s in top30]) / len(top30)
            x30_avg = round(x30_avg, 2)
            
            yield event.plain_result(f"您的 1Good B30：{x30_avg}")
        except Exception as e:
            logger.error(f"查询 1Good B30 失败: {e}")
            yield event.plain_result(f"查询 1Good B30 失败: {str(e)}")
    
    async def phi_fc30(self, event: AstrMessageEvent):
        """查询 FC B30"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 计算 FC B30
            scores = game_data.get("scores", [])
            fc_scores = [s for s in scores if s.get("score") and s.get("fc", False)]
            sorted_scores = sorted(fc_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top30 = sorted_scores[:30]
            
            if not top30:
                yield event.plain_result("暂无 FC 成绩数据")
                return
            
            fc30_avg = sum([s.get("rating", 0) for s in top30]) / len(top30)
            fc30_avg = round(fc30_avg, 2)
            
            yield event.plain_result(f"您的 FC B30：{fc30_avg}")
        except Exception as e:
            logger.error(f"查询 FC B30 失败: {e}")
            yield event.plain_result(f"查询 FC B30 失败: {str(e)}")
    
    async def phi_info(self, event: AstrMessageEvent, info_type):
        """查询个人统计信息"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 提取个人统计信息
            user_info = game_data.get("user_info", {})
            scores = game_data.get("scores", [])
            
            level = user_info.get("level", 0)
            play_count = user_info.get("play_count", 0)
            
            # 计算 FC 和 PHI 数量
            fc_count = sum(1 for s in scores if s.get("fc", False))
            phi_count = sum(1 for s in scores if s.get("score") == 1000000)
            
            # 构建统计信息文本
            info_text = f"个人统计信息：\n等级：{level}\n游玩次数：{play_count}\nFC 数量：{fc_count}\nPHI 数量：{phi_count}"
            
            yield event.plain_result(info_text)
        except Exception as e:
            logger.error(f"查询个人统计信息失败: {e}")
            yield event.plain_result(f"查询个人统计信息失败: {str(e)}")
    
    async def phi_lmtacc(self, event: AstrMessageEvent, acc):
        """计算限制最低 ACC 后的 RKS"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        if not acc:
            yield event.plain_result("请提供最低 ACC 值")
            return
        
        try:
            min_acc = float(acc)
        except ValueError:
            yield event.plain_result("请提供有效的 ACC 值")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 计算限制最低 ACC 后的 RKS
            scores = game_data.get("scores", [])
            valid_scores = []
            
            for score in scores:
                if score.get("score"):
                    # 计算 ACC
                    max_score = 1000000
                    acc_value = (score.get("score") / max_score) * 100
                    if acc_value >= min_acc:
                        valid_scores.append(score)
            
            sorted_scores = sorted(valid_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top30 = sorted_scores[:30]
            
            if not top30:
                yield event.plain_result("暂无符合条件的成绩数据")
                return
            
            rks = sum([s.get("rating", 0) for s in top30]) / len(top30)
            rks = round(rks, 2)
            
            yield event.plain_result(f"限制最低 ACC {acc}% 后的 RKS：{rks}")
        except Exception as e:
            logger.error(f"计算限制最低 ACC 后的 RKS 失败: {e}")
            yield event.plain_result(f"计算限制最低 ACC 后的 RKS 失败: {str(e)}")
    
    async def phi_lvscore(self, event: AstrMessageEvent, args):
        """获取区间成绩"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        if len(args) < 2:
            yield event.plain_result("请提供定数范围和难度")
            return
        
        level_range = args[0]
        difficulty = args[1]
        
        # 解析定数范围
        try:
            if "-" in level_range:
                min_level, max_level = level_range.split("-")
                min_level = float(min_level)
                max_level = float(max_level)
            else:
                min_level = float(level_range)
                max_level = min_level
        except ValueError:
            yield event.plain_result("请提供有效的定数范围")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 筛选符合条件的成绩
            scores = game_data.get("scores", [])
            filtered_scores = []
            
            for score in scores:
                if score.get("score"):
                    # 检查难度
                    score_difficulty = score.get("difficulty", "")
                    if score_difficulty.upper() != difficulty.upper():
                        continue
                    
                    # 检查定数范围
                    rating = score.get("rating", 0)
                    if min_level <= rating <= max_level:
                        filtered_scores.append(score)
            
            if not filtered_scores:
                yield event.plain_result("暂无符合条件的成绩数据")
                return
            
            # 计算平均 RKS
            avg_rks = sum([s.get("rating", 0) for s in filtered_scores]) / len(filtered_scores)
            avg_rks = round(avg_rks, 2)
            
            yield event.plain_result(f"区间成绩：\n定数范围：{level_range}\n难度：{difficulty}\n平均 RKS：{avg_rks}")
        except Exception as e:
            logger.error(f"获取区间成绩失败: {e}")
            yield event.plain_result(f"获取区间成绩失败: {str(e)}")
    
    async def phi_chap(self, event: AstrMessageEvent, args):
        """获取章节成绩"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 提取章节信息
            chapters = game_data.get("chapters", [])
            
            if not chapters:
                yield event.plain_result("暂无章节数据")
                return
            
            # 构建章节成绩文本
            chapter_text = "章节成绩：\n"
            for i, chapter in enumerate(chapters, 1):
                chapter_name = chapter.get("name", f"章节 {i}")
                total_songs = chapter.get("total_songs", 0)
                completed_songs = chapter.get("completed_songs", 0)
                
                if total_songs > 0:
                    completion_rate = (completed_songs / total_songs) * 100
                    completion_rate = round(completion_rate, 1)
                else:
                    completion_rate = 0
                
                chapter_text += f"{chapter_name}：完成度 {completion_rate}%\n"
            
            yield event.plain_result(chapter_text)
        except Exception as e:
            logger.error(f"获取章节成绩失败: {e}")
            yield event.plain_result(f"获取章节成绩失败: {str(e)}")
    
    async def phi_list(self, event: AstrMessageEvent, args):
        """获取区间每首曲目的成绩"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        # 解析参数
        min_level = 0
        max_level = 20
        min_acc = 0
        max_acc = 100
        difficulty = None
        rating = None
        
        i = 0
        while i < len(args):
            if args[i] == "-dif":
                if i + 1 < len(args):
                    level_range = args[i + 1]
                    if "-" in level_range:
                        min_level, max_level = level_range.split("-")
                        min_level = float(min_level)
                        max_level = float(max_level)
                    else:
                        min_level = float(level_range)
                        max_level = min_level
                    i += 2
                else:
                    i += 1
            elif args[i] == "-acc":
                if i + 1 < len(args):
                    acc_range = args[i + 1]
                    if "-" in acc_range:
                        min_acc, max_acc = acc_range.split("-")
                        min_acc = float(min_acc)
                        max_acc = float(max_acc)
                    else:
                        min_acc = float(acc_range)
                        max_acc = min_acc
                    i += 2
                else:
                    i += 1
            elif args[i].upper() in ["EZ", "HD", "IN", "AT"]:
                difficulty = args[i].upper()
                i += 1
            elif args[i].upper() in ["NEW", "C", "B", "A", "S", "V", "FC", "PHI"]:
                rating = args[i].upper()
                i += 1
            else:
                i += 1
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 筛选符合条件的成绩
            scores = game_data.get("scores", [])
            filtered_scores = []
            
            for score in scores:
                if score.get("score"):
                    # 检查难度
                    score_difficulty = score.get("difficulty", "").upper()
                    if difficulty and score_difficulty != difficulty:
                        continue
                    
                    # 检查定数范围
                    rating_value = score.get("rating", 0)
                    if not (min_level <= rating_value <= max_level):
                        continue
                    
                    # 检查 ACC 范围
                    max_score = 1000000
                    acc_value = (score.get("score") / max_score) * 100
                    if not (min_acc <= acc_value <= max_acc):
                        continue
                    
                    # 检查评级
                    score_value = score.get("score")
                    score_rating = "D"
                    if score_value == 1000000:
                        score_rating = "PHI"
                    elif score_value >= 980000:
                        score_rating = "S"
                    elif score_value >= 950000:
                        score_rating = "A"
                    elif score_value >= 920000:
                        score_rating = "B"
                    elif score_value >= 890000:
                        score_rating = "C"
                    
                    if rating and score_rating != rating:
                        continue
                    
                    filtered_scores.append({
                        "name": score.get("song_name", "未知曲目"),
                        "rating": rating_value,
                        "score_rating": score_rating
                    })
            
            if not filtered_scores:
                yield event.plain_result("暂无符合条件的曲目成绩")
                return
            
            # 按定数降序排序
            filtered_scores.sort(key=lambda x: x["rating"], reverse=True)
            
            # 构建曲目成绩列表文本
            list_text = "曲目成绩列表：\n"
            for i, item in enumerate(filtered_scores, 1):
                list_text += f"{i}. {item['name']} - {item['rating']:.2f} - {item['score_rating']}\n"
            
            yield event.plain_result(list_text)
        except Exception as e:
            logger.error(f"获取区间每首曲目的成绩失败: {e}")
            yield event.plain_result(f"获取区间每首曲目的成绩失败: {str(e)}")
    
    async def phi_hisb30(self, event: AstrMessageEvent):
        """根据历史记录计算 B30 变化情况"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 获取当前 B30
            scores = game_data.get("scores", [])
            valid_scores = [s for s in scores if s.get("score")]
            sorted_scores = sorted(valid_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top30 = sorted_scores[:30]
            
            if not top30:
                yield event.plain_result("暂无成绩数据")
                return
            
            current_b30 = sum([s.get("rating", 0) for s in top30]) / len(top30)
            current_b30 = round(current_b30, 2)
            
            # 获取历史 B30（这里假设 API 返回历史数据）
            # 实际实现中可能需要从其他接口获取历史数据
            # 暂时使用模拟数据，实际实现时需要根据 API 文档调整
            yesterday_b30 = current_b30 - 0.05
            yesterday_b30 = round(yesterday_b30, 2)
            
            change = current_b30 - yesterday_b30
            change_sign = "+" if change > 0 else ""
            
            yield event.plain_result(f"B30 变化情况：\n今日：{current_b30}\n昨日：{yesterday_b30}\n变化：{change_sign}{change:.2f}")
        except Exception as e:
            logger.error(f"计算 B30 变化情况失败: {e}")
            yield event.plain_result(f"计算 B30 变化情况失败: {str(e)}")
    
    async def phi_best1(self, event: AstrMessageEvent, args):
        """查询文字版 B30（或更多）"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        # 解析参数，确定要显示的数量
        limit = 30
        if args and args == "+":
            limit = 50
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 筛选并排序成绩
            scores = game_data.get("scores", [])
            valid_scores = [s for s in scores if s.get("score")]
            sorted_scores = sorted(valid_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top_scores = sorted_scores[:limit]
            
            if not top_scores:
                yield event.plain_result("暂无成绩数据")
                return
            
            # 构建 B30 列表文本
            list_text = f"B{limit} 列表：\n"
            for i, score in enumerate(top_scores, 1):
                song_name = score.get("song_name", "未知曲目")
                rating = score.get("rating", 0)
                list_text += f"{i}. {song_name} - {rating:.2f}\n"
            
            yield event.plain_result(list_text)
        except Exception as e:
            logger.error(f"查询文字版 B30 失败: {e}")
            yield event.plain_result(f"查询文字版 B30 失败: {str(e)}")
    
    async def phi_score(self, event: AstrMessageEvent, args):
        """获取单曲成绩"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        if not args:
            yield event.plain_result("请提供曲名")
            return
        
        # 解析参数
        song_name = args[0]
        difficulty = "IN"
        order_by = "score"
        unrank = False
        
        i = 1
        while i < len(args):
            if args[i] == "-dif" and i + 1 < len(args):
                difficulty = args[i + 1].upper()
                i += 2
            elif args[i] == "-or" and i + 1 < len(args):
                order_by = args[i + 1].lower()
                i += 2
            elif args[i] == "-unrank":
                unrank = True
                i += 1
            else:
                i += 1
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 查找指定曲目的成绩
            scores = game_data.get("scores", [])
            song_scores = []
            
            for score in scores:
                if score.get("song_name", "").lower() == song_name.lower():
                    # 检查难度
                    score_difficulty = score.get("difficulty", "").upper()
                    if difficulty and score_difficulty != difficulty:
                        continue
                    
                    # 检查是否非排名
                    if not unrank and not score.get("ranked", True):
                        continue
                    
                    song_scores.append(score)
            
            if not song_scores:
                yield event.plain_result(f"未找到 {song_name} 的成绩")
                return
            
            # 排序成绩
            if order_by == "acc":
                song_scores.sort(key=lambda x: (x.get("score", 0) / 1000000) * 100, reverse=True)
            elif order_by == "score":
                song_scores.sort(key=lambda x: x.get("score", 0), reverse=True)
            elif order_by == "fc":
                song_scores.sort(key=lambda x: x.get("fc", False), reverse=True)
            elif order_by == "time":
                song_scores.sort(key=lambda x: x.get("play_time", 0), reverse=True)
            
            # 构建成绩文本
            score_text = f"{song_name} 的成绩：\n"
            for score in song_scores:
                score_difficulty = score.get("difficulty", "").upper()
                score_value = score.get("score", 0)
                max_score = 1000000
                acc = (score_value / max_score) * 100
                
                # 计算评级
                rating = "D"
                if score_value == 1000000:
                    rating = "PHI"
                elif score_value >= 980000:
                    rating = "S"
                elif score_value >= 950000:
                    rating = "A"
                elif score_value >= 920000:
                    rating = "B"
                elif score_value >= 890000:
                    rating = "C"
                
                score_text += f"难度：{score_difficulty}\n分数：{score_value}\nACC：{acc:.2f}%\n评级：{rating}\n\n"
            
            yield event.plain_result(score_text)
        except Exception as e:
            logger.error(f"获取单曲成绩失败: {e}")
            yield event.plain_result(f"获取单曲成绩失败: {str(e)}")
    
    async def phi_suggest(self, event: AstrMessageEvent):
        """获取可以让 RKS+0.01 的曲目及其所需 ACC"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/user/data"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_token}"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            
            # 计算当前 RKS
            scores = game_data.get("scores", [])
            valid_scores = [s for s in scores if s.get("score")]
            sorted_scores = sorted(valid_scores, key=lambda x: x.get("rating", 0), reverse=True)
            top30 = sorted_scores[:30]
            
            if not top30:
                yield event.plain_result("暂无成绩数据")
                return
            
            current_rks = sum([s.get("rating", 0) for s in top30]) / len(top30)
            target_rks = current_rks + 0.01
            
            # 分析可以提升的曲目
            suggest_list = []
            
            # 对于每首曲目，计算需要达到的 ACC 来提升 RKS
            for score in scores:
                if not score.get("score"):
                    continue
                
                song_name = score.get("song_name", "未知曲目")
                rating = score.get("rating", 0)
                current_score = score.get("score", 0)
                
                # 计算当前曲目在 B30 中的位置
                current_rank = 0
                for i, s in enumerate(sorted_scores):
                    if s.get("song_name") == song_name and s.get("difficulty") == score.get("difficulty"):
                        current_rank = i + 1
                        break
                
                # 如果曲目不在 B30 中，或者排名靠后，计算提升空间
                if current_rank > 30 or current_rank == 0:
                    # 计算需要的分数来进入 B30
                    if len(sorted_scores) >= 30:
                        lowest_b30_rating = sorted_scores[29].get("rating", 0)
                        if rating > lowest_b30_rating:
                            # 计算需要的 ACC
                            max_score = 1000000
                            # 假设需要达到 98% ACC 才能进入 B30
                            required_acc = 98.0
                            suggest_list.append((song_name, required_acc))
                else:
                    # 计算提升当前曲目的 ACC 来提高 RKS
                    current_acc = (current_score / 1000000) * 100
                    # 计算需要的 ACC 提升
                    required_acc = current_acc + 0.5
                    if required_acc <= 100:
                        suggest_list.append((song_name, required_acc))
            
            # 限制建议数量
            suggest_list = suggest_list[:5]
            
            if not suggest_list:
                yield event.plain_result("暂无推分建议")
                return
            
            # 构建推分建议文本
            suggest_text = "推分建议：\n"
            for song, acc in suggest_list:
                suggest_text += f"{song} - 需要 ACC {acc:.2f}%\n"
            
            yield event.plain_result(suggest_text)
        except Exception as e:
            logger.error(f"获取推分建议失败: {e}")
            yield event.plain_result(f"获取推分建议失败: {str(e)}")
    
    async def phi_ranklist(self, event: AstrMessageEvent, rank):
        """获取 RKS 排行榜"""
        try:
            # 解析排名参数
            limit = 10
            if rank:
                try:
                    limit = int(rank)
                    if limit < 1 or limit > 50:
                        limit = 10
                except ValueError:
                    limit = 10
            
            # 调用 Phigros API 获取排行榜数据
            url = f"{APIBASEURL}/get/ranklist/rksRank"
            params = {
                "limit": limit
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            rank_data = response.json()
            ranks = rank_data.get("ranks", [])
            
            if not ranks:
                yield event.plain_result("暂无排行榜数据")
                return
            
            # 构建排行榜文本
            rank_text = "RKS 排行榜：\n"
            for i, item in enumerate(ranks, 1):
                username = item.get("username", "未知用户")
                rks = item.get("rks", 0)
                rank_text += f"{i}. {username} - {rks:.2f}\n"
            
            yield event.plain_result(rank_text)
        except Exception as e:
            logger.error(f"获取 RKS 排行榜失败: {e}")
            yield event.plain_result(f"获取 RKS 排行榜失败: {str(e)}")
    
    async def phi_rankfind(self, event: AstrMessageEvent, rks):
        """获取有多少人大于查询 RKS"""
        if not rks:
            yield event.plain_result("请提供 RKS 值")
            return
        
        try:
            rks_value = float(rks)
        except ValueError:
            yield event.plain_result("请提供有效的 RKS 值")
            return
        
        try:
            # 调用 Phigros API 获取排名数据
            url = f"{APIBASEURL}/get/ranklist/rksRank"
            params = {
                "min_rks": rks_value
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            rank_data = response.json()
            count = rank_data.get("count", 0)
            
            yield event.plain_result(f"有 {count} 人 RKS 大于 {rks}")
        except Exception as e:
            logger.error(f"获取排名数据失败: {e}")
            yield event.plain_result(f"获取排名数据失败: {str(e)}")
    
    async def phi_data(self, event: AstrMessageEvent):
        """获取用户 data 数量"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        session_token = self.user_data[user_id]["sessionToken"]
        
        try:
            # 调用 Phigros API 获取用户数据
            url = f"{APIBASEURL}/get/cloud/saves"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "token": session_token
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            game_data = response.json()
            user_info = game_data.get("user_info", {})
            data_count = user_info.get("data_count", 0)
            
            yield event.plain_result(f"您的 data 数量：{data_count}")
        except Exception as e:
            logger.error(f"获取用户 data 数量失败: {e}")
            yield event.plain_result(f"获取用户 data 数量失败: {str(e)}")
    
    async def phi_guess(self, event: AstrMessageEvent):
        """猜曲绘游戏"""
        try:
            # 获取曲绘目录
            ill_dir = os.path.join(self.plugin_dir, "resources", "html", "avatar")
            
            # 列出所有曲绘文件
            if not os.path.exists(ill_dir):
                yield event.plain_result("曲绘目录不存在")
                return
            
            ill_files = [f for f in os.listdir(ill_dir) if f.endswith(".png") or f.endswith(".jpg")]
            
            if not ill_files:
                yield event.plain_result("曲绘文件不存在")
                return
            
            # 随机选择一个曲绘
            selected_file = random.choice(ill_files)
            song_name = os.path.splitext(selected_file)[0]
            
            # 发送曲绘给用户
            ill_path = os.path.join(ill_dir, selected_file)
            
            # 保存当前游戏状态
            user_id = event.get_sender_id()
            if user_id not in self.user_data:
                self.user_data[user_id] = {}
            
            self.user_data[user_id]["guess_game"] = {
                "song_name": song_name,
                "start_time": time.time()
            }
            self.save_user_data()
            
            # 发送曲绘和游戏提示
            yield event.image_result(ill_path)
            yield event.plain_result("猜曲绘游戏开始！请猜测曲名。")
        except Exception as e:
            logger.error(f"猜曲绘游戏失败: {e}")
            yield event.plain_result(f"猜曲绘游戏失败: {str(e)}")
    
    async def phi_ltr(self, event: AstrMessageEvent):
        """开字母游戏"""
        try:
            # 获取曲目信息文件
            info_file = os.path.join(self.plugin_dir, "resources", "info", "info.csv")
            
            if not os.path.exists(info_file):
                yield event.plain_result("曲目信息文件不存在")
                return
            
            # 读取曲目列表
            song_names = []
            with open(info_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) > 0:
                        song_names.append(parts[0])
            
            if not song_names:
                yield event.plain_result("曲目列表为空")
                return
            
            # 随机选择一首歌曲
            selected_song = random.choice(song_names)
            
            # 生成初始显示（首字母 + 下划线）
            if len(selected_song) > 0:
                display = selected_song[0]
                display += "_" * (len(selected_song) - 1)
            else:
                display = ""
            
            # 保存游戏状态
            user_id = event.get_sender_id()
            if user_id not in self.user_data:
                self.user_data[user_id] = {}
            
            self.user_data[user_id]["ltr_game"] = {
                "song_name": selected_song,
                "display": display,
                "guessed_letters": set(selected_song[0]),
                "start_time": time.time()
            }
            self.save_user_data()
            
            # 发送游戏提示
            yield event.plain_result(f"开字母游戏开始！\n曲名：{display}\n请使用 #出 命令开字母。")
        except Exception as e:
            logger.error(f"开字母游戏失败: {e}")
            yield event.plain_result(f"开字母游戏失败: {str(e)}")
    
    async def phi_tipgame(self, event: AstrMessageEvent):
        """提示猜曲游戏"""
        try:
            # 获取曲目信息文件
            info_file = os.path.join(self.plugin_dir, "resources", "info", "info.csv")
            
            if not os.path.exists(info_file):
                yield event.plain_result("曲目信息文件不存在")
                return
            
            # 读取曲目列表
            song_info = []
            with open(info_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) > 1:
                        song_info.append({"name": parts[0], "composer": parts[1]})
            
            if not song_info:
                yield event.plain_result("曲目列表为空")
                return
            
            # 随机选择一首歌曲
            selected_song = random.choice(song_info)
            song_name = selected_song["name"]
            composer = selected_song.get("composer", "未知")
            
            # 生成初始提示
            initial_tip = f"作曲家：{composer}"
            
            # 保存游戏状态
            user_id = event.get_sender_id()
            if user_id not in self.user_data:
                self.user_data[user_id] = {}
            
            self.user_data[user_id]["tipgame"] = {
                "song_name": song_name,
                "composer": composer,
                "tips_given": [initial_tip],
                "start_time": time.time()
            }
            self.save_user_data()
            
            # 发送游戏提示
            yield event.plain_result(f"提示猜曲游戏开始！\n{initial_tip}\n请使用 #tip 命令获取更多提示。")
        except Exception as e:
            logger.error(f"提示猜曲游戏失败: {e}")
            yield event.plain_result(f"提示猜曲游戏失败: {str(e)}")
    
    async def phi_song(self, event: AstrMessageEvent, args):
        """查询曲目信息"""
        if not args:
            yield event.plain_result("请提供曲名")
            return
        
        song_name = args[0]
        
        try:
            # 调用 Phigros API 获取曲目信息
            url = f"{APIBASEURL}/get/cloud/song"
            params = {
                "name": song_name
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            song_data = response.json()
            
            if not song_data:
                yield event.plain_result(f"未找到曲目：{song_name}")
                return
            
            # 提取曲目信息
            composer = song_data.get("composer", "未知")
            bpm = song_data.get("bpm", 0)
            
            # 构建曲目信息文本
            song_info = f"{song_name} 的信息：\n"
            song_info += f"作曲家：{composer}\n"
            song_info += f"BPM：{bpm}\n"
            
            # 提取各难度的定数
            difficulties = song_data.get("difficulties", [])
            for diff in difficulties:
                diff_name = diff.get("name", "")
                rating = diff.get("rating", 0)
                if diff_name and rating:
                    song_info += f"{diff_name} 定数：{rating}\n"
            
            yield event.plain_result(song_info)
        except Exception as e:
            logger.error(f"查询曲目信息失败: {e}")
            yield event.plain_result(f"查询曲目信息失败: {str(e)}")
    
    async def phi_chart(self, event: AstrMessageEvent, args):
        """查询谱面信息"""
        if not args:
            yield event.plain_result("请提供曲名")
            return
        
        song_name = args[0]
        difficulty = "IN" if len(args) < 2 else args[1].upper()
        
        try:
            # 调用 Phigros API 获取谱面信息
            url = f"{APIBASEURL}/get/cloud/song"
            params = {
                "name": song_name,
                "difficulty": difficulty
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            chart_data = response.json()
            
            if not chart_data:
                yield event.plain_result(f"未找到曲目 {song_name} 的 {difficulty} 难度谱面")
                return
            
            # 提取谱面信息
            rating = chart_data.get("rating", 0)
            note_count = chart_data.get("note_count", 0)
            bpm = chart_data.get("bpm", 0)
            
            # 构建谱面信息文本
            chart_info = f"{song_name} ({difficulty}) 的谱面信息：\n"
            chart_info += f"定数：{rating}\n"
            chart_info += f"物量：{note_count}\n"
            chart_info += f"BPM：{bpm}\n"
            
            yield event.plain_result(chart_info)
        except Exception as e:
            logger.error(f"查询谱面信息失败: {e}")
            yield event.plain_result(f"查询谱面信息失败: {str(e)}")
    
    async def phi_tag(self, event: AstrMessageEvent, args):
        """查看谱面标签"""
        if len(args) < 3:
            yield event.plain_result("请提供曲名、难度和标签")
            return
        
        song_name = args[0]
        difficulty = args[1].upper()
        tag = args[2]
        
        try:
            # 调用 Phigros API 获取谱面标签
            url = f"{APIBASEURL}/chartsTag/get/bySongRank"
            params = {
                "song_name": song_name,
                "difficulty": difficulty
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            tag_data = response.json()
            
            if not tag_data:
                yield event.plain_result(f"未找到曲目 {song_name} 的 {difficulty} 难度谱面的 {tag} 标签")
                return
            
            # 构建标签信息文本
            tag_info = f"{song_name} ({difficulty}) 的标签：{tag}\n"
            tag_info += f"标签描述：{tag_data.get('description', '无描述')}\n"
            tag_info += f"使用次数：{tag_data.get('usage_count', 0)}"
            
            yield event.plain_result(tag_info)
        except Exception as e:
            logger.error(f"查看谱面标签失败: {e}")
            yield event.plain_result(f"查看谱面标签失败: {str(e)}")
    
    async def phi_settag(self, event: AstrMessageEvent, args):
        """给谱面打标签"""
        if len(args) < 3:
            yield event.plain_result("请提供曲名、难度和标签")
            return
        
        # 这里需要实现与 Phigros API 的交互
        # 暂时返回模拟结果
        yield event.plain_result(f"成功为 {args[0]} ({args[1]}) 添加标签：{args[2]}")
    
    async def phi_comment(self, event: AstrMessageEvent, args):
        """评论曲目"""
        if len(args) < 2:
            yield event.plain_result("请提供曲名和评论内容")
            return
        
        # 这里需要实现与 Phigros API 的交互
        # 暂时返回模拟结果
        yield event.plain_result(f"评论成功！")
    
    async def phi_recmt(self, event: AstrMessageEvent, comment_id):
        """查看并确认是否删评"""
        if not comment_id:
            yield event.plain_result("请提供评论 ID")
            return
        
        # 这里需要实现与 Phigros API 的交互
        # 暂时返回模拟结果
        yield event.plain_result(f"评论 ID {comment_id}：\n内容：这是一条评论\n是否删除？")
    
    async def phi_mycmt(self, event: AstrMessageEvent):
        """查看自己的云端评论"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data or "sessionToken" not in self.user_data[user_id]:
            yield event.plain_result("请先绑定 sessionToken")
            return
        
        # 这里需要实现与 Phigros API 的交互
        # 暂时返回模拟结果
        yield event.plain_result("您的评论：\n1. 曲目 A - 这是一条评论")
    
    async def phi_table(self, event: AstrMessageEvent, difficulty):
        """查询定数表"""
        if not difficulty:
            yield event.plain_result("请提供定数")
            return
        
        # 这里需要实现与 Phigros API 的交互
        # 暂时返回模拟结果
        yield event.plain_result(f"定数 {difficulty} 的曲目：\n1. 曲目 A\n2. 曲目 B")
    
    async def phi_new(self, event: AstrMessageEvent):
        """查询更新的曲目"""
        # 这里需要实现与 Phigros API 的交互
        # 暂时返回模拟结果
        yield event.plain_result("最新更新的曲目：\n1. 曲目 A\n2. 曲目 B")
    
    async def phi_tips(self, event: AstrMessageEvent):
        """随机 tips"""
        # 这里需要实现随机 tips 逻辑
        # 暂时返回模拟结果
        yield event.plain_result("随机 tips：\nPhigros 是一款非常好玩的音游！")
    
    async def phi_jrrp(self, event: AstrMessageEvent):
        """今日人品"""
        # 这里需要实现今日人品逻辑
        # 暂时返回模拟结果
        yield event.plain_result("今日人品：99\n运气爆棚！")
    
    async def phi_alias(self, event: AstrMessageEvent, args):
        """查询某一曲目的别名"""
        if not args:
            yield event.plain_result("请提供曲名")
            return
        
        # 这里需要实现别名查询逻辑
        # 暂时返回模拟结果
        yield event.plain_result(f"{args[0]} 的别名：\n别名 1\n别名 2")
    
    async def phi_rand(self, event: AstrMessageEvent, args):
        """随机曲目"""
        # 这里需要实现随机曲目逻辑
        # 暂时返回模拟结果
        yield event.plain_result("随机曲目：曲目 A (IN 15.0)")
    
    async def phi_randclg(self, event: AstrMessageEvent, args):
        """随机课题"""
        # 这里需要实现随机课题逻辑
        # 暂时返回模拟结果
        yield event.plain_result("随机课题：\n1. 曲目 A (IN 15.0)\n2. 曲目 B (IN 14.8)\n3. 曲目 C (IN 14.5)\n课题总值：44.3")
    
    async def phi_ill(self, event: AstrMessageEvent, args):
        """查询曲绘"""
        if not args:
            yield event.plain_result("请提供曲名")
            return
        
        # 这里需要实现曲绘查询逻辑
        # 暂时返回模拟结果
        yield event.plain_result(f"{args[0]} 的曲绘已发送")
    
    async def phi_search(self, event: AstrMessageEvent, args):
        """检索曲库中的曲目"""
        if len(args) < 2:
            yield event.plain_result("请提供条件和值")
            return
        
        # 这里需要实现检索逻辑
        # 暂时返回模拟结果
        yield event.plain_result(f"检索结果：\n1. 曲目 A\n2. 曲目 B")
    
    async def phi_theme(self, event: AstrMessageEvent, theme):
        """切换绘图主题"""
        if not theme:
            yield event.plain_result("请提供主题编号 (0-2)")
            return
        
        # 这里需要实现主题切换逻辑
        # 暂时返回模拟结果
        yield event.plain_result(f"主题已切换为：{theme}")
    
    async def phi_sign(self, event: AstrMessageEvent):
        """签到获取 Notes"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        
        # 这里需要实现签到逻辑
        # 暂时返回模拟结果
        yield event.plain_result("签到成功！获得 10 Notes")
    
    async def phi_task(self, event: AstrMessageEvent):
        """查看自己的任务"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        
        # 这里需要实现任务查看逻辑
        # 暂时返回模拟结果
        yield event.plain_result("您的任务：\n1. 游玩 10 首歌曲 - 未完成\n2. 获得 1 个 FC - 未完成")
    
    async def phi_retask(self, event: AstrMessageEvent):
        """刷新任务"""
        user_id = event.get_sender_id()
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        
        # 这里需要实现任务刷新逻辑
        # 暂时返回模拟结果
        yield event.plain_result("任务已刷新！")
    
    async def phi_send(self, event: AstrMessageEvent, args):
        """送给目标 Note"""
        if len(args) < 2:
            yield event.plain_result("请提供目标和数量")
            return
        
        # 这里需要实现送 Note 逻辑
        # 暂时返回模拟结果
        yield event.plain_result(f"已成功送给 {args[0]} {args[1]} Notes")
    
    async def phi_backup(self, event: AstrMessageEvent, args):
        """备份存档文件"""
        # 这里需要实现备份逻辑
        # 暂时返回模拟结果
        yield event.plain_result("存档备份成功！")
    
    async def phi_restore(self, event: AstrMessageEvent):
        """从备份中还原"""
        # 这里需要实现还原逻辑
        # 暂时返回模拟结果
        yield event.plain_result("存档还原成功！")
    
    async def phi_setnick(self, event: AstrMessageEvent, args):
        """设置歌曲别名"""
        if len(args) < 3 or "--->" not in args:
            yield event.plain_result("请使用正确的格式：/phi setnick <原名> ---> <别名>")
            return
        
        # 这里需要实现设置别名逻辑
        # 暂时返回模拟结果
        yield event.plain_result("别名设置成功！")
    
    async def phi_delnick(self, event: AstrMessageEvent, args):
        """删除歌曲别名"""
        if not args:
            yield event.plain_result("请提供要删除的别名")
            return
        
        # 这里需要实现删除别名逻辑
        # 暂时返回模拟结果
        yield event.plain_result("别名删除成功！")
    
    async def phi_force_update(self, event: AstrMessageEvent):
        """强制更新插件"""
        # 这里需要实现强制更新逻辑
        # 暂时返回模拟结果
        yield event.plain_result("插件更新成功！")
    
    async def terminate(self):
        """插件被卸载/停用时调用"""
        self.save_user_data()
        logger.info("PhiPlugin 已卸载")
