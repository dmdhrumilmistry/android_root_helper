from subprocess import call, check_output
from os.path import join, isdir, isfile
from os import error, getcwd, environ, pathsep
from time import sleep
import colorama
from colorama import Style, Fore


colorama.init(autoreset=True)

adb_dir_name = 'minimal_adb_and_fastboot'
recovery_name = 'recovery.img'
magisk_file_name = 'Magisk-v23.0.zip'
curr_dir = getcwd()
YELLOW_BRIGHT = Fore.YELLOW + Style.BRIGHT
WHITE_BRIGHT = Fore.WHITE + Style.BRIGHT
RED_BRIGHT = Fore.RED + Style.BRIGHT


def pre_requisites():
    if isfile('pre-requisites.txt'):
        with open('pre-requisites.txt','r') as f:
            important_lines = f.readlines()
            for line in important_lines:
                print(YELLOW_BRIGHT + line, end='')
        
        f.close()   
    
    else:
        print(RED_BRIGHT + '[*] pre-requisites.txt not found. Cannot proceed Further, download this software again.')


def setup_adb()->bool:
    '''
    performs required tasks to setup adb on the windows machine.
    Sets environment variable for minimal adb and fastboot.
    '''
    
    if isdir(adb_dir_name):
        adb_env_path = join(curr_dir, adb_dir_name)
    
        environ["PATH"] += pathsep + adb_env_path
        if adb_env_path in environ["PATH"]:
            print(WHITE_BRIGHT + '[*] Minimal ADB and Fastboot has been added to environment variable path successfully.')
            print(WHITE_BRIGHT + '[*] Checking if ADB is working!')
            check_adb_version =check_output('adb --version', shell=True).decode()
            print(check_adb_version)
            user_check = input('Can you see any abd version installed? (y/n) : ').lower()
            if user_check == 'y':
                print(WHITE_BRIGHT + '[+] ADB installed successfully!')
                return True
        else:
            print(RED_BRIGHT + '[-] Something went wrong while adding Minimal ADB and Fastboot to environment variable path.')
            quit()

    else:
        print(RED_BRIGHT + '[-] Minimal ABD and Fastboot folder is missing, please clone/download the repository again.')
        quit()


def start_adb_server():
    '''
    Starts adb server on the machine.
    '''
    print( YELLOW_BRIGHT + "\n[*] Important : if you're prompted to allow debugging, then tick *Always allow from this computer* and press ok.")
    print(WHITE_BRIGHT + '[*] Starting ADB SERVER...')
    call('adb start-server', shell=True)


def connected_devices() -> bool:
    '''
    checks the devices detected and connected by the windows machine.
    '''

    connected_devices_output = check_output('adb devices', shell=True)
    print(connected_devices_output.decode())
    user_dev_check = input(YELLOW_BRIGHT + '[*] did you find your android device in the list? (y/n) : ').lower()

    if user_dev_check == 'y':
        print(WHITE_BRIGHT + '[*] Device Connected!!')
        return True
    
    print(RED_BRIGHT + '[-] Try installing drivers needed to root your android device.')
    return False


def start_custom_recovery_flash()->True:
    '''
    starts recovery flashing process.
    '''

    def check_recovery_image()->bool:
        '''
        checks if recovery image is present in the directory.
        '''
        if isfile(recovery_name):
            print(WHITE_BRIGHT + '[*] Found Custom Recovery image.')
            return True
        
        print(RED_BRIGHT + "[-] No custom recovery image found. Don't to rename custom recovery image as recovery.img")
        print(RED_BRIGHT + '[-] Cannot proceed further. Exiting Program...')
        quit()

    try: 

        if check_recovery_image():
            recovery_path = join(curr_dir, recovery_name)

            adb_reboot_bootloader_output = check_output('adb reboot bootloader').decode()
            print(adb_reboot_bootloader_output)
            sleep(2)
            
            input(YELLOW_BRIGHT + '[*] Important Step : Press any key after placing your custom recovery image file inside this folder, by renaming it to recovery.img if not done yet!')
            
            print(WHITE_BRIGHT + '[*] Flashing Recovery.')
            fastboot_flash_output = check_output('fastboot flash recovery {}'.format(recovery_path)).decode()
            print(fastboot_flash_output)
            sleep(2)

            print(WHITE_BRIGHT + '[*] Rebooting into bootloader mode.')
            fastboot_reboot_bootloader_output = check_output('fastboot reboot-bootloader').decode()
            print(fastboot_reboot_bootloader_output)
            sleep(2)

            print(WHITE_BRIGHT + '[*] Erasing Cache.')
            fastboot_erase_cache_output = check_output('fastboot erase cache').decode()
            print(fastboot_erase_cache_output)
            sleep(2)

    except Exception as e:
        print(RED_BRIGHT + '[-] An Exception Occurred')
        return False

    finally:
        print(WHITE_BRIGHT + '[*] Rebooting device into fastboot mode.')
        fastboot_reboot_output = check_output('fastboot reboot').decode()
        print(fastboot_reboot_output)
        sleep(2)

        return True
        

def transfer_magisk_zip()->bool:
    '''
    transfers the magisk manager zip to internal storage.
    '''
    source = join(curr_dir, magisk_file_name)
    destination = '/sdcard/'
    try:
        print(WHITE_BRIGHT + '[*] Starting File Transfer')
        file_transfer_output = check_output('adb push {} {}'.format(source, destination), shell=True).decode()
        print(file_transfer_output)
        return True
    except Exception :
        print(RED_BRIGHT + '[-] Exception Occurred while transferring Magisk Manager. Due to error you cannot move further but you can manually transfer and install zip.')
        print(RED_BRIGHT + 'Exception : ', Exception)
        return False

def adb_reboot_recovery()->bool:
    '''
    reboots android device into recovery.
    '''
    try:
        print(WHITE_BRIGHT + '[*] Rebooting device into recovery mode.')
        recovery_reboot_output = check_output('adb reboot recovery', shell=True).decode()
        print(recovery_reboot_output)
        sleep(5)

    except Exception :
        print(RED_BRIGHT + '[-] Exception occured while rebooting into recovery.')
        return False
    
    return True


pre_requisites()
setup_adb()
start_adb_server()
connected_devices()
if start_custom_recovery_flash():
    print(WHITE_BRIGHT + '[*] Custom image flashed sucessfully.')
    print('-'*40)

    print(WHITE_BRIGHT + '[*] Starting to transfer magisk to sd card.')
    print(YELLOW_BRIGHT + '[*] press Ctrl+C simultaneously to tranfer files manually to sdcard.')
    print(WHITE_BRIGHT + '[*] Waiting For Device to detect...')
    
    sleep(15)
    # continue to check if device if not connected.
    while not connected_devices():
        if transfer_magisk_zip():
            print(WHITE_BRIGHT + '[+] Files Transferred successfully.')
            print('-'*40)
            print(WHITE_BRIGHT + '[*] Rebooting into Recovery, install the magisk zip from the sdcard.')
            sleep(5)
        
        
    
    if adb_reboot_recovery():
        print(YELLOW_BRIGHT + '[*] Now follow instruction Install->Select Storage-> Sd Card-> locate and choose Magisk zip-> swipe to install zip')
        print(YELLOW_BRIGHT + '[*] After successfull installation reboot your android device. First Reboot may take some time to boot. Do not interrupt while your android device is booting.')
        print(WHITE_BRIGHT + '[*] Voila!! Now your android device is rooted..')

else:
    print(RED_BRIGHT + '[-] Failed to install custom image. Please try again after installing requirements.')
