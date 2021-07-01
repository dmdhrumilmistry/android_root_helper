from subprocess import call, check_output
from os.path import join, isdir, isfile
from os import error, getcwd, environ, pathsep
from time import sleep


adb_dir_name = 'minimal_adb_and_fastboot'
curr_dir = getcwd()
recovery_name = 'recovery.img'
magisk_file_name = 'Magisk-v23.0.zip'

  
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


def transfer_magisk_zip()->bool:
    '''
    transfers the magisk manager zip to internal storage.
    '''
    source = join(curr_dir, magisk_file_name)
    destination = '/sdcard/'
    try:
        file_transfer_output = check_output('adb push {} {}'.format(source, destination), shell=True).decode()
        print(file_transfer_output)

    except Exception :
        print('[-] Exception Occurred while transferring Magisk Manager. Due to error you cannot move further but you can manually transfer and install zip.')
        print('Exception : ', Exception)


if check_recovery_image():
    recovery_path = join(curr_dir, recovery_name)
    print('[*] Recovery found on this location: \n')
    print(recovery_path)

else:
    print('recovery not found')