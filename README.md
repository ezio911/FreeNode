### FreeNode

> 无任何流量限制
> 实测晚高峰看 youtube 1080P 情况下完全不卡

- 部署

```bash
# 下载本项目的 compose.yaml 
docker compose up -d

# 开始爬取代理信息
http://127.0.0.1:5000/sub/crawl?token=ezio911

# 上一步完成后,稍等一分钟,即可获取代理链接
http://127.0.0.1:5000/sub/get?token=ezio911

# 因为会定时删除已经被使用过或者失效的代理信息,所以可以设置定时任务爬取代理信息
crontab -e
0 */3 * * * curl http://127.0.0.1:5000/sub/crawl?token=ezio911
```



- 客户端使用

> 1.使用 [hiddify](https://github.com/hiddify/hiddify-app/releases/tag/v2.5.7) 客户端
>
> 2.安装完成客户端后,复制获取的代理信息的链接,然后在客户端首页添加,(设置自动更新,定时获取最新链接)
>
> 3.打开hiddify客户端的配置选项 (因为公开的代理信息对一些网站有限制,所以必须在客户端开启一些功能,才能解除限制)
>
>  	-  将远程dns设置成  https://1.1.1.1/dns-query , 直连dns设置成 udp://223.5.5.5
>  	-  开启严格路由,关闭dns路由,服务模式选择系统代理,tun实现选择system
>  	-  启用 TLS 数据分段,启用 TLS 混合 SNI 情形,启用 TLS填充

- Api

```bash
# 以超级 token 开始爬取免费代理信息
http://127.0.0.1:5000/sub/crawl?token=ezio911

# 创建普通 token 给其他人使用
http://127.0.0.1:5000/token/create?token=ezio911&user_token=普通token

# 获取免费 token (超级token 和 普通 token都可以)
http://127.0.0.1:5000/sub/get?token=ezio911[普通token]

# 将订阅链接生成二维码分享给别人(带管理员token的订阅链接默认不允许分享)
http://127.0.0.1:5000/sub/qrcode?token=普通token

# 删除 普通token
http://127.0.0.1:5000/sub/del?token=ezio911&user_token=普通用户token
```

- config.json 文件说明

```bash
# config.json是全局配置文件,位于项目目录下 App/resources/config.json
# 如果想修改config.json文件,请下载源码修改,或者通过挂载数据卷的方式
# 如果想定义更多功能,请关注下个版本!
{
  "auth": {
    "admin_token": "ezio911"
  },
  "crawl": {
    "total": 20,
    "interval": 12
  },
  "banBot": {
    "try_count": 3,
    "ban_duration": 36000
  },
  "redis": {
    "host": "free-node-redis",
    "port": 6379,
    "password": "ezio911"
  }
}


# admin_token 管理员token
# total 每次发送爬取代理信息的个数
# interval 设置代理信息的有效期为6小时,普通用户在获取了一个代理信息后,需要6小时才能获取新的
# try_count 非法用户尝试需要超级token才能访问的接口,超过3次就封禁ip,被封禁后无法访问所有接口
# ban_duration 封禁ip的时间为 36000秒
```