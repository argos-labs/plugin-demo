"""
====================================
 :mod:`your.demo.helloworld`
====================================
.. moduleauthor:: Your Name <your@modify.me>
.. note:: YOURLABS License

Description
===========
YOUR LABS plugin module sample
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from your.demo.helloworld import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
