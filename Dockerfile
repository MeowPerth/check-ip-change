FROM python:3.7-alpine
 
RUN pip install requests
 
COPY run.py /run.py

ENV API="https://ddns.oray.com/checkip,https://ip.3322.net"
ENV FROM_NAME=
ENV FROM_EMAIL=
ENV FROM_EMAIL_PASSWORD=
ENV TO_EMAIL=
ENV SMTP_SERVER="smtp.qq.com"
ENV SMTP_PORT="465"
ENV INTERVAL="60"
ENV EMAIL_TITLE="IP 地址改变提醒"
ENV EMAIL_HEADER="服务器检测到当前 ip 地址发生改变！"
ENV EMAIL_FOOTER="来自 Check IP Change"
 
ENTRYPOINT ["python3", "-u","/run.py"]