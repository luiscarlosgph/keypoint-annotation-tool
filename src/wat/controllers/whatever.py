#!/usr/bin/python
#
# @brief  This module and class represent a singleton controller.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2021.

import threading
import apscheduler.schedulers.background

# My imports
# TODO

class Whatever(object):
    """
    @class that keeps the database updated. It is a Singleton.
    """
    class __Controller: 
        def __init__(self, db_path):
            self.db_path = db_path
            self.working = False
            self.thread = None
            
            # Start scheduler for async jobs 
            self.sched = apscheduler.schedulers.background.BackgroundScheduler()
            self.sched.start()
            
            # TODO: launch every day at 22:00, for example
            #self.sched.add_job(self.run, 'cron', hour=22, minute=0)

        def _threaded_run(self):
            """@brief Do whatever in a separate thread."""
            self.working = True

            # TODO: Do somthing
            
            self.working = False

        def run(self):
            """
            @brief   Runs an update is one is not already running.
            @returns True if the update can start successfully. Otherwise,
                     returns False.
            """
            if self.working:
                return False
            
            # Launch a thread to do the update
            self.thread = threading.Thread(target=self._threaded_run)
            self.thread.start()

            return True
        
    # Singleton implementation for the Controller class 
    instance = None
    def __init__(self, db_path):
        if Whatever.instance is None:
            Whatever.instance = Whatever.__Controller(db_path)
        else:
            if Whatever.instance.db_path == db_path:
                pass # Same database, nothing to do
            else:
                raise NotImplemented()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
    
    def run(self):
        return Whatever.instance.run()


if __name__ == "__main__":
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
