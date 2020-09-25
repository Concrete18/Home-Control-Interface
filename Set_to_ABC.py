from roku import Roku
import time
import os

roku = Roku('192.168.0.131')


def Change_to_ABC():
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


def Check_If_Youtube_TV():
    if 'YouTube TV' in str(roku.active_app):
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        Change_to_ABC()
    except:
        input('Connection Failed. Check IP Address.')