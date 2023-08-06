"""Main module."""


#pylint:disable=W0221
from typing import List

from threading import Lock, Event

from telegram.ext import Updater




class ExtUpdater(Updater):
    
    def __init__(self, token:str):
        super().__init__(token)
        
        self.__lock = Lock()
        self.__threads = []
       
        
        
    def start_webhook(
        self,
        webhook_url: str = None,
        allowed_updates: List[str] = None,
        force_event_loop: bool = None,
        drop_pending_updates: bool = False,
        ip_address: str = None,
        max_connections: int = 40,
    ):
        
       with self.__lock:
            if not self.running:
                self.running = True

                # Create & start threads
                #webhook_ready = Event()
                dispatcher_ready = Event()
                self.job_queue.start()
                self._init_thread(self.dispatcher.start, "dispatcher", dispatcher_ready)
                
                dispatcher_ready.wait()

                # Return the update queue so the main thread can insert updates
                return self.update_queue
            return None
        
        
   