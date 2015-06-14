#a simple diary program that runs on the command line

def fill_from_file(filename):
        """puts the contents of a text file formatted in a specific way into
        a dictionary"""
        
        try:
                f = open(filename, 'r')
                f.close()
        except:
                f = open(filename, 'a')
                f.close()

        f = open(filename,'r')
        last_line = '-'
        dic = {}
        value = ''
        for line in f:
                
                if '-' in (last_line):
                       key = line[:-1]
                elif '-' in (line):
                        dic[key] = value
                        value = ''
                else:
                        value +=  line
                last_line = line
        f.close()
        return dic

dic = fill_from_file('todo.txt')

while True:

        dates = dic.keys()
        entries = dic.values()
        nbr_dates = len(dates)
        command = raw_input('-> ')
        
        if command in ('list entries', 'le'):

                entries_left = 0
                last_line = ''
                
                if (nbr_dates % 3 == 1):
                        nbr_dates -= 1
                        entries_left = 1
                elif (nbr_dates % 3 == 2):
                        nbr_dates -= 2
                        entries_left = 2
                        
                for i in range(0,nbr_dates, 3):
                        print '{0:10} | {1:10} | {2:10}'.format(dates[i], dates[i+1], dates[i+2])
                        
                for i in range (entries_left,0,-1):
                        last_line += '{0:10} | '.format(dates[len(dates)-i])
                if (last_line):
                        print last_line
                if (len(dic) == 0):
                        print '<no entries>'
                                     
        elif 'read' in (command):

                key = command.replace('read ','')
                if key in dates:
                        print dic[key]
                else:
                        print 'no entry found'
                        
        elif command in ('add', 'a'):

                date = raw_input('date: ')
                entry = raw_input('entry: ')
                if date in dates:
                        dic[date] += '\n' + entry
                else:
                        dic[date] = entry
        elif 'delete' in (command):

                date = command.replace('delete ','')
                if date in dates:
                        del dic[date]
                      
        elif command in ('close','c'):
               
                f = open('todo.txt','w')
                for i in range(nbr_dates):
                        f.write(dates[i] + '\n')
                        f.write(entries[i] +'\n')
                        f.write('-\n')
                f.close()
                quit()

        elif command in ('total_entries', 'te'):

                print nbr_dates

        elif command in ('clear','c'):

                print 25*'\n'
                       



