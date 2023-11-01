from subprocess import Popen, PIPE, STDOUT
from os import system
from multiprocessing import Process


def nb_run():
    system(r'.\venv\Scripts\activate & nb run')


def go_cqhttp():
    system('cd "./LittlePaimon-Bot/go-cqhttp" & go-cqhttp.exe')


# def retrieve_url(cmds):
#     system(cmds)


if __name__ == '__main__':
    # commands = [r'..\venv\Scripts\activate & nb run', 'cd "./LittlePaimon/LittlePaimon-Bot/go-cqhttp" & go-cqhttp.exe']
    # pool = Pool(2)
    # pool.map(retrieve_url, commands)
    # p1 = Process(target=go_cqhttp)
    p2 = Process(target=nb_run)
    # p1.start()
    p2.start()
    # p1.join()
    p2.join()
    print('all done!')
    # bot.run(use_reloader=False, loop=asyncio.get_event_loop())
