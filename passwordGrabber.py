from os import popen, geteuid
from os.path import getsize
from sys import platform


class PasswordGrabber:
    def __init__(self):
        self.check_system()
        pass

    def Password_win32(self):
        # first command to get all interfaces
        get_profile = popen("netsh wlan show profile")
        interface = list(get_profile)
        inter = []
        # in all interface grap ALL user Profile
        for value in interface:
            if "All User" in value:
                # spliting response
                val = value.split(":")
                # appendind in inter
                inter.append(val[1])
        if len(inter) == 0:
            print("\n<---- No Profiles ---->\n")
        # now we got the all interfaces
        else:
            print("\n<----Wifi Password----->\n")

            for interface in inter:
                creds = popen(
                    f'netsh wlan show profile "{interface.strip()}" key=clear')
                # time for password
                for password in creds:
                    if "Key Content" in password:
                        value = password.split(":")

                        print(f"{interface.strip()} --> {value[1]}")

    def password_linux(self):
        PATH = "/etc/NetworkManager/system-connections/"
        # checking for sudo user
        if geteuid() == 0:
            get_profile = popen(f"ls {PATH}")

            interface = []
            for line in get_profile.readlines():
                if ".nmconnection" in line:
                    interface.append(line.strip())
                # interface.append(splitLine)
            if len(interface) == 0:
                print("\n<---- No Profiles ---->\n")

            else:

                print("\n<----Wifi Password----->\n")
                for creds in interface:
                    # checking con file is not empty
                    if getsize(PATH+creds)==0:
                        print(f"\n<----- {creds} file is Empty ------->\n")
                    else:
                        get_pass = popen(
                            f'sudo cat "{PATH}{creds}"')
                        for line in get_pass:
                            if "psk=" in line:
                                password = line.split("=")
                                print(creds, "--> ", password[1])

        else:
            print("\n<----- Use Sudo Before Excuteing------>\n")

     # for checking the system
    def check_system(self):
        system = platform
        if system.lower().strip() == "win32":
            self.Password_win32()
        elif system.lower().strip() == "linux":
            self.password_linux()


Grab = PasswordGrabber()
