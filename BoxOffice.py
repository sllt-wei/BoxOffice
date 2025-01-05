import os
import json
import requests
from common.log import logger
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *
from typing import Dict, Any


@plugins.register(
    name="BoxOffice",
    desc="实时查询电影票房数据",
    version="1.0",
    author="Your Name",
    desire_priority=500
)
class BoxOffice(Plugin):
    # 配置常量
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
    API_ENDPOINT = "http://shanhe.kim/api/za/piaofang.php"

    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] initialized")

    def on_handle_context(self, e_context):
        """处理用户输入的上下文"""
        if e_context['context'].type != ContextType.TEXT:
            return

        content = e_context["context"].content.strip()
        if content == "票房":
            logger.info(f"[{__class__.__name__}] 收到票房查询请求")
            self._handle_text_query(e_context)

    def _fetch_box_office(self) -> Dict[str, Any]:
        """获取票房数据"""
        try:
            response = requests.get(self.API_ENDPOINT)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == "200":
                return data
            logger.error(f"API返回格式不正确: {data}")
            return {}
        except Exception as e:
            logger.error(f"获取票房数据失败: {e}")
            return {}

    def _handle_text_query(self, e_context):
        """处理文字版票房查询"""
        data = self._fetch_box_office()
        if not data:
            self._send_error_reply(e_context, "获取票房数据失败，请稍后重试")
            return

        reply_text = f"🎬 {data.get('day', '今日')}全国电影票房榜 🎬\n{'=' * 30}\n\n"

        for i in range(1, 11):
            movie = data.get(f'Top_{i}')
            if movie:
                rank_emoji = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else "🎯"
                reply_text += f"{rank_emoji} No.{i} {movie['name']}\n"
                reply_text += f"├ 上映日期：{movie['release date']}\n"
                reply_text += f"├ 实时票房：{movie['Box Office Million']}\n"
                reply_text += f"├ 票房占比：{movie['Share of box office']}\n"
                reply_text += f"├ 排片占比：{movie['Row Films']}\n"
                reply_text += f"└ 排座占比：{movie['Row seats']}\n\n"

        reply_text += f"{'=' * 30}\n数据更新时间：{data.get('day', '实时')} ⏰"

        e_context["reply"] = Reply(ReplyType.TEXT, reply_text)
        e_context.action = EventAction.BREAK_PASS

    def _send_error_reply(self, e_context, message: str):
        """发送错误消息"""
        e_context["reply"] = Reply(ReplyType.TEXT, message)
        e_context.action = EventAction.BREAK_PASS

    def get_help_text(self, **kwargs):
        """获取插件帮助信息"""
        help_text = """电影票房查询助手
        指令：
        发送"票房"：获取实时票房排行榜
        """
        return help_text
