"""
  @Project     : sentry-dingtalkv
  @Time        : 2022/05/26 15:35:12
  @File        : plugin.py
  @Author      : source
  @Software    : VSCode
  @Desc        :
"""


import requests
import six
import ast
from sentry import tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_plugins.base import CorePluginMixin
from django.conf import settings
class DingTalkVPlugin(CorePluginMixin, notify.NotificationPlugin):
    title = "dingtalkv"
    slug = "dingtalkv"
    description = "用于已指派负责人后，问题未被处理的通知"
    conf_key = "dingtalkv"
    required_field = "webhook"
    author = "source"
    author_url = "https://xxx.xxx.cc/FE/sentry-k8s/-/tree/main/sentry-dingtalkv"
    version = "1.0.2"
    resource_links = [
        ("Report Issue", "https://xxx.xxx.cc/FE/sentry-k8s/-/tree/main/sentry-dingtalkv/issues"),
        ("View Source", "https://xxx.xxx.cc/FE/sentry-k8s/-/tree/main/sentry-dingtalkv"),
    ]x

    feature_descriptions = [
        FeatureDescription(
            """
                完全服务于内部业务化的插件,于sentry-dingtalk-source不同，该插件无法对外使用.
                """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "webhook",
                "type": "url",
                "placeholder": "https://oapi.dingtalkv.com/robot/send?access_token=**********",
                "required": True,
                "help": "钉钉 webhook",
                "default": self.set_default(project, "webhook", "DingTalkV_WEBHOOK"),
            }
        ]

    def set_default(self, project, option, env_var):
        if self.get_option(option, project) != None:
            return self.get_option(option, project)
        if hasattr(settings, env_var):
            return six.text_type(getattr(settings, env_var))
        return None

    def notify(self, notification, raise_exception=False):
        event = notification.event
        user = event.get_minimal_user()
        userName = user.username
        release = event.release
        group = event.group
        project = group.project
        self._post(group, userName, release, project)

    def _post(self, group, userName, release, project):
        webhook = self.get_option("webhook", project)
        # 项目负责人
        # [@{at}](dingtalkv://DingTalkVclient/action/sendmsg?DingTalkV_id={at})
            
        assignee = group.get_assignee()
        issue_link = group.get_absolute_url(params={"referrer": "dingtalkv"})

        payload = f"#### [迷惑]已指派的问题还没有解决噢，赶快核查一下～\n\n"
        payload = f"{payload} #### 项目名：{project.name}\n\n"
        payload = f"{payload} #### 问题处理人：{assignee}\n\n"
        payload = f"{payload} #### [异常信息]({issue_link}): \n\n"
        payload = f"{payload} > {group.message}…\n\n"

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "charset": "utf8"
        }

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"{project.name}存在问题被重新激活，问题地址：{issue_link}",
                "text": payload,
            }
        }
        requests.post(webhook, data=json.dumps(data), headers=headers)
