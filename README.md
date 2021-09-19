# <p align="center">QL_HeyTap</p>

## 普通版本
- 点击前往[HeyTap](https://github.com/Mashiro2000/HeyTap)

## 免责声明
- 本仓库发布的QL_HeyTap项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.

- 所有使用者在使用QL_HeyTap项目的任何部分时，需先遵守法律法规。对于一切使用不当所造成的后果，需自行承担.对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

- 如果任何单位或个人认为该项目可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关文件.

- 任何以任何方式查看此项目的人或直接或间接使用该QL_HeyTap项目的任何脚本的使用者都应仔细阅读此声明。本人保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或QL_HeyTap项目的规则，则视为您已接受此免责声明.

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
* [x] 积分大作战
* [ ] 发信功能

## 文件说明
```text
│  HeyTap.py         # 欢太商城任务中心
│  timingCash.py     # 欢太定时红包，建议配合Linux定时系统Crontab
│  dailyCash.py      # 每日现金任务
│  CheckInEarly.py   # 欢太商城，早睡报名或打卡，建议配合Linux定时系统Crontab
│  PointsBattle.py   # 积分大作战
│  formatCK.py       # 格式化CK(本地运行)
│  README.md         # 说明文档
```


#### 拉库指令
```text
ql repo https://github.com/Mashiro2000/QL_HeyTap.git                        # 国外机
ql repo https://ghproxy.com/https://github.com/Mashiro2000/QL_HeyTap.git    # 国内机(谢谢大佬的代理)
```

#### 变量值
- 结果测试欢太所需CK为: `TOKENSID`、`app_param`

#### 变量格式
```text
    名称= HT_COOKIE
    值=     {
            'user':'',                                      # 自定义备注(为了区分账号，包括未登录状态下)
            'CK':'TOKENSID=TOKEN_xxxx;',
            'UA':'UA',
            'app_param':'{"a":"a","b":"b","c":"c"};'
            }
    备注=   随便填
```

##### 变量获取
- CK和UA信息需自行抓包，欢太商城 -> 我的 -> 任务中心 -> 领券中心
- 抓包地址:`https://store.oppo.com/cn/oapi/users/web/checkPeople/isNewPeople`
- 其中`app_param`包含在CK中，由于青龙面板把嵌套JSON转换为不可直接转变的字符串,需手动提取'app_param'   PS:可能是我太菜了

##### 格式样本
![](https://s3.bmp.ovh/imgs/2021/09/28fd1982909e4e91.png)
