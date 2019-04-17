import wuy

class helloWorld(wuy.Window):
    """ <button onclick="wuy.beep()">BEEP</button> """
    size=(100,100)

    def beep(self):
        print("\a BEEP !!!")

helloWorld()