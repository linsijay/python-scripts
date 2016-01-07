'''
read file and find the parsing failed log
'''

import re

def test_regex(regEX, test_file):
    reg_compile_obj = list()

    for r in regEX:
        reg_compile_obj.append(re.compile(r))

    f = file(test_file,'r')

    tmp = list()
    
    for line in f:
        for ro in reg_compile_obj:
            try:
                tmp = re.match(ro,line).groupdict()
                break
            except:
                pass
        
        #to show the parsing failed
        if tmp.__len__() == 0:
            print (line.strip())

if __name__ == '__main__':
    regEX = ('(?P<deviceName>[^\s]+)\sLogcategory\=(?P<fwLogType>\S+)', 
            '(?P<deviceName>[^\s]+)\sLogcategory\=(?P<fwLogType>\S+)')
    test_file = '/path/sample/file'
    
    test_regex(regEX, test_file)