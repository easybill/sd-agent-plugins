"""
  Server Density Plugin
  ArcconfCLI monitor

  Inspired by https://github.com/serverdensity/sd-agent-plugins/tree/master/MegaRAID

  Version: 1.0.0
"""

import json
import logging
import platform
import sys
import subprocess
import time


class ArcconfCLI(object):
    """
        Check the "Status of Logical Device" of the controller using output from
        arcconf GETCONFIG 1 LD
    """

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()

    def run(self):

        data = {}

        try:
            proc = subprocess.Popen(
                ['arcconf', 'GETCONFIG', '1', 'LD'],
                stdout=subprocess.PIPE,
                close_fds=True)
            output = proc.communicate()[0]
        except OSError as exception:
            self.checks_logger.error(
                'Unable to find arcconf.'
                ' Error: {0}'.format(exception.message))
            return data

        ldn = 'X'
        for line in output.split("\n"):
            if line.startswith('Logical Device number'):
                ldn = line.replace('Logical Device number ', '').replace(' ', '')
            if line.startswith('   Status of Logical Device'):
                data['logical-device-' + ldn + '-state'] = line.split(':')[1].replace(' ', '')

        return data


if __name__ == '__main__':
    """
        Standalone test
    """

    raw_agent_config = {}

    main_checks_logger = logging.getLogger('ArcconfCLI')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    megaraid_check = ArcconfCLI({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(megaraid_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
