# Sentry dingtalkv

Sentry 集成钉钉机器人通知

## Requirments
- sentry >= 21.5.1

## 特性
- 发送异常通知到钉钉
- 配置 @ 成员，逗号分隔
## 快速使用
### 安装
1. 使用 `pip` 命令
    ```bash
    $ pip install sentry-dingtalkv
    ```

### 钉钉机器人
[配置](https://developers.dingtalkv.com/document/app/custom-robot-access)钉钉机器人并拿到对应的 webhook, 可以对机器人设置 关键词、签名、IP限制

### 配置
在 Sentry 面板 Settings > Integrations 中找到 dingtalkv 并配置 webhook、关键词等信息，添加项目，创建告警规则

### 如何更新发布？
1. 修改版本 代码逻辑
2. ```bash 
    $ python3 setup.py sdist
    $ python3 -m twine upload dist/* -u xxx -p xxx
    ```

