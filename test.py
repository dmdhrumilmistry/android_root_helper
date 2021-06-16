from subprocess import call, check_output
from os.path import join, isdir, isfile
from os import error, getcwd, environ, pathsep
from time import sleep


adb_dir_name = 'minimal_abd_and_fastboot'
curr_dir = getcwd()
recovery_name = 'recovery.img'

  
def check_recovery_image()->bool:
    '''
    checks if recovery image is present in the directory.
    '''
    if isfile(recovery_name):
        print('[*] Found Custom Recovery image.')
        return True
    
    print("[-] No custom recovery image found. Don't to rename custom recovery image as recovery.img")
    print('[-] Cannot proceed further. Exiting Program...')
    quit()


if check_recovery_image():
    recovery_path = join(curr_dir, recovery_name)
    print('[*] Recovery found on this location: \n')
    print(recovery_path)

else:
    print('recovery not found')