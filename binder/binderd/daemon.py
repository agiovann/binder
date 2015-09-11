from multiprocessing import Process
from threading import Thread

import zmq
from zmq.eventloop.ioloop import IOLoop

from mdp import MDPBroker

from binder.settings import BinderDSettings
import binder.binderd.modules as modules
from binder.binderd.client import BinderClient

class BinderDProcess(Process):

    class Broker(MDPBroker):
        pass

    class ControlThread(Thread):

        def __init__(self, binderd):        
            self.binderd = binderd
            self._stopped = False

        def _process_control_msg(self):
            pass
            
        def run(self):
            while not self._stopped:
                self._process_control_msg()

    def run(self):
        # launch the control thread
        control = BinderDProcess.ControlThread(self) 
        control.start()

        # start all submodules
        for module in modules:
            clazz = modules[module]
            instance = clazz()
            instance.start()

        # start the MDP broker
        context = zmq.Context()
        url = "{0}:{1}".format(BinderDSettings.BROKER_HOST, BinderDSettings.BROKER_PORT)
        broker = BinderDProcess.Broker(context, url)
        IOLoop.instance().start()
        broker.shutdown()

    def stop(self):
        # stop all submodules
        # stop the control/broker sockets
        pass
   
def start_daemon():
    # start the binderd process (by creating a process)
    BinderDProcess().start()
   
def stop_daemon():
    # stop the binderd process (by sending a 'stop' message to the control socket):
    with BinderClient() as client:
        client.stop_daemon()

def stop_module(name):
    with BinderClient as client:
        client.stop_daemon()




