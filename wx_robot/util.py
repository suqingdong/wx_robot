import base64
import hashlib
from typing import Union, Dict
from pathlib import Path



def get_file_md5(file: Union[Path, str]) -> str:
    """获取文件的md5值
    
    Args:
        file (Union[Path, str]): 文件路径

    Returns:
        str: md5值
    """
    with open(file, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


def get_image_base64(image_path: Union[Path, str]) -> str:
    """获取图片的base64编码
    
    Args:
        image_path (Union[Path, str]): 图片路径

    Returns:
        str: base64编码
    """
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def wrap_image_data(image_path: Union[Path, str]) -> Dict:
    """包装图片数据

    Args:
        image_path (Union[Path, str]): 图片路径

    Returns:
        Dict: 包装后的图片数据
    """
    return {
        'base64': get_image_base64(image_path),
        'md5': get_file_md5(image_path)
    }
