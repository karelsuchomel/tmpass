import shlex, subprocess
import os, sys
from pathlib import Path

class LogoutSleeper:
	def __init__(self, sleepTime, uid):
		self.sleepTime = sleeTime
		self.uid = uid
		self.procKiller = None
	
	def __del__(self):
		self.procKiller.kill()
		self.procKiller.wait()
	
	def run(self):
		args = shlex.split("sleep " + self.sleepTime + " ; pkill -KILL -u " + self.uid) # maybe -U is right one
		self.procKiller = subprocess.Popen(args, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

class PipeNotifier:
	def __init__(self, pipePath, pipeName, uid):
		self.pipePath = pipePath
		self.pipeName = pipeName
		self.uid = uid
		self.fullPipePath = os.path.join(self.pipePath, self.pipeName)
		self.fifo = None

		Path(self.pipePath).mkdir(parents=True, exist_ok=True)
		pipeFile = Path(self.fullPipePath)
		if pipeFile.is_file():
			os.unlink(self.fullPipePath)
			
		try:
			os.mkfifo(self.fullPipePath)
		except OSError as e:
			print("Failed to create FIFO: %s", e)
		else:
			self.fifo = open(self.fullPipePath, "r")
			print "Path is created."

	def __del__(self):
		close(self.fifo)
		os.unlink(self.fullPipePath)
		
	def read(self):
		line = self.fifo.readline()
		if line == self.uid + "\n":
			return True
		else:
			return False
		

def main():
	notifier = PipeNotifier("/dev/shm/tmpass/", "tmpass_pipe", "1002")
	killer = None
	while notifier.read():
		del killer
		# TODO: change password
		killer = LogoutSleeper(3600, 1002)

if __name__ == "__main__":
    main()

