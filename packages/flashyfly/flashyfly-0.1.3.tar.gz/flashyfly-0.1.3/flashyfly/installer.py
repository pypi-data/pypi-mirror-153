import subprocess
import sys

def installer():

    run_cmd = lambda cmd: subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)
    install_tools_cmd = "pio platform install espressif32 --with-package framework-arduinoespressif32"
    run_cmd(install_tools_cmd) # -s to silent
    print()

# if __name__ == "__main__":
#     installer()