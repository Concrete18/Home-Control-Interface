from roku import Roku
import threading
import time

roku = Roku('192.168.0.132')


def Change_to_ABC():
    '''Switches display to the mode entered as an argument. Works for PC and TV mode.'''
    def Callback():
        print('Switching to ABC')
        youtube = roku['YouTube TV']
        youtube.launch()
        time.sleep(10)
        roku.right()
        time.sleep(1)
        for _ in range(2):
            roku.down()
            time.sleep(.5)
        roku.enter()
        if 'YouTube TV' in str(roku.active_app):
            print('Success')
        else:
            input('Roku Failed to switch to ABC on Youtube TV.')
    ABC = threading.Thread(target=Callback)
    ABC.start()


def Check_If_Youtube_TV(obj):
    '''Set Scene Function.

    Args = obj.'''
    if 'YouTube TV' in str(roku.active_app):
        obj.config(relief='sunken')
    else:
        obj.config(relief='raised')
