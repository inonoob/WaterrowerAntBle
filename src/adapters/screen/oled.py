import threading
from time import sleep
from globalParameters import globalParameters
from setupHandler import device, shutdown
import time
import signal
import screens.mainmenu
import screens.pirowflosettings
import screens.buttonhelp
import screens.emptyscreen



updaterun = threading.Event()

Mainlock = threading.Lock()


class Graceful:

    def __init__(self):
        self.run = True
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        Mainlock.acquire()
        self.run = False
        Mainlock.release()

grace = Graceful()

while grace.run:
    try:
        sleep(0.2)

        if time.time() - globalParameters.lastbuttonpressed >= 10:
            globalParameters.blackscreen = True
            screens.emptyscreen.draw(device)


        elif globalParameters.activemenu == 0:
            screens.mainmenu.draw(device)

        elif globalParameters.activemenu == 1:
            screens.pirowflosettings.draw(device)

        elif globalParameters.activemenu == 2:
            screens.buttonhelp.draw(device)

        #Send trigger event to active screen
        if globalParameters.trigger == True:
            globalParameters.trigger = False
            if globalParameters.blackscreen == True:
                screens.emptyscreen.trigger(device)
            else:
                if globalParameters.activemenu == 0: screens.mainmenu.trigger()
                elif globalParameters.activemenu == 1: screens.pirowflosettings.trigger()
                elif globalParameters.activemenu == 2: screens.buttonhelp.trigger()


        sleep(0.2)
    except KeyboardInterrupt:
        print("Exiting...")
        break

updaterun.set() #Stop screen update procedure
shutdown()