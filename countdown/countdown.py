#countdown.py
#
#plays a sound when countdown number reaches 0

import time, argparse, pyglet

def display_countdown(delta, run_time):
	clock_line = '|' + ('#' * (run_time - delta)) + ('-' * delta) + '|' + '[' + str(delta) + ' mins]' 
	for i in range (60):
		print clock_line	

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
	
	run_time = args.minutes * 60

	if args.minutes:
		completion_time = time.time() + run_time
	else:
		completion_time = time.time() + 100

	last_printed_digit = run_time
	delta = 1

	while (delta > 0):
		
		delta = int((completion_time - time.time()) / 60)
		if (delta < last_printed_digit):
			display_countdown(delta, run_time / 60)
			last_printed_digit = delta

  	play_sound()
	
if (__name__=='__main__'):
	main()