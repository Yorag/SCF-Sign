## 集成签到
集成签到，可加入腾讯云SCF云函数，也可修改部分代码直接运行

### 一、功能：
* 1.集成爱奇艺、腾讯视频、芒果tv、网易云音乐、天翼网盘、52破解论坛、精易论坛、乐易论坛的签到  

> a.爱奇艺：(签到、做任务VIP仅支持VIP)签7天奖1天，14天奖2天，28天奖7天；日常任务；随机成长值；抽奖
  b.腾讯视频：VIP签到两次获取成长值  
  c.芒果TV：连签21天，得15天体验会员；对应积分  
  d.网易云音乐：签到、300首歌单打卡  
  e.天翼云盘：签到、抽奖获取空间  
  f.吾爱破解论坛：2吾爱币  
  g.乐易论坛：随机易币、金币  
  h.精易论坛：随机精币  
 
* 2.支持多账户签到
* 3.支持添加QMsg酱推送

### 二、使用：
* 1.修改添加config.json相关参数
* 2.打包成zip文件，上传至scf云函数  
  *注：语言python3.6，超时时间设置为900*
* 3.添加定时触发器  
PS：若本机环境运行，将index.py的`def main_handler(event, context):`一行改为`if __name__ == '__main__':`，运行index.py

### 三、配置config.json
* 1.Skey为[Qmsg酱](https://qmsg.zendee.cn/login)密钥
* 2.[爱奇艺（IQIYI）](https://iqiyi.com/)官网，加载主页面，开发者工具搜索获取**P00001**，**P00003**参数
![爱奇艺 参数抓取](https://s1.ax1x.com/2020/08/10/aHuqns.jpg)
* 3.[腾讯视频（TV）](https://v.qq.com/)官网，浏览器F12开发者工具并刷新，找到请求**access.video.qq.com/user/auth_refresh**，params为?后字符串，cookies为返回cookies（可仅提取关键参数）
![腾讯视频 参数抓取](https://s1.ax1x.com/2020/08/10/aHKXKH.jpg)
* 4.[芒果TV（MGO）](https://www.mgtv.com/)官网，抓包获取**uuid**，**ticket**是cookie中的HDCN横线前的字符串进行替换
![芒果TV 参数抓取](https://s1.ax1x.com/2020/08/15/dibifU.png)
* 5.[网易云音乐（WYY）](https://music.163.com/)，填入账号、密码  
  *注：官方接口登录*
* 6.[天翼云盘（ECLOUD）](https://cloud.189.cn/)，填入账号、密码  
  *注：官方接口登录*
* 7.[吾爱破解（52PJ）](https://www.52pojie.cn/)网站，抓取cookies中关键参数**htVD_2132_saltkey、htVD_2132_auth**
* 8.[乐易论坛（LEY）](https://www.leybc.com/)网站，抓取cookise中关键参数**2vlT_96d0_saltkey、2vlT_96d0_auth**
* 9.[精易论坛（BBS）](https://bbs.125.la/)网站，抓取cookies中关键参数**lDlk_ecc9_saltkey、lDlk_ecc9_auth**
* 注：多账户在对应项目列表下添加字典参数即可；若指定项目不签到，对应项目下留空列表
