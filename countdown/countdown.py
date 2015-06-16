#countdown.py
#
#plays a sound when countdown number reaches 0

import time
import argparse

def display_countdown(delta):
	print delta

def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--minutes', help = 'countdown from specified minutes', type = int)
	args = parser.parse_args()
	
	if args.minutes:
		completion_time = time.time() + (args.minutes * 10)
	else:
		completion_time = time.time() + 100

	last_printed_digit = 10
	delta = 1

	while (delta > 0):
		
		delta = int(completion_time - time.time())
		if (delta < last_printed_digit):
			display_countdown(delta)
			last_printed_digit = delta


	
if (__name__=='__main__'):
	main()