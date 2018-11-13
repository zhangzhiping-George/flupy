import sys
org_stdout = sys.stdout
sys.stdout = open('sysstdout_test.txt', 'w+')
print('here should be printed on screen, but redirected to sysdout_test.txt')
sys.stdout = org_stdout
print('here will be printed on screen, back again!')
