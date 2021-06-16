from subprocess import call, check_output
from os.path import join, isdir
from os import getcwd, environ, pathsep


def pre_requisites():
    print('''
    
    Android Root Helper, Written By Dhrumil Mistry.

    Please make sure, you have required files and softwares installed before proceeding.
    1. Python 3.x.x
    2. USB and Universal ADB/ADB drivers installed for your device on this windows machine.
    3. Custom Recovery image for your android device like TWRP, CWM, etc.
    4. Enough charge on your devices.
    5. Patience 🙂

    Note: I'm not responsible for any damage to your device, This software comes with absolutely 
    no guarantee and warranty. You're completely responsible for your actions.
    If you use this software/script you agree to all my terms and conditions.
    this software doesn't collect any data from your device.

    If you face any issues, do consider opening an issue on the repo.
    
    ''')

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
            user_check = input('Can you see any abd version installed? (y/n) : ').lower()
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
    print("\n[*] Important : if you're prompted to allow debugging, then tick *Always allow from this computer* and press ok.")
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
    adb_reboot_bootloader = check_output('adb reboot bootloader').decode()
    print(adb_reboot_bootloader)
    
    print('[*] Important Step : Press any key after placing your custom recovery image file inside this folder, by renaming it to recovery.img')



pre_requisites()
setup_adb()
start_adb_server()
connected_devices()
