# <p align="center">HeyTapTask</p>
<p align="center">目前代码已完成重构建！！！请重新下载或者拉取</P>
<p align="center">喜欢这个项目？可以在右上角给颗⭐！你的支持是我最大的动力😎！</P>

## 免责声明
- 本仓库发布的HeyTapTask项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.

- 所有使用者在使用HeyTapTask项目的任何部分时，需先遵守法律法规。对于一切使用不当所造成的后果，需自行承担.对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

- 如果任何单位或个人认为该项目可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关文件.

- 任何以任何方式查看此项目的人或直接或间接使用该HeyTapTask项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或HeyTapTask项目的规则，则视为您已接受此免责声明.

您必须在下载后的24小时内从计算机或手机中完全删除以上内容.

> 您使用或者复制了本仓库且本人制作的任何脚本，则视为`已接受`此声明，请仔细阅读

## 环境

[Python3](https://www.python.org/) >= 3.6.8

## 已实现功能
* [x] 每日签到
* [x] 每日浏览商品任务
* [x] 每日分享商品任务
* [x] ~~每日点推送任务~~(已下架)
* [x] 赚积分活动
* [x] 天天积分翻倍(默认注释，基本抽不到)
* [x] 天天领现金任务列表(可能黑号)
* [x] 天天领现金定时红包(可能黑号)
* [x] 早睡打卡
* [x] 积分大作战(realme)
* [x] 积分大作战(HeyTap) 由@kuake0挖掘
* [x] 配信功能 由@curtinlv开发

## 文件说明
```text
│  TaskCenter.py        # 欢太商城任务中心
│  TimingCash.py        # 欢太定时红包，建议配合定时系统
│  DailyCash.py         # 每日现金任务
│  ChockInEarly.py      # 欢太商城，早睡报名或打卡，建议配合定时系统
│  BattleForHeyTap.py   # 积分大作战(欢太)
│  BattleForRealMe.py   # 积分大作战(真我)
│  HT_config.py         # 欢太配置文件(推荐使用)
│  sendNotify.py        # 欢太配信文件(青龙已配备,无需额外下载)
│  README.md            # 说明文档
```

#### 一、Linux部署
```bash
yum install python3 -y

yum install git -y

git clone https://ghproxy.com/https://github.com/Mashiro2000/HeyTapTask.git   # 国内git较慢，故添加代理前缀

cd HeyTapTask

vi Ht_config.py
```

#### 二、青龙面板拉库指令
```text
旧版本升级新版本,先备份CK数据

第一次拉取
ql repo https://github.com/Mashiro2000/HeyTapTask.git "" "HT_.*|sendNotify" "HT_.*|sendNotify"

第二次拉取，确保HT_config.py不被覆盖，更改拉库命令，命令如下
ql repo https://github.com/Mashiro2000/HeyTapTask.git "" "HT_.*|sendNotify" "HT_config|sendNotify"
```

#### 三、云函数
- 重构前 -> [部署方案](https://github.com/Mashiro2000/HeyTapTask/blob/main/Doc/README.md)
- 重构后 -> 待更新

##### 变量值
- 测试表明欢太所需CK为: `source_type`、`TOKENSID`、`app_param`,顺序不可乱
- 不再支持青龙面板`环境变量`添加账号的方案,请尽快将CK转移至配置文件
- 原因:欢太变量采用json字符串,但青龙会将`HUAWEI P50`解析为`HUAWEIP50`
- CK和UA中的特定字符会被错误的解析,为了长远发展，请使用配置文件

##### 编辑配置文件(本地/青龙/云函数)
```text
# 推荐方案(HT_account.py)
{
    'user':'',                                                  # 自定义备注(为了区分账号，包括未登录状态下)
    'CK':'source_type=xxx;TOKENSID=TOKEN_xxxx;app_param=xxxx',  # 用户环境变量 Cookie,建议全部粘贴,且顺序不可乱
    'UA':'UA'                                                   # 用户环境变量 User-Agent
}
```

##### 变量获取
- CK和UA信息需自行抓包，欢太商城 -> 我的 -> 任务中心 -> 领券中心
- 抓包地址:`https://store.oppo.com/cn/oapi/users/web/checkPeople/isNewPeople`

#### 其他帮助
- Q:NameError: name '`xxxxxx`' is not defined
- A:可能是因为CK的格式存在错误,可以使用[bejson](https://www.bejson.com/)进行校验


#### 更新日志
<details>
<summary> </summary>
 
> 证明该项目仍然存活

2021-9-29
重构代码,确保后续更新不在涉及`HT_config.py`文件，新增环境变量`notifyBlack`和`Lottery`

</details>
