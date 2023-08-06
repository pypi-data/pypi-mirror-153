import subprocess
import os
import sys

def flasher(sensor_name : str = None):
    BASE_USER = os.path.expanduser('~')
    ESPTOOL = os.path.join(BASE_USER,'.platformio','packages','tool-esptoolpy','esptool.py')

    if os.name == 'nt': # windows
        SCRIPTS = os.path.join(BASE_USER,'.platformio','penv','Scripts')
        #PYTHON = os.path.join(SCRIPTS,'python.exe')
    elif os.name == 'posix': # linux
        BIN = os.path.join(BASE_USER,'.platformio','penv','bin')
        #PYTHON = os.path.join(BIN,'python')
    PYTHON = 'python'

    BASE_TOOLS = os.path.join(BASE_USER,'.platformio','packages','framework-arduinoespressif32','tools')
    BOOTLOADER_DIO_40M = os.path.join(BASE_TOOLS,'sdk','bin','bootloader_dio_40m.bin')
    BOOT_APP0 = os.path.join(BASE_TOOLS,'partitions','boot_app0.bin')

    run_cmd = lambda cmd: subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)

    # get binaries names into a dict for easy indexing
    sketch_binaries = {'firmware':'', 'partitions':''}
    for bin in os.listdir('sketch'): sketch_binaries[bin.split('_')[0]] = os.path.join('sketch',bin) 

    # list number of tasks based in spiffs folder content
    spiffs_binaries = [os.path.join('spiffs',bin) for bin in os.listdir('spiffs')] # list all spiffs binaries

    # iterate over all possible targets based in spiffs folder content
    for spiffs_binary in spiffs_binaries:
        if os.name == 'nt': sensor_id = spiffs_binary.split('\\')[-1].split('_')[0]
        elif os.name == 'posix': sensor_id = spiffs_binary.split('/')[-1].split('_')[0]
        
        choice = input(f"Flash sketch image to sensor %s? [y/N]" % sensor_id)
        if (not choice) or (choice=='n') or (choice=='N'):
            pass
        elif (choice=='Y') or (choice=='y'):
            # flash sketch
            #"C:\Users\USER\.platformio\penv\Scripts\python.exe" "C:\Users\USER\.platformio\packages\tool-esptoolpy\esptool.py" --chip esp32 --port "COM3" --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 C:\Users\USER\.platformio\packages\framework-arduinoespressif32\tools\sdk\bin\bootloader_dio_40m.bin 0x8000 C:\Users\USER\PROJECT\.pio\build\lolin32\partitions.bin 0xe000 C:\Users\USER\.platformio\packages\framework-arduinoespressif32\tools\partitions\boot_app0.bin 0x10000 .pio\build\lolin32\firmware.bin
            #"/home/USER/.platformio/penv/bin/python" "/home/USER/.platformio/packages/tool-esptoolpy/esptool.py" --chip esp32 --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 /home/USER/.platformio/packages/framework-arduinoespressif32/tools/sdk/bin/bootloader_dio_40m.bin 0x8000 /home/USER/PROJECT/.pio/build/lolin32/partitions.bin 0xe000 /home/USER/.platformio/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin 0x10000 .pio/build/lolin32/firmware.bin
            flash_firmware_cmd = f"%s %s --chip esp32 --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 %s 0x8000 %s 0xe000 %s 0x10000 %s" % (PYTHON, ESPTOOL, BOOTLOADER_DIO_40M, sketch_binaries['partitions'], BOOT_APP0, sketch_binaries['firmware'])
            run_cmd(flash_firmware_cmd)
        else: 
            print('Error: invalid choice. Ending script...')
            break

        choice = input(f"Flash spiffs image to sensor %s? [y/N]" % sensor_id)
        if (not choice) or (choice=='n') or (choice=='N'):
            pass
        elif (choice=='Y') or (choice=='y'):
            # flash spiffs
            # "C:\Users\USER\.platformio\penv\Scripts\python.exe" "C:\Users\USER\.platformio\packages\tool-esptoolpy\esptool.py" --chip esp32 --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_size detect 2686976 .pio\build\lolin32\spiffs.bin
            # "/home/USER/.platformio/penv/bin/python" "/home/USER/.platformio/packages/tool-esptoolpy/esptool.py" --chip esp32 --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_size detect 2686976 .pio/build/lolin32/spiffs.bin
            flash_spiffs_cmd = f"%s %s --chip esp32 --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_size detect 2686976 %s" %(PYTHON, ESPTOOL, spiffs_binary)
            run_cmd(flash_spiffs_cmd)
        else: 
            print('Error: invalid choice. Ending script...')
            break

# if __name__ == "__main__":
#     flasher()