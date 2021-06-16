from subprocess import call, check_output
from os.path import join, isdir
from os import getcwd, environ, pathsep


def setup_adb()->bool:
    '''
    performs required tasks to setup adb on the windows machine.
    Sets environment variable for minimal adb and fastboot.
    '''
    adb_dir = 'minimal_abd_and_fastboot'
    curr_dir = getcwd()

    if isdir(adb_dir):
        adb_env_path = join(curr_dir, adb_dir)
    
        environ["PATH"] += pathsep + adb_env_path
        if adb_env_path in environ["PATH"]:
            print('[*] Minimal ADB and Fastboot has been added to environment variable path successfully.')
            print('[*] Checking if ADB is working!')
            check_adb_version =check_output('adb --version', shell=True).decode()
            print(check_adb_version)
            user_check = input('Can you see any abd version installed? (y/n)').lower()
            if user_check == 'y':
                print('[+] ADB installed successfully!')
                return True
        else:
            print('[-] Something went wrong while adding Minimal ADB and Fastboot to environment variable path.')
            quit()

    else:
        print('[-] Minimal ABD and Fastboot folder is missing, please clone/download the repository again.')
        quit()


def start_adb_server():
    '''
    Starts adb server on the machine.
    '''
    print('[*] Starting ADB SERVER...')
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



setup_adb()

# start_adb_server()
# connected_devices()

