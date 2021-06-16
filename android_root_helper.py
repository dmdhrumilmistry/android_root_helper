from subprocess import call, check_output
from os.path import join as path_join


def setup_adb():
    pass



def start_adb_server():
    '''
    Starts adb server on the machine.
    '''
    print('[*] Starting ABD SERVER...')
    call('adb start-server', shell=True)


def connected_devices() -> bool:

    connected_devices_output = check_output('adb devices', shell=True)
    print(connected_devices_output.decode())
    user_dev_check = input('[*] did you find your android device in the list? (y/n) : ').lower()

    if user_dev_check == 'y':
        print('[*] Device Connected!!')
        return True
    
    print('[-] Try installing drivers needed to root your android device.')
    return False


def start_custom_recovery_flash():
    '''
    starts recovery flashing process.
    '''
    pass





start_adb_server()
connected_devices()

