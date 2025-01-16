# Robot Client for QiYe Wechat
> https://developer.work.weixin.qq.com/document/14404


## Installation

```bash
python3 -m pip install wx-robot-client
```

## Usage

### Usage in CMD

```bash
wx_robot -h

# method 1: use -k option
wx_robot -k YOUR_ROBOT_KEY 'hello world'

# method 2: use env variable
WX_ROBOT_KEY=YOUR_ROBOT_KEY wx_robot 'hello world'

# method 3: use .env [recommend]
echo "WX_ROBOT_KEY=YOUR_ROBOT_KEY" > .env
wx_robot 'hello world'

# --------------------------------------------------

# send markdown
wx_robot -t markdown '# hello world'

# send image
wx_robot -t image test.png

# send file
wx_robot -t file README.md

# send news
wx_robot -t news '[{"title": "Hello, World!", "description": "...", "url": "https://www.example.com", "picurl": "xxx"}]'

# --------------------------------------------------
# send message from file
wx_robot requirement.txt
wx_robot -t markdown README.md
wx_robot -t news news.json
wx_robot -t template_card template_card.json
```

### Usage in Python

```python
from wx_robot.core import Robot

robot = Robot()

robot.send_text('Hello, World!')
robot.send_markdown('# Hello, World!')
robot.send_image('test.png')
robot.send_file('README.md')

robot.send_news([{
    'title': 'Hello, World!',
    'description': 'This is a test news.',
    'url': 'https://www.example.com',
    'picurl': 'https://www.example.com/demo.png',
}])
```