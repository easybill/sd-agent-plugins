"""
  Server Density Plugin
  StorCLI (MegaRAID) monitor

  Inspired by https://github.com/serverdensity/sd-agent-plugins/tree/master/MegaRAID

  Version: 1.0.0
"""

import json
import logging
import platform
import sys
import subprocess
import time


class StorCLI(object):
    """
        Check the "Hlth" of the controller using output from
        /opt/MegaRAID/storcli/storcli64 show J
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
                ['sudo', '/opt/MegaRAID/storcli/storcli64', 'show', 'J'],
                stdout=subprocess.PIPE,
                close_fds=True)
            output = proc.communicate()[0]
        except OSError as exception:
            self.checks_logger.error(
                'Unable to find /opt/MegaRAID/storcli/storcli64.'
                ' Error: {0}'.format(exception.message))
            return data

        outputJson = json.loads(output)

        for ctl in outputJson['Controllers']:
            for stat in ctl['Response Data']['System Overview']:
                data['Ctl-' + str(stat['Ctl']) + '-Hlth'] = stat['Hlth']

        return data


if __name__ == '__main__':
    """
        Standalone test
    """

    raw_agent_config = {}

    main_checks_logger = logging.getLogger('StorCLI')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    megaraid_check = StorCLI({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(megaraid_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
