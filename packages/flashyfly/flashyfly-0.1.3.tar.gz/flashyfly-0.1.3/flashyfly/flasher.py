import typer
import subprocess
import os
import sys
import re

def flasher(sensor_name : str = None, sensor_spiffs_version : str = None, sensor_sketch_version : str = None):
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

    sketch_list_dir = os.listdir('sketch')
    spiffs_list_dir = os.listdir('spiffs')

    # get unique sketch versions
    ver = []
    for elem in sketch_list_dir: 
        ver_group = re.search('firmware_(.*).ino.esp32.bin', elem)
        if ver_group: ver.append(ver_group.group(1))
    unique_sketch_ver = list(set(ver))
    
    # get unique spiffs versions and check sensor name
    ver = []
    nam = []
    for elem in spiffs_list_dir: 
        nam_group = re.search('(.*)_', elem)
        ver_group = re.search('_(.*).spiffs.bin', elem)
        if ver_group: ver.append(ver_group.group(1))
        if nam_group: nam.append(nam_group.group(1))
    unique_spiffs_ver = list(set(ver))
    unique_names = list(set(nam))

    # check if sensor name exists and filter binaries to it
    if sensor_name:
        if sensor_name not in unique_names:
            typer.echo('Error: Sensor name was not found in binaries list..')
            raise typer.Exit()
        else:
            new_spiffs_list_dir = []
            for elem in spiffs_list_dir:
                if re.search(sensor_name+'_', elem): new_spiffs_list_dir.append(elem)
            spiffs_list_dir = new_spiffs_list_dir.copy()
    
    # check if sketch version exists and filter binaries to it
    if sensor_sketch_version:
        if sensor_sketch_version not in unique_sketch_ver:
            typer.echo('Error: Sketch version was not found in binaries list.')
            raise typer.Exit()
        else:
            new_sketch_list_dir = []
            for elem in sketch_list_dir:
                if re.search(sensor_sketch_version+'.ino.esp32.bin', elem): new_sketch_list_dir.append(elem)
            sketch_list_dir = new_sketch_list_dir.copy()

    # check if spiffs version exists and filter binaries to it
    if sensor_spiffs_version:
        if sensor_spiffs_version not in unique_spiffs_ver:
            typer.echo('Error: SPIFFS version was not found in binaries list.')
            raise typer.Exit()
        else:
            new_spiffs_list_dir = []
            for elem in spiffs_list_dir:
                if re.search(sensor_spiffs_version+'.spiffs.bin', elem): new_spiffs_list_dir.append(elem)
            spiffs_list_dir = new_spiffs_list_dir.copy()
    
    # get binaries names into a dict for easy indexing
    sketch_binaries = {'firmware':'', 'partitions':''}
    for bin in sketch_list_dir: sketch_binaries[bin.split('_')[0]] = os.path.join('sketch',bin) 

    # list number of tasks based in spiffs folder content
    spiffs_binaries = [os.path.join('spiffs',bin) for bin in spiffs_list_dir] # list all spiffs binaries

    # iterate over all possible targets based in spiffs folder content
    for spiffs_binary in spiffs_binaries:
        if os.name == 'nt': sensor_id = spiffs_binary.split('\\')[-1].split('_')[0]
        elif os.name == 'posix': sensor_id = spiffs_binary.split('/')[-1].split('_')[0]
        
        sketch_ver = sketch_binaries['firmware'].split('_')[-1].split('.ino.esp32.bin')[0]
        spiffs_ver = spiffs_binary.split('_')[-1].split('.spiffs.bin')[0]

        choice = input(f"Flash sketch image v.%s to sensor %s? [y/N]" % (sketch_ver, sensor_id))
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

        choice = input(f"Flash spiffs image v.%s to sensor %s? [y/N]" % (spiffs_ver, sensor_id))
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