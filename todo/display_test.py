s = 'There was once a man who loved to live alone because when he was alone he could truly think. One day he woke up and realized that there was no point in thinking when you are truly alone te te te that is what he said'
line_width = 10
nbr_lines = len(s) // line_width
print len(s)
print (nbr_lines)

for i in range(nbr_lines):
	line = s[:line_width]
	s = s[line_width:]
	
	while (len(s) != 0 and line[len(line) - 1] != ' '):
		line += s[:1]
		s = s[1:]

	print line
if (s):
	print s
