// 引入AstrBot核心API
const { AstrBot, pluginAuth, dataManager, configManager } = require('@astrbot/core');
// 引入插件组件
const Config = require('./src/components/Config.js');
const getSave = require('./src/model/getSave.js');
const fCompute = require('./src/model/fCompute.js');
const getInfo = require('./src/model/getInfo.js');
const getBanGroup = require('./src/model/getBanGroup.js');
const picmodle = require('./src/model/picmodle.js');
const send = require('./src/model/send.js');
const getUpdateSave = require('./src/model/getUpdateSave.js');
const getBackup = require('./src/model/getBackup.js');
const guessIll = require('./src/apps/guessGame/guessIll.js');
const guessLetter = require('./src/apps/guessGame/guessLetter.js');
const guessTips = require('./src/apps/guessGame/guessTips.js');
const getNotes = require('./src/model/getNotes.js');
const getFile = require('./src/model/getFile.js');
const path = require('path');
const getdata = require('./src/model/getdata.js');
const getRksRank = require('./src/model/getRksRank.js');
const phisong = require('./src/apps/phisong.js');
const chart = require('./src/apps/chart.js');
const manage = require('./src/apps/manage.js');
const money = require('./src/apps/money.js');
const jrrp = require('./src/apps/jrrp.js');
const setting = require('./src/apps/setting.js');
const Dan = require('./src/apps/Dan.js');
const RankList = require('./src/apps/RankList.js');
const apiSetting = require('./src/apps/apiSetting.js');
const b19 = require('./src/apps/b19.js');
const update = require('./src/apps/update.js');
const user = require('./src/apps/user.js');

// 插件注册函数（AstrBot规范）
module.exports = (bot) => {
  const { commandManager, sessionManager } = bot;
  const config = configManager.get('catrong.phi') || {};
  const cmdHead = Config.getUserCfg('config', 'cmdhead') || 'phi';

  // **************************
  // 注册普通用户指令（核心查分功能）
  // **************************
  
  // phi帮助
  commandManager.register(['phi帮助', 'phi菜单', 'phi命令', 'phi使用说明'], async (session) => {
    try {
      const head = cmdHead;
      const pluginData = await require('./src/model/getNotes.js').getNotesData(session.user.id);
      const background = getInfo.getill(getInfo.illlist[fCompute.randBetween(0, getInfo.illlist.length - 1)]);
      const theme = pluginData?.theme || 'star';
      const helpGroup = await require('./src/model/getFile.js').FileReader(require('path').join(require('./src/model/path.js').infoPath, 'help.json'));
      
      // 生成帮助图片
      const helpImg = await picmodle.help(session, {
        helpGroup: helpGroup,
        cmdHead: head || null,
        isMaster: pluginAuth.isMaster(session.user.id),
        background: background,
        theme: theme
      });
      
      if (helpImg) {
        await session.sendImage(helpImg);
      } else {
        await session.send('生成帮助图片失败！');
      }
    } catch (error) {
      console.error('[phi-plugin] 帮助命令错误:', error);
      await session.send(`获取帮助失败：${error.message}`);
    }
  });

  // phi绑定 [token] （支持国服/国际服）
  commandManager.register('phi绑定 :type? :token*', async (session, { type, token }) => {
    const userId = session.user.id;
    const isGb = type === 'gb' ? true : false;
    
    try {
      // 保存token
      await getSave.add_user_token(userId, token);
      // 更新存档
      const updateResult = await getUpdateSave.getNewSave(userId, token, isGb);
      await session.send(updateResult ? '绑定成功！' : '绑定失败，请检查token是否正确。');
    } catch (error) {
      await session.send(`绑定失败：${error.message}`);
    }
  });

  // phi解绑
  commandManager.register('phi解绑', async (session) => {
    const userId = session.user.id;
    try {
      await getSave.del_user_token(userId);
      await session.send('解绑成功！');
    } catch (error) {
      await session.send(`解绑失败：${error.message}`);
    }
  });

  // phi b30 / phi rks / phi pgr （核心查分功能）
  commandManager.register(['phi b30', 'phi rks', 'phi pgr'], async (session) => {
    const userId = session.user.id;
    try {
      // 获取存档
      const save = await getSave.getSave(userId);
      if (!save) {
        await session.send('请先绑定sessionToken！');
        return;
      }
      
      // 计算B30
      const stats = await save.getStats();
      const b30Result = {
        text: `您的RKS：${stats.rankingScore.toFixed(2)}\nB30：${stats.b30.toFixed(2)}\nB19：${stats.b19.toFixed(2)}`,
        img: await picmodle.b30(session, save)
      };
      
      // 发送结果
      if (b30Result.img) {
        await session.sendImage(b30Result.img);
      } else {
        await session.send(b30Result.text);
      }
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi更新
  commandManager.register('phi更新', async (session) => {
    const userId = session.user.id;
    try {
      const token = await getSave.get_user_token(userId);
      if (!token) {
        await session.send('请先绑定sessionToken！');
        return;
      }
      
      const updateResult = await getUpdateSave.getNewSave(userId, token);
      await session.send(updateResult ? '更新成功！' : '更新失败，请检查网络连接。');
    } catch (error) {
      await session.send(`更新失败：${error.message}`);
    }
  });

  // phi猜曲绘
  commandManager.register('phi猜曲绘', async (session) => {
    if (!session.groupId) {
      await session.send('请在群聊中使用这个功能！');
      return;
    }
    
    try {
      const result = await guessIll.start(session);
      await session.send(result);
    } catch (error) {
      await session.send(`游戏启动失败：${error.message}`);
    }
  });

  // phi开字母
  commandManager.register('phi开字母', async (session) => {
    if (!session.groupId) {
      await session.send('请在群聊中使用这个功能！');
      return;
    }
    
    try {
      const result = await guessLetter.start(session);
      await session.send(result);
    } catch (error) {
      await session.send(`游戏启动失败：${error.message}`);
    }
  });

  // phi提示猜曲
  commandManager.register('phi提示猜曲', async (session) => {
    if (!session.groupId) {
      await session.send('请在群聊中使用这个功能！');
      return;
    }
    
    try {
      const result = await guessTips.start(session);
      await session.send(result);
    } catch (error) {
      await session.send(`游戏启动失败：${error.message}`);
    }
  });

  // **************************
  // 注册主人管理指令（需权限校验）
  // **************************
  
  // phi备份
  commandManager.register('phi备份', async (session) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      await getBackup.backup();
      await session.send('备份成功！');
    } catch (error) {
      await session.send(`备份失败：${error.message}`);
    }
  });

  // phi恢复
  commandManager.register('phi恢复', async (session) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const backups = await getBackup.listBackups();
      if (backups.length === 0) {
        await session.send('没有找到备份文件！');
        return;
      }
      
      let msg = '请选择需要恢复的备份文件：\n';
      backups.forEach((backup, index) => {
        msg += `[${index}]${backup}\n`;
      });
      await session.send(msg);
      
      // 实现会话管理，等待用户输入选择
      sessionManager.createSession({
        userId: session.user.id,
        groupId: session.groupId,
        type: 'phi_restore',
        data: { backups },
        timeout: 60000, // 60秒超时
        onMessage: async (message) => {
          try {
            const index = parseInt(message.content);
            if (isNaN(index) || index < 0 || index >= backups.length) {
              await session.send('请输入有效的文件序号！');
              return false; // 继续等待输入
            }
            
            const selectedBackup = backups[index];
            const restoreResult = await getBackup.restore(selectedBackup);
            await session.send(restoreResult ? '恢复成功！' : '恢复失败，请检查备份文件是否正确。');
            return true; // 会话结束
          } catch (error) {
            await session.send(`恢复失败：${error.message}`);
            return true; // 会话结束
          }
        },
        onTimeout: async () => {
          await session.send('恢复操作已超时，请重新执行命令！');
        }
      });
    } catch (error) {
      await session.send(`恢复失败：${error.message}`);
    }
  });

  // **************************
  // 注册更多普通用户指令
  // **************************

  // phi info
  commandManager.register('phi info', async (session) => {
    const userId = session.user.id;
    try {
      const save = await getSave.getSave(userId);
      if (!save) {
        await session.send('请先绑定sessionToken！');
        return;
      }
      
      const infoImg = await picmodle.userinfo(session, save);
      if (infoImg) {
        await session.sendImage(infoImg);
      } else {
        await session.send('生成信息失败！');
      }
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi score
  commandManager.register('phi score :song*', async (session, { song }) => {
    const userId = session.user.id;
    try {
      const save = await getSave.getSave(userId);
      if (!save) {
        await session.send('请先绑定sessionToken！');
        return;
      }
      
      const scoreImg = await picmodle.score(session, save, song);
      if (scoreImg) {
        await session.sendImage(scoreImg);
      } else {
        await session.send('查询失败，可能是曲目名称不正确！');
      }
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi data
  commandManager.register('phi data', async (session) => {
    const userId = session.user.id;
    try {
      const data = await getdata.getdata(userId);
      await session.send(`您的data数量：${data}`);
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi jrrp
  commandManager.register('phi jrrp', async (session) => {
    try {
      const jrrpResult = await jrrp.getJrrp(session.user.id);
      await session.send(jrrpResult);
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi rand
  commandManager.register('phi rand :args*', async (session, { args }) => {
    try {
      const randResult = await picmodle.rand(session, args);
      if (randResult) {
        await session.sendImage(randResult);
      } else {
        await session.send('随机失败！');
      }
    } catch (error) {
      await session.send(`随机失败：${error.message}`);
    }
  });

  // phi song
  commandManager.register('phi song :song*', async (session, { song }) => {
    try {
      const songResult = await phisong.getSongInfo(session, song);
      await session.send(songResult);
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi chart
  commandManager.register('phi chart :song*', async (session, { song }) => {
    try {
      const chartResult = await chart.getChartInfo(session, song);
      await session.send(chartResult);
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi table
  commandManager.register('phi table :level', async (session, { level }) => {
    try {
      const tableResult = await picmodle.table(session, level);
      if (tableResult) {
        await session.sendImage(tableResult);
      } else {
        await session.send('查询失败！');
      }
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi ill
  commandManager.register('phi ill :song*', async (session, { song }) => {
    try {
      const illResult = await picmodle.ill(session, song);
      if (illResult) {
        await session.sendImage(illResult);
      } else {
        await session.send('查询失败，可能是曲目名称不正确！');
      }
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi sign
  commandManager.register('phi sign', async (session) => {
    try {
      const signResult = await money.sign(session);
      await session.send(signResult);
    } catch (error) {
      await session.send(`签到失败：${error.message}`);
    }
  });

  // phi task
  commandManager.register('phi task', async (session) => {
    try {
      const taskResult = await money.task(session);
      if (taskResult) {
        await session.sendImage(taskResult);
      } else {
        await session.send('获取任务失败！');
      }
    } catch (error) {
      await session.send(`获取任务失败：${error.message}`);
    }
  });

  // phi retask
  commandManager.register('phi retask', async (session) => {
    try {
      const retaskResult = await money.retask(session);
      await session.send(retaskResult);
    } catch (error) {
      await session.send(`刷新任务失败：${error.message}`);
    }
  });

  // phi send
  commandManager.register('phi send :target :amount', async (session, { target, amount }) => {
    try {
      const sendResult = await money.send(session, target, amount);
      await session.send(sendResult);
    } catch (error) {
      await session.send(`转账失败：${error.message}`);
    }
  });

  // phi ranklist
  commandManager.register('phi ranklist :rank?', async (session, { rank }) => {
    try {
      const rankResult = await picmodle.rankingList(session, rank);
      if (rankResult) {
        await session.sendImage(rankResult);
      } else {
        await session.send('获取排行榜失败！');
      }
    } catch (error) {
      await session.send(`获取排行榜失败：${error.message}`);
    }
  });

  // phi rankfind
  commandManager.register('phi rankfind :rks', async (session, { rks }) => {
    try {
      const rankFindResult = await getRksRank.getRankByRks(rks);
      await session.send(rankFindResult);
    } catch (error) {
      await session.send(`查询失败：${error.message}`);
    }
  });

  // phi theme
  commandManager.register('phi theme :theme', async (session, { theme }) => {
    try {
      const themeResult = await setting.setTheme(session, theme);
      await session.send(themeResult);
    } catch (error) {
      await session.send(`设置主题失败：${error.message}`);
    }
  });

  // phi tips
  commandManager.register('phi tips', async (session) => {
    try {
      const tipsResult = await setting.getTips();
      await session.send(tipsResult);
    } catch (error) {
      await session.send(`获取tips失败：${error.message}`);
    }
  });

  // **************************
  // 注册更多管理指令
  // **************************

  // phi设置别名
  commandManager.register('phi设置别名 :name :alias', async (session, { name, alias }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const setNickResult = await manage.setNick(name, alias);
      await session.send(setNickResult);
    } catch (error) {
      await session.send(`设置别名失败：${error.message}`);
    }
  });

  // phi删除别名
  commandManager.register('phi删除别名 :alias', async (session, { alias }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const delNickResult = await manage.delNick(alias);
      await session.send(delNickResult);
    } catch (error) {
      await session.send(`删除别名失败：${error.message}`);
    }
  });

  // phi下载曲绘
  commandManager.register('phi下载曲绘', async (session) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      await getInfo.downill();
      await session.send('曲绘下载成功！');
    } catch (error) {
      await session.send(`曲绘下载失败：${error.message}`);
    }
  });

  // phi设置
  commandManager.register('phi设置 :args*', async (session, { args }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const setResult = await setting.set(args);
      await session.send(setResult);
    } catch (error) {
      await session.send(`设置失败：${error.message}`);
    }
  });

  // phi更新插件
  commandManager.register(['phi更新插件', 'phi强制更新'], async (session) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const updateResult = await update.updatePlugin(session);
      await session.send(updateResult);
    } catch (error) {
      await session.send(`更新失败：${error.message}`);
    }
  });

  // phi获取token
  commandManager.register('phi获取token :rank', async (session, { rank }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const getTokenResult = await manage.getToken(rank);
      await session.send(getTokenResult);
    } catch (error) {
      await session.send(`获取token失败：${error.message}`);
    }
  });

  // phi禁用token
  commandManager.register('phi禁用token :token', async (session, { token }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const delTokenResult = await manage.delToken(token);
      await session.send(delTokenResult);
    } catch (error) {
      await session.send(`禁用token失败：${error.message}`);
    }
  });

  // phi恢复token
  commandManager.register('phi恢复token :token', async (session, { token }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const allowTokenResult = await manage.allowToken(token);
      await session.send(allowTokenResult);
    } catch (error) {
      await session.send(`恢复token失败：${error.message}`);
    }
  });

  // phi禁用功能
  commandManager.register('phi禁用功能 :func', async (session, { func }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const banResult = await manage.ban(func);
      await session.send(banResult);
    } catch (error) {
      await session.send(`禁用功能失败：${error.message}`);
    }
  });

  // phi恢复功能
  commandManager.register('phi恢复功能 :func', async (session, { func }) => {
    if (!pluginAuth.isMaster(session.user.id)) {
      await session.send('仅主人可执行该操作！');
      return;
    }
    
    try {
      const unbanResult = await manage.unban(func);
      await session.send(unbanResult);
    } catch (error) {
      await session.send(`恢复功能失败：${error.message}`);
    }
  });

  console.log('[phi-plugin] Phigros插件已成功适配AstrBot并加载！');
};