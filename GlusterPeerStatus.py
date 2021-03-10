import json
import logging
import platform
import sys
import subprocess
import time
import re

class GlusterPeerStatus(object):

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()

    def run(self):

        data = {}

        try:
            proc = subprocess.Popen(
                ['sudo', 'gluster', 'peer', 'status'],
                stdout=subprocess.PIPE,
                close_fds=True)
            output = proc.communicate()[0]
        except OSError as exception:
            self.checks_logger.error(
                ' Error: {0}'.format(exception.message))
            return data

        pcc = output.count('Connected')
        pdc = output.count('Disconnected')

        lines = output.split("\n\n")
        firstline = lines.pop(0)
        data['peer-count'] = firstline.replace('Number of Peers:', '').replace(' ', '')
        data['peer-connected-count'] = pcc
        data['peer-disconnected-count'] = pdc

        for line in lines:
            match = re.search("Hostname: (.*)", line)
            hostname = match.group(1)
            match = re.search("State: (.*)", line)
            state = match.group(1)
            data['peer-' + hostname + '-state'] = state


        return data


if __name__ == '__main__':
    """
        Standalone test
    """

    raw_agent_config = {}

    main_checks_logger = logging.getLogger('gluster-peer')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    megaraid_check = GlusterPeerStatus({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(megaraid_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)       