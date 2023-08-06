import os

def init():
    os.mkdir('data')
    os.mkdir('firmware')
    os.mkdir('sketch')
    os.mkdir('spiffs')

    f = open(os.path.join('README.md'), 'w+')
    str_ = f""
    str_ += f"- data/: Folder where the geXYZ.txt files should be located to feed the scripts.\n"
    str_ += f"- firmware/: Folder where the platformio arduino-esp32 project should be located.\n"
    str_ += f"- sketch/: Folder where the binaries regarding the sketch will be outputted, i.e partition.bin and firmware.bin.\n"
    str_ += f"- spiffs/: Folder where the binaries regarding the SPIFFS will be outputted, i.e. geXYZ.bin files for each target.\n"
    str_ += f"- /: Root folder of project where the manifest file should be located so as the Python scripts.\n"
    f.write(str_)
    f.close()

    f = open(os.path.join('manifest'), 'w+')
    f.write('')
    f.close()

# if __name__ == "__main__":
#     init()