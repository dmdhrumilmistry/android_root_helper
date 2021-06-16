from subprocess import call, check_output
from os.path import join, isdir, isfile
from os import error, getcwd, environ, pathsep
from time import sleep


adb_dir_name = 'minimal_abd_and_fastboot'
curr_dir = getcwd()
recovery_name = 'recovery.img'


def pre_requisites():
    if isfile('pre-requisites.txt'):
        with open('pre-requisites.txt','r') as f:
            important_lines = f.readlines()
            for line in important_lines:
                print(line, end='')
        
        f.close()   
    
    else:
        print('[*] pre-requisites.txt not found. Cannot proceed Further, download this software again.')


def setup_adb()->bool:
    '''
    performs required tasks to setup adb on the windows machine.
    Sets environment variable for minimal adb and fastboot.
    '''
    
    if isdir(adb_dir_name):
        adb_env_path = join(curr_dir, adb_dir_name)
    
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
    '''
    checks the devices detected and connected by the windows machine.
    '''

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

    try: 

        if check_recovery_image():
            recovery_path = join(curr_dir, recovery_name)

            adb_reboot_bootloader_output = check_output('adb reboot bootloader').decode()
            print(adb_reboot_bootloader_output)
            sleep(2)
            
            input('[*] Important Step : Press any key after placing your custom recovery image file inside this folder, by renaming it to recovery.img')
            
            fastboot_flash_output = check_output('fastboot flash recovery {}'.format(recovery_path)).decode()
            print(fastboot_flash_output)
            sleep(2)

            fastboot_reboot_bootloader_output = check_output('fastboot reboot-bootloader').decode()
            print(fastboot_reboot_bootloader_output)
            sleep(2)

            fastboot_erase_cache_output = check_output('fastboot erase cache').decode()
            print(fastboot_erase_cache_output)
            sleep(2)

    except Exception as e:
        print('[-] An Exception Occurred')
        return False

    finally:
        fastboot_reboot_output = check_output('fastboot reboot').decode()
        print(fastboot_reboot_output)
        sleep(2)
        

pre_requisites()
setup_adb()
start_adb_server()
connected_devices()
start_custom_recovery_flash()
