"""
API Docs: https://developer.work.weixin.qq.com/document/14404
"""
import os
from enum import Enum
from pathlib import Path
from typing import Dict, Union, List

import dotenv
import loguru
import requests

from . import util

dotenv.load_dotenv()


# msgtype类型：text, markdown, image, news, file, voice, template_card
class MsgType(Enum):
    TEXT = 'text'
    MARKDOWN = 'markdown'
    IMAGE = 'image'
    NEWS = 'news'
    FILE = 'file'
    VOICE = 'voice'
    TEMPLATE_CARD = 'template_card'


class MediaType(Enum):
    FILE = 'file'
    VOICE = 'voice'


class Robot(object):
    """企业微信机器人

    Usage:
    >>> from wx_robot import Robot
    >>> robot = Robot('0559be4f-5d50-48f4-abd9-df504201d93e')
    >>> robot.send('text', {'content': 'hello world'})

    """

    base_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook'

    def __init__(self, key: Union[str, None]):
        self.key = self._check_key(key)

    def _check_key(self, key):
        """检查key是否存在
        """
        key = key or os.environ.get('WX_ROBOT_KEY')
        if not key:
            loguru.logger.error('请提供机器人key!')
            exit(1)
        return key

    def upload_media(self, file: Union[Path, str], media_type: MediaType = 'file'):
        """文件上传接口

        Args:
            file (Union[Path, str]): 文件路径
            media_type (MediaType, optional): 文件类型，可选值：voice(语音)， file(普通文件，默认)
        """
        url = self.base_url + '/upload_media'
        params = {'key': self.key, 'type': media_type}
        file = Path(file)
        
        files = {
            'media': (file.name, file.open('rb'), 'application/octet-stream')
        }

        response = requests.post(url, params=params, files=files).json()
        return response

    def send(self, msgtype: MsgType, data: Dict):
        """发送消息

        Args:
            msgtype (MsgType): 消息类型
            data (Dict): 消息内容
        """
        url = self.base_url + '/send'
        params = {'key': self.key}
        payload = {
            'msgtype': msgtype,
            msgtype: data,
        }

        response = requests.post(url, params=params, json=payload).json()
        # print(response)
        if response['errcode'] == 0:
            loguru.logger.debug(f'发送 {msgtype} 消息成功')
        elif response['errcode'] == 93000:
            loguru.logger.error(f'发送 {msgtype} 消息失败: 机器人key不合法或者机器人已经被移除出群')
        elif response['errcode'] == 45033:
            loguru.logger.error(f'发送 {msgtype} 消息失败: 接口并发调用超过限制')
        else:
            loguru.logger.error(f'发送 {msgtype} 消息失败: {response["errmsg"]}')

        return response
    
    def send_text(self, content: str, mentioned_list: List[str] = None, mentioned_mobile_list: List[str] = None):
        """发送文本消息

        Args:
            content (str): 消息内容
        """
        data = {'content': content}
        if mentioned_list:
            data['mentioned_list'] = mentioned_list
        if mentioned_mobile_list:
            data['mentioned_mobile_list'] = mentioned_mobile_list
        return self.send('text', data)
    
    def send_markdown(self, content: str):
        """发送markdown消息

        Args:
            content (str): 消息内容

        支持的markdown语法如下:
            - 标题
            - 加粗
            - 链接
            - 链接
            - 行内代码
            - 引用
            - 字体颜色(只支持3种内置颜色):
                - <font color="info">绿色</font>
                - <font color="comment">灰色</font>
                - <font color="warning">橙红色</font>
        """
        return self.send('markdown', {'content': content})
    
    def send_image(self, image_path: Union[Path, str]):
        """发送图片消息

        Args:
            image_path (Union[Path, str]): 图片路径
        """
        return self.send('image', util.wrap_image_data(image_path))
    
    def send_file(self, file_path: Union[Path, str]):
        """发送文件消息

        Args:
            file_path (Union[Path, str]): 文件路径
        """
        media_id = self.upload_media(file_path)['media_id']
        return self.send('file', {'media_id': media_id})
    
    def send_voice(self, voice_path: Union[Path, str]):
        """发送语音消息

        Args:
            voice_path (Union[Path, str]): 语音路径
        """
        media_id = self.upload_media(voice_path, media_type='voice')['media_id']
        return self.send('voice', {'media_id': media_id})
    
    def send_news(self, articles: List[Dict]):
        """发送新闻消息

        Args:
            articles (List[Dict]): 新闻列表

        Example:
            articles = [
                {
                    'title': 'Hello, World!',
                    'description': 'This is a test news.',
                    'url': 'https://www.example.com',
                    'picurl': 'https://www.example.com/logo.png',
                }
            ]
        """
        return self.send('news', {'articles': articles})

    def send_template_card(self, data: Dict):
        """发送模板卡片消息

        Args:
            data (Dict): 模板卡片数据

        Example:
            https://developer.work.weixin.qq.com/document/path/91770#模版卡片类型
        """
        return self.send('template_card', data)


if __name__ == '__main__':
    robot = Robot()

    robot.send_text('Hello, World!')
    # robot.send_text('Hello, World!', mentioned_list=['suqingdong'])
    # robot.send_text('Hello, World!', mentioned_mobile_list=['15202204043'])
    # robot.send_markdown('# Hello, World!')
    robot.send_markdown('<font color="info">绿色</font>')
    # robot.send_image('test.png')
    # robot.send_file('README.md')

    # robot.send_news([{
    #     'title': 'Hello, World!',
    #     'description': 'This is a test news.',
    #     'url': 'https://cn.novogene.com',
    #     'picurl': 'https://cn.novogene.com/sequencing-2/images/chlogo.png',
    # }])
