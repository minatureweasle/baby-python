#a simple diary program that runs on the command line

def display(nbr_dates, dates):
    """diaplys dates in colums of three"""

    entries_left = 0
    last_line = ''
    
    print ''      

    if (nbr_dates % 3 == 1):
        nbr_dates -= 1
        entries_left = 1

    elif (nbr_dates % 3 == 2):
        nbr_dates -= 2
        entries_left = 2
                        
    for i in range(0,nbr_dates, 3):
        print '{0:10} | {1:10} | {2:10}'.format(dates[i],dates[i+1],
         dates[i+2])
                        
    for i in range (entries_left,0,-1):
        last_line += '{0:10} | '.format(dates[len(dates)-i])

    if (last_line):
        print last_line

    if (len(dic) == 0):
        print '<no entries>'

def fill_from_file(filename):
        """reads text file contents into a dictionary"""
        
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

               def compare_dates(date):
                try:
                    return  int(date[:2])
                except:
                    return 0

               dates.sort(key= compare_dates, reverse=True)
               display(nbr_dates, dates)
                                     
        elif 'read' in (command):

                key = command.replace('read ','')
                if key in dates:
                       
                        whole_entry = dic[key]
                        line_width = 25
                        lines_to_print = len(whole_entry) / line_width

                        for i in range(lines_to_print):
                            entry_line = whole_entry[:25]
                            whole_entry = whole_entry[25:]
                            print entry_line
                       
                        if (whole_entry):
                            print whole_entry

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
                        f.write(dates[i].replace('\n', '') + '\n')
                        f.write(entries[i].replace('\n', '') +'\n')
                        f.write('-\n')
                f.close()

                quit()

        elif command in ('total_entries', 'te', 't'):

                print nbr_dates

        elif command in ('clear','c'):

                print 25*'\n'