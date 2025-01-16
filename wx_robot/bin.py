import json
from pathlib import Path

import click
import loguru

from wx_robot import version_info
from wx_robot.core import Robot, MsgType


CONTEXT_SETTINGS = dict(
    help_option_names=['-?', '-h', '--help'],
    max_content_width=120,
)

@click.command(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.option('-k', '--key', help='the key of the robot', envvar='WX_ROBOT_KEY', show_envvar=True)
@click.option('-t', '--msg-type', help='the type of the message', type=click.Choice([t.value for t in list(MsgType)]), default=MsgType.TEXT.value, show_default=True)
@click.argument('data', nargs=1)
def cli(key, msg_type, data):
    robot = Robot(key)

    if msg_type in ('file', 'voice', 'image'):
        getattr(robot, f'send_{msg_type}')(data)
    else:
        if Path(data).is_file():
            data = Path(data).read_text()

        if msg_type in ('news', 'template_card'):
            try:
                data = json.loads(data)
            except Exception:
                loguru.logger.error('invalid json format, please check!')
                exit(2)
        getattr(robot, f'send_{msg_type}')(data)

def main():
    cli()


if __name__ == '__main__':
    main()
