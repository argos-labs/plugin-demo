"""
====================================
 :mod:`your.demo.helloworld`
====================================
.. moduleauthor:: Your Name <user@modify.me>
.. note::

Description
===========
Your Demo plugin module sample
"""
# Authors
# ===========
#
# * Your Name
#
# Change Log
# --------
#
#  * [2019/03/08]
#     - add icon
#  * [2018/10/28]
#     - starting

################################################################################
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def helloworld(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    print('Hello world %s' % argspec.name)
    mcxt.logger.info('>>>end...')
    return 0


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='YOUR-LABS',
        group='demo',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='My World',
        icon_path=get_icon_path(__file__),
        description='Hello World friends',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('name', nargs='+', help='name to say hello')
        argspec = mcxt.parse_args(args)
        return helloworld(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
