#!/usr/bin/python3

import array
import os
import subprocess
import sys
import stat
import logging
import datetime
import time
import _thread
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


class UserNotificationSleeper:
    def __init__(self, session_length):
        self.sessionLength = int(session_length)
        self.proc = None

    def __del__(self):
        self.stop()

    def stop(self):
        if not (self.proc is None):
            self.proc.kill()
            self.proc.wait()
            self.proc = None

    def run(self):
        args = "sleep " + str(
            self.sessionLength - 600) + " && notify-send \"10 minut do odhlášení\" && sleep 300 && notify-send \"5 minut do odhlášení\" && sleep 240 && notify-send \"1 minuta do odhlášení\""
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
        logger.info("line: " + line)
        if line == self.uid + "\n":
            return True
        else:
            return False


def hour_scheduler(uid):
    while True:
        change_pass(str(uid))

        dt = datetime.datetime.now() + datetime.timedelta(hours=1)
        dt = dt.replace(minute=0, second=0, microsecond=0)

        time.sleep((dt - datetime.datetime.now()).total_seconds())
        logger.info("Run scheduled action: " + str(datetime.datetime.now()))


def change_pass(uid):
    password = dateToFourDigits.get_current_password()
    args = 'passwd $(getent passwd ' + uid + ' | cut -d: -f1)'
    x = array.array('b')
    x.frombytes((password + '\n' + password).encode())
    pass_changer = subprocess.run(args, shell=True, stdout=subprocess.PIPE, input=x)
    logger.info("Password changed...")
    logger.info("Password changed: " + password)


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
    schedule_user_notifications = UserNotificationSleeper(sleep_seconds)
    sleep_and_logout = LogoutSleeper(sleep_seconds, uid)
    _thread.start_new_thread(hour_scheduler, (uid,))
    while True:
        if notifier.read_verify() is True:
            logger.info("New login.")
            sleep_and_logout.stop()
            schedule_user_notifications.stop()
            sleep_and_logout.run()
            schedule_user_notifications.run()


if __name__ == "__main__":
    main()
