# countdown.py
# plays a sound at the end of a countdown 

import time, argparse, pyglet
from fprint import fprint

def display_countdown(delta, run_time):	
	fprint ('.')

def play_sound():
	sound = pyglet.media.load('clock-tick2.wav')
	sound.play()
	
	def exit(delta):
		pyglet.app.exit()

	pyglet.clock.schedule_once(exit, 2.6)
	pyglet.app.run()

def main():	
	parser = argparse.ArgumentParser()
	parser.add_argument('--minutes', help = 'countdown from specified minutes', type = int)
	args = parser.parse_args()
	if args.minutes:
		completion_time = time.time() + (args.minutes * 60) 
	else:
		completion_time = time.time()
	while time.time() <= completion_time:
		print completion_time - time.time()
  	play_sound()
	
if (__name__=='__main__'):
	main()
