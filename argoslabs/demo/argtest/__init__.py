#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:helloworld
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: VIVANS
"""

# 관련 작업자
# ===========
#
# 본 모듈은 다음과 같은 사람들이 관여했습니다:
#  * 채문창
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#  * [2019/03/08]
#     - add icon
#  * [2018/11/02] TODO
#       subparsers 추가
#  * [2018/10/26]
#    -  >, >=, <=, <, ==, != 제공
#    -  정규식 validation
#    -  statfile test
#    -  verbose 코드
#    -  dumpspec 반영 확인
#  * [2018/09/30]
#     - 본 모듈 작업 시작
################################################################################
import sys
import time
from alabs.common.util.vvargs import ModuleContext, func_log, str2bool, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
@func_log
def helloworld(mcxt, argspec):
    if argspec.infile and argspec.infile != '-':
        sys.stdout.write('\n%s\n' % ('=' * 80))
        for line in sys.stdin:
            print(line.rstrip('\n'))

    params = [argspec.boolparam, argspec.intparam, argspec.floatparam,
              argspec.strparam]
    params += argspec.name
    params = map(str, params)
    sys.stdout.write('Hello world, %s\n' % ', '.join(params))
    if argspec.error:
        mcxt.logger.error('my runtime error')
        sys.stderr.write('RuntimeError: MyError\noccurs')
        raise RuntimeError('MyError\noccurs')

    if argspec.verbose > 0:
        mcxt.logger.info('>>>starting...')
    for i in range(argspec.steps):
        for j in range(argspec.max_loop):
            percent = (j+1) / argspec.max_loop * 100
            msg = '[%s/%s] step doing [%s/%s] ... ' \
                  % (i+1, argspec.steps, j+1, argspec.max_loop)
            if argspec.verbose > 1:
                mcxt.logger.debug('>>>%s' % msg)
            mcxt.add_status(i+1, argspec.steps, '%4.2f' % percent, msg)
            time.sleep(0.1)
    return argspec


################################################################################
def _main(*args):
    """
플러그인 모듈은 ModuleContext 을 생성하여 mcxt를 with 문과 함께 사용
    owner='ARGOS-LABS',
    group='demo',
    version='1.0',
    platform=['windows', 'darwin', 'linux'],
    output_type='text',
    description='Hello World friends',
    test_class=TU,

(참조: https://docs.python.org/ko/3.7/library/argparse.html)
사용자 입력에 필요한 spec은 다음과 같이 add_argument 함수 호출로 가능
    mcxt.add_argument(name or flags...[, action][, nargs][, const][, default]
        [, type][, choices][, required][, help][, metavar][, dest])
    단일 명령행 인자를 구문 분석하는 방법을 정의합니다.
    매개 변수마다 아래에서 더 자세히 설명되지만, 요약하면 다음과 같습니다:

    name or flags - 옵션 문자열의 이름이나 리스트, 예를 들어 foo 또는 -f, --foo.
        '-m', '--myarg' 와 같이 '-'로 시작하면 옵션 아니면 패러미터
    action - 명령행에서 이 인자가 발견될 때 수행 할 액션의 기본형
        'store' - 인자 값을 저장합니다. 이것이 기본 액션
        'append' - 리스트를 저장하고 각 인자 값을 리스트에 추가합니다
            옵션을 여러 번 지정할 수 있도록 하는 데 유용합니다
        'count' - 키워드 인자가 등장한 횟수를 계산합니다. 예를 들어,
            상세도를 높이는 데 유용합니다
        'store_true' 와 'store_false' - 각각 True 와 False 값을 저장하는
            'store_const' 의 특별한 경우입니다. 또한, 각각 기본값 False 와
            True 를 생성합니다
    nargs - 소비되어야 하는 명령행 인자의 수. 또는 다음과 같은 의미의 문자,
        N (정수). 명령행에서 N 개의 인자를 함께 모아서 리스트에 넣습니다.
        '?'. 가능하다면 한 인자가 명령행에서 소비되고 단일 항목으로 생성됩니다.
            명령행 인자가 없으면 default 의 값이 생성됩니다. 선택 인자의 경우
            추가적인 경우가 있습니다 - 옵션 문자열은 있지만, 명령행 인자가
            따라붙지 않는 경우입니다. 이 경우 const 의 값이 생성됩니다.
        '*'. 모든 명령행 인자를 리스트로 수집합니다. 일반적으로 두 개 이상의
            위치 인자에 대해 nargs='*' 를 사용하는 것은 별로 의미가 없지만,
            nargs='*' 를 갖는 여러 개의 선택 인자는 가능합니다
        '+'. '*' 와 같이, 존재하는 모든 명령행 인자를 리스트로 모읍니다.
            또한, 적어도 하나의 명령행 인자가 제공되지 않으면 에러 메시지가
            만들어집니다
    const - nargs='?' 를 주고 해당 값이 생략될 때 필요한 상숫값.
    default - 인자가 명령행에 없는 경우 생성되는 값.
    type - 명령행 인자가 변환되어야 할 형. (또는 str2bool 와 같은 함수)
        str - 문자열 (디폴트)
        int - 정수형
        float - 실수형
        str2bool - True/False, Yes/No 등의 문자열에서 판별
            'yes', 'true', 't', 'y', '1' 이면 True
            'no', 'false', 'f', 'n', '0' 이면 False
            둘다 아니면 예외 발생
    choices - 인자로 허용되는 값의 컨테이너.
    required - 명령행 옵션을 생략 할 수 있는지 아닌지 (선택적일 때만).
    help - 인자가 하는 일에 대한 간단한 설명.
    metavar - 사용 메시지에 사용되는 인자의 이름.
    dest - parse_args() 가 반환하는 argspec 객체에 추가될 어트리뷰트의 이름.
    min_value | greater_eq - 사용자가 입력한 값이 설정 값보다 같거나 크면 정상
    max_value | less_eq - 사용자가 입력한 값이 설정 값보다 같거나 작으면 정상
    min_value_ni | greater - 사용자가 입력한 값이 설정 값보다 크면 정상
    max_value_ni | less - 사용자가 입력한 값이 설정 값보다 작으면 정상
    equal - 사용자가 입력한 값이 설정 값과 같으면 정상
    not_equal - 사용자가 입력한 값이 설정 값과 같지 않으면 정상
    re_match - 사용자가 입력한 값이 설정 정규식을 만족하면 정상
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='demo',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='My Arg Test',
        icon_path=get_icon_path(__file__),
        description='Hello World friends',
    ) as mcxt:
        # ######################################## for app dependent options
        # mcxt.add_argument('--error', '-e', nargs="?", type=bool,
        #                   const=True, default=False,
        #                   help='make error forcefully')
        mcxt.add_argument('--error', '-e', action='store_true',
                          help='make error forcefully')
        mcxt.add_argument('--steps', '-s', nargs="?", type=int,
                          const=1, default=0,
                          min_value=0, max_value=5,
                          not_equal=3,
                          help='number of steps')
        mcxt.add_argument('--max-loop', '-m', nargs="?", type=int,
                          const=20, default=10,
                          min_value=1,
                          help='number of loop')
        mcxt.add_argument('--str-verify', nargs="?",
                          min_value='daa', max_value_ni='e',
                          help='str constraint')
        mcxt.add_argument('--append', '-a', action="append",
                          min_value='a', max_value_ni='d',
                          help='one or more append options')
        mcxt.add_argument('--count', '-c', action="count", default=0,
                          help='count option')
        mcxt.add_argument('--choice', choices=[3, 4, 5], type=int,
                          input_group='opt1', input_method='my_choice',
                          help='choices option')
        # ##################################### for app dependent parameters
        mcxt.add_argument('boolparam', type=str2bool,
                          input_group='grp1', input_method='my_boolean',
                          help='boolean parameter')
        mcxt.add_argument('intparam', type=int,
                          greater=40, less_eq=50,
                          input_group='grp1', input_method='my_int',
                          help='integer parameter')
        mcxt.add_argument('floatparam', type=float,
                          greater=0.0, less=1.0,
                          input_group='grp2', input_method='my_float',
                          help='float parameter')
        mcxt.add_argument('ipaddr', type=str,
                          re_match='^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
                          input_group='grp2', input_method='my_ip_addr4',
                          help='ipv4 address')
        mcxt.add_argument('strparam', help='문자열 패러미터',
                          greater_eq='tom')
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
