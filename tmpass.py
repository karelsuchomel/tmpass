#!/usr/bin/python3

import array
import os
import subprocess
import sys
import stat
import logging
from pathlib import Path
# This project imports:
import dateToFourDigits


# create logger
logger = logging.getLogger('tmpass')
logger.setLevel(logging.INFO)
logging.basicConfig(filename='/var/log/tmpass_core.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class LogoutSleeper:
    def __init__(self, sleep_time, uid):
        self.sleepTime = str(sleep_time)
        self.uid = str(uid)
        self.proc = None

    def __del__(self):
        self.stop()

    def stop(self):
        if not (self.proc is None):
            self.proc.kill()
            self.proc.wait()
            self.proc = None

    def run(self):
        args = "sleep " + self.sleepTime + " && pkill -KILL -u " + self.uid  # FIXME: Maybe -U is right one
        logger.info("Starting: " + str(args))
        self.proc = subprocess.Popen(args, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


class PipeNotifier:
    def __init__(self, pipe_path, pipe_name, uid):
        self.pipePath = pipe_path
        self.pipeName = pipe_name
        self.uid = uid
        self.fullPipePath = os.path.join(self.pipePath, self.pipeName)

        Path(self.pipePath).mkdir(parents=True, exist_ok=True)
        pipe_file = Path(self.fullPipePath)
        if pipe_file.is_file() or pipe_file.is_fifo():
            os.unlink(self.fullPipePath)

        try:
            os.mkfifo(self.fullPipePath)
        except OSError as e:
            logger.critical("Failed to create FIFO: %s", e)
        else:
            os.chmod(self.fullPipePath, stat.S_IROTH | stat.S_IWOTH)
            logger.info("FIFO is created.")

    def __del__(self):
        os.unlink(self.fullPipePath)

    def read_verify(self):
        line_process = subprocess.run("read -r line <" + self.fullPipePath + " && echo $line",
                                      shell=True, stdout=subprocess.PIPE)
        line = str(line_process.stdout, "utf-8")
        logger.debug("line: " + line)
        if line == self.uid + "\n":
            return True
        else:
            return False


def change_pass(uid):
    password = dateToFourDigits.get_current_password()
    args = 'passwd $(getent passwd ' + uid + ' | cut -d: -f1)'
    x = array.array('b')
    x.frombytes((password + '\n' + password).encode())
    pass_changer = subprocess.run(args, shell=True, stdout=subprocess.PIPE, input=x)
    logger.info("Password changed...")
    logger.debug("Password changed: " + password)


def main():
    uid = os.getenv("TMPASS_MNG_USER")
    if len(sys.argv) != 2 and uid is None:
        error_msg = "Missing UID or environment TMPASS_MNG_USER... Usage: $ " + sys.argv[0] + " <UID>"
        print(error_msg)
        logger.critical(error_msg)
        return 1
    elif len(sys.argv) == 2:
        uid = sys.argv[1]
    sleep_seconds = os.getenv("TMPASS_SLEEP", "3600")
    logger.info("INIT ... uid: " + uid + " sleep_seconds: " + sleep_seconds)

    notifier = PipeNotifier("/dev/shm/", "tmpass_pipe", str(uid))
    sleep_and_logout = LogoutSleeper(sleep_seconds, uid)
    while True:
        if notifier.read_verify() is True:
            logger.info("New login.")
            sleep_and_logout.stop()
            change_pass(str(uid))
            sleep_and_logout.run()

if __name__ == "__main__":
    main()
