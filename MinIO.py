import json
import logging
import platform
import sys
import subprocess
import time
import re

class MinIO(object):
    """
        Check the status of MinIO Cluster. 
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
                ['sudo', 'mc', 'admin', 'info', 'local', '--json'],
                stdout=subprocess.PIPE,
                close_fds=True)
            output = proc.communicate()[0]
        except OSError as exception:
            self.checks_logger.error(
                ' Error: {0}'.format(exception.message))
            return data
       
        raw = json.loads(output)
        
        data['status'] = raw['status']
        data['mode'] = raw['info']['mode']
        data['backend-onlineDisks'] = raw['info']['backend']['onlineDisks']

        return data


if __name__ == '__main__':
    """
        Standalone test
    """

    raw_agent_config = {}

    main_checks_logger = logging.getLogger('gluster-peer')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    check = MinIO({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)       