import subprocess
import os
import glob
import shutil
import re
import sys
    
def handle_verbose(verbose):
    content = ''.join(verbose)
    index = content.find('Building in release mode')
    print(content[index:])

def config_txt_string(targ):
    """
    config.txt
    id=ge120
    actual_spiffs_version=1.0.7
    next_spiffs_version=1.0.8
    spiffs_version=10.07
    """
    str_ = f"id=%s\n" \
            "actual_spiffs_version=%s\n" \
            "next_spiffs_version=%s\n" \
            "spiffs_version=%f" \
            % tuple(targ)
    return str_

def builder():
    BASE_USER = os.path.expanduser('~')

    # if os.name == 'nt': # windows
    #     PIO = PLATFORMIO = os.path.join(BASE_USER,'.platformio','penv','Scripts','platformio.exe')
    # elif os.name == 'posix': # linux
    #     PIO = PLATFORMIO = os.path.join(BASE_USER,'.platformio','penv','bin','pio')
    PIO = 'pio'

    run_cmd = lambda cmd: subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)

    # read manifest file
    manifest = open('manifest', 'r')
    lines = manifest.readlines()
    build_targ = [line.replace('\n','').split('@') for line in lines]
    manifest.close()

    # read ota_config.h file to get sketch actual version
    path = os.path.join('firmware','include','ota_config.h')
    ota_config = open(path, 'r')
    content = ota_config.readlines()
    ota_config.close()
    matched_line = ''.join([line for line in content if "ACTUAL_VERSION_SKETCH" in line])
    sketch_version = ''.join(re.findall(r'"([^"]*)"', matched_line))

    # read platformio.ini file to get target board
    path = os.path.join('firmware','platformio.ini')
    ini = open(path, 'r')
    content = ini.readlines()
    ini.close()
    matched_line = ''.join([line for line in content if "board" in line])
    BOARD =  re.search('board = (.*)\n', matched_line).group(1)

    # generate config.txt content based in manifest file
    for targ in build_targ:
        index = build_targ.index(targ)
        sensor, actualVer = targ

        # parse next version
        nextVer = actualVer.split('.')
        nextVer[-1] = str(int(nextVer[-1])+1)
        nextVer = '.'.join(nextVer)
        build_targ[index].append(nextVer)

        # parse numeric version
        numVer = actualVer.split('.')
        numVer = float(int(numVer[0])*1e1 + int(numVer[1])*1e0 + int(numVer[2])*1e-2)
        build_targ[index].append(numVer)

    # get existing geXYZ.txt sensor configuration files in data folder
    data_files = os.listdir('data') # list all data files 
    data_files_names = [file.split('.')[0] for file in data_files] # extract name without extension

    for targ in build_targ:
        if targ[0] in data_files_names:
            # clean all content in firmware/data folder
            PATH_TO_CLEAN = os.path.join('firmware','data','**','*')
            files = glob.glob(PATH_TO_CLEAN, recursive=True)
            for f in files:
                try:
                    os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))

            # write config.txt file into firmware/data folder
            PATH_TO_CONFIGF = os.path.join('firmware','data','config.txt')
            config_file = open(PATH_TO_CONFIGF, 'w+') 
            config_file.write(config_txt_string(targ))
            config_file.close()

            # copy geXYZ.txt sensor configuration files to firmware/data folder
            SRC_PATH = os.path.join('data',f'%s.txt' % targ[0])
            DST_PATH = os.path.join('firmware','data',f'%s.txt' % targ[0])
            shutil.copy(SRC_PATH, DST_PATH)

            # build filesystem image
            build_spiffs_cmd = f"%s run --target buildfs --environment %s -d firmware" % (PIO,BOARD)
            #handle_verbose(run_cmd(build_spiffs_cmd)) # -s to silent
            run_cmd(build_spiffs_cmd) # -s to silent
            print()

            # copy spiffs binary to spiffs root folder
            SRC_PATH = os.path.join('firmware','.pio','build',BOARD,'spiffs.bin')
            DST_PATH = os.path.join('spiffs','%s_%s.spiffs.bin' % (targ[0], targ[1]))
            shutil.copy(SRC_PATH, DST_PATH)

        else: print(f'No %s.txt sensor configuration file found.\n' % targ[0])

    # build sketch image
    build_sketch_cmd = "%s run -d firmware" % PIO
    #handle_verbose(run_cmd(build_sketch_cmd)) # -s to silent
    run_cmd(build_sketch_cmd) # -s to silent
    print()

    # copy sketch binaries to sketch root folder

    # firmware
    SRC_PATH = os.path.join('firmware','.pio','build',BOARD,'firmware.bin')
    DST_PATH = os.path.join('sketch','firmware_%s.ino.esp32.bin' % sketch_version)
    shutil.copy(SRC_PATH, DST_PATH)

    # partitions
    SRC_PATH = os.path.join('firmware','.pio','build',BOARD,'partitions.bin')
    DST_PATH = os.path.join('sketch','partitions_%s.ino.esp32.bin' % sketch_version)
    shutil.copy(SRC_PATH, DST_PATH)

# if __name__ == "__main__":
#     builder()