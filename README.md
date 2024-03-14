# 功能简介
此镜像常用Python脚本编写，用于监测本地IP，如果IP发生变更即发送邮件进行通知收件人。
<br> 支持 多API获取IP
<br> 支持 多收件人
<br> 支持 自定义发件人昵称、邮件标题、正文内容

# Docker运行参数
```
docker run -d \
--name Check-IP-Change \
-e API="https://ddns.oray.com/checkip,https://ip.3322.net" \
-e FROM_EMAIL="xxx@qq.com" \
-e FROM_EMAIL_PASSWORD="xxx" \
-e TO_EMAIL="xxx@qq.com" \
-e SMTP_SERVER="smtp.qq.com" \
-e SMTP_PORT=465 \
-e INTERVAL=60 \
--restart=always \
1114788662/check-ip-change
```
# 所有参数解释：

| 变量 | 含义 | 
| --- | --- | 
| API | 可以返回公网地址的 api，支持多个地址，以半角逗号隔开，默认为https://ddns.oray.com/checkip, https://ip.3322.net | 
| FROM_NAME | 自定义发送人名称 | 
| FROM_EMAIL | 发送人邮箱（必填） | 
| FROM_EMAIL_PASSWORD | 发送人邮箱授权码（必填） | 
| TO_EMAIL | 收件人邮箱，支持多个接收人，以半角逗号隔开，默认为发送人邮箱 | 
| SMTP_SERVER | smtp 服务器地址，默认为 smtp.qq.com | 
| SMTP_PORT | smtp 端口，默认为 465 | 
| INTERVAL | 检测间隔，默认为 60s | 
| EMAIL_TITLE | 自定义邮件标题，默认为 "IP 地址改变提醒" | 
|  EMAIL_HEADER | 自定义邮件开头，默认为 "服务器检测到当前 ip 地址发生改变！" | 
| EMAIL_FOOTER | 自定义邮件结尾，默认为 "来自 Check IP Change" | 

# 参考资料
本镜像源码参考 阿蛮君 进行修改制作。
<br> https://registry.hub.docker.com/r/hausen1012/checkip/
<br> https://www.amjun.com/577.html
