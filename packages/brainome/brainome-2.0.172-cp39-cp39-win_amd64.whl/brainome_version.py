"""
EDIT THIS PROGRAM TO CHANGE THE BASE "VERSION" NUMBER

RUN THIS PROGRAM TO WRITE THE CURRENT VERSION into btc_version.txt
Usage:
    python3 brainome_version.py
Output File:
    brainome_version.txt

Usage:
    python3 brainome_version.py -full
Returns:
    'v0.000-BUILD#-STAGE'  or   'v0.000-USER-BRANCH'

Usage:
    python3 brainome_version.py -short
Returns:
    latest | beta | alpha | branch
"""
import os
import subprocess
import logging
import sys
from typing import Union

logger = logging.getLogger(__name__)

# file with version stamp in it - created by running this program
btc_version_filename = 'brainome_version.txt'
version_filename = 'version.py'
env_filename = 'version.env'

version_dir = "."
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    BTCVERSION_TXT = sys._MEIPASS + "/_version/" + btc_version_filename
    VERSION_PY = sys._MEIPASS + "/_version/" + version_filename
    VERSION_ENV = sys._MEIPASS + "/_version/" + env_filename
else:
    # we are running in a normal Python environment
    BTCVERSION_TXT = os.path.dirname(os.path.abspath(__file__)) + '/' + btc_version_filename
    VERSION_PY = os.path.dirname(os.path.abspath(__file__)) + '/' + version_filename
    VERSION_ENV = os.path.dirname(os.path.abspath(__file__)) + '/' + env_filename

logger.debug("reporting template_dir=" + BTCVERSION_TXT)

BTC_FULL_VERSION = 'BTC_FULL_VERSION'
BTC_SHORT_VERSION = 'BTC_SHORT_VERSION'
BTC_STAGE = 'BTC_STAGE'
GIT_DETECT_MERGE_IN_PROGRESS = ['git', 'rev-parse', '-q', '--verify', 'MERGE_HEAD']     # exit code = 128 if not in progress
GIT_SHOW_BRANCH_CMD = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
GIT_DETECT_DETACHED_HEAD = ['git', 'symbolic-ref', '-q', 'HEAD']
GIT_SHOW_TAGS = ['git', 'describe', '--tags']
BTC_SRV_TAG_PREFIX = 'brainome/btc_srv'

""" edit this version variable with the version number of the application"""
VERSION = "2.0"


class BtcVersion:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if BtcVersion.__instance is None:
            BtcVersion()
        return BtcVersion.__instance

    """ container the entire BTC VERSION source code.
    Usage:
        BtcVersion.get_version()        ->  'v0.000-BUILD#-STAGE'  or   'v0.000-USER-BRANCH'
        v = BtcVersion()
        v.get_version()                 ->  'v0.000-BUILD#-STAGE'  or   'v0.000-USER-BRANCH'
        v.
    """
    def __init__(self):
        """ Virtually private constructor. """
        BtcVersion.__instance = self
        self.build = ''
        self.branch = self.__get_git_branch()
        self.release_stage = self.get_release_stage()
        self.run_number = self.__get_git_run_number()
        self.user = self.__get_user()
        self.build = 'unknown'
        self.version_full = self.get_version_full()
        self.version_short = self.get_version_short()
        logger.debug(f'BtcVersion initialized {self.version_full} {self.version_short}')

    @classmethod
    def __get_git_branch(cls):
        try:
            # preloaded into environment - no need to open shell
            b = os.getenv('BRANCH_NAME', None)
            if b is None:
                # not preloaded, execute git
                # detect merge in progress
                process4 = subprocess.Popen(GIT_DETECT_MERGE_IN_PROGRESS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process4.communicate()
                if process4.returncode == 0:
                    # merge in progress
                    b = "MERGE"
                else:
                    # detect detacted head stat
                    process1 = subprocess.Popen(GIT_DETECT_DETACHED_HEAD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = process1.communicate()
                    if process1.returncode != 0:
                        # we are in detached head state
                        # get tag name
                        process2 = subprocess.Popen(GIT_SHOW_TAGS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err = process2.communicate()
                        b = out.decode().strip()
                    else:
                        # get branch name
                        process3 = subprocess.Popen(GIT_SHOW_BRANCH_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err = process3.communicate()
                        b = out.decode().strip()
            logger.debug(f"git branch is {b}")
        except:     # noqa
            b = 'unknown'
        return b

    @classmethod
    def __get_git_run_number(cls) -> Union[str, None]:
        """ return github action run number or None """
        run_number = os.getenv('GITHUB_RUN_NUMBER', None)
        logger.debug(f"run number is {run_number}")
        return run_number

    @classmethod
    def __get_user(cls) -> Union[str, None]:
        """ return github action run number or None """
        user = 'root' if os.path.expanduser('~') == '/root' else os.getenv('SUDO_USER', os.getenv('USER', 'btcuser'))
        logger.debug(f"user is {user}")
        return user

    @classmethod
    def get_version(cls) -> str:
        """
        return the contents of brainome_version.txt found on disk
        which is created by running this program
        """
        try:
            # attempt importing version first
            import version
            version_stamp = version.BTC_FULL_VERSION
        except ImportError:
            # attempt reading static file second
            vfile = BTCVERSION_TXT
            if not os.path.isfile(vfile):
                # attempt to look in the current directory instead
                vfile = 'bin/' + version_filename

            try:
                with open(vfile) as version_file:
                    version_stamp = version_file.read()
                logger.info(f"version is {version_stamp}")
                version_stamp = version_stamp.strip()       # strip off trailing newline
            except OSError as os_err:
                logger.error(f'{vfile} not available', exc_info=os_err)
                version_stamp = 'unknown-unidentified'

        return version_stamp

    def get_version_full(self) -> str:
        if self.run_number is None:
            # user run
            self.build = 'dev'
            full_version = "v" + VERSION + '-{0}-{1}'.format(self.user, self.release_stage)
        else:
            # CI/CD run
            self.build = 'github'
            full_version = 'v' + VERSION + '-{0}-{1}'.format(self.run_number, self.release_stage)
        logger.info(f'current version is {full_version}')
        return full_version

    def get_version_pep(self) -> str:
        """ returns 1.2.333: """
        if self.run_number is None:
            # user run
            return VERSION
        else:
            # CI/CD run
            self.build = 'github'
            return VERSION + '.' + str(self.run_number)

    def get_version_short(self) -> str:
        """ returns latest, beta, alpha, branch for use in easy retrieval """
        if self.release_stage == 'prod':
            logger.debug('current version is latest')
            return 'latest'
        else:
            logger.debug(f'current version is {self.release_stage}')
            return self.release_stage

    def get_release_stage(self) -> str:
        """ if the branch starts with 'v' then it is PROD
            if the branch is main, master, or beta, then it is BETA
            if the branch is qa or development then it is ALPHA
            otherwise it is branch name
        """
        # if self.branch is None:
        #     logger.error('github branch not identified')
        #     return 'unknown'
        if self.branch.startswith('v') or self.branch.startswith('refs-tags-v'):
            return 'prod'
        elif self.branch in ['main', 'master', 'beta']:
            return 'beta'
        # elif self.branch in ['qa', 'alpha']:
        else:
            return 'alpha'
        # else:
        #     return self.branch

    def compare_versions(self, other_version: str, this_version: str = None):
        """
            compare this version with another version
            determine if the versions are compatible
            recommend identical vs upgrade/downgrade patch/recommended/required
        """
        # TODO implement rules found at https://docs.google.com/document/d/1-WE6YH2b7pz3Va6iuXoGU1TcnOx12AqKem7ESARps5I/edit#heading=h.ap5z23pnlr7w
        pass


def main():
    """
    writes version.txt and writes version.py
    """
    btc_version = BtcVersion()
    # write btcversion.txt with full version
    with open(BTCVERSION_TXT, "w") as write_version_file:
        write_version_file.write(btc_version.get_version_full())
        write_version_file.write("\n")
    # write btcversion.py with all the version info
    with open(VERSION_PY, "w") as write_version_py:
        write_version_py.write(f"BTC_FULL_VERSION = \"{btc_version.get_version_full()}\"\n")
        write_version_py.write(f"BTC_SHORT_VERSION = \"{btc_version.get_version_short()}\"\n")
        write_version_py.write(f"BTC_STAGE = \"{btc_version.get_release_stage()}\"\n")
        write_version_py.write(f"BTC_PEP = \"{btc_version.get_version_pep()}\"\n")
        write_version_py.write(f"BTC_SRV_FULL_TAG = \"{BTC_SRV_TAG_PREFIX}:{btc_version.get_version_full()}\"\n")
        write_version_py.write(f"BTC_SRV_SHORT_TAG = \"{BTC_SRV_TAG_PREFIX}:{btc_version.get_version_short()}\"\n")
    # write version.env with all the version info
    with open(VERSION_ENV, "w") as write_version_env:
        write_version_env.write(f"BTC_FULL_VERSION={btc_version.get_version_full()}\n")
        write_version_env.write(f"BTC_SHORT_VERSION={btc_version.get_version_short()}\n")
        write_version_env.write(f"BTC_STAGE={btc_version.get_release_stage()}\n")
        write_version_env.write(f"BTC_PEP={btc_version.get_version_pep()}\n")
        write_version_env.write(f"BTC_SRV_FULL_TAG={BTC_SRV_TAG_PREFIX}:{btc_version.get_version_full()}\n")
        write_version_env.write(f"BTC_SRV_SHORT_TAG={BTC_SRV_TAG_PREFIX}:{btc_version.get_version_short()}\n")


if __name__ == '__main__':
    btcv = BtcVersion()
    if len(sys.argv) > 1 and sys.argv[1] == '-short':
        print(btcv.get_version_short())
    elif len(sys.argv) > 1 and sys.argv[1] == '-full':
        print(btcv.get_version_full())
    elif len(sys.argv) > 1 and sys.argv[1] == '-stage':
        print(btcv.get_release_stage())
    elif len(sys.argv) > 1 and sys.argv[1] == '-pep':
        print(btcv.get_version_pep())
    else:
        main()
