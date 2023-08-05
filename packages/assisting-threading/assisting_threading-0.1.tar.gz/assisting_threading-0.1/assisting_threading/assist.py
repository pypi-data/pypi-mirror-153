from threading import Thread, active_count
import threading

class CurrentThread(Thread):
    def current_thread(self) -> Thread:
        self.t: Thread = [thread for thread in threading.enumerate()] if active_count() in [1] else None
        return self.t[0]
        
class Assistant(CurrentThread):
    def __init__(self, thread=CurrentThread().current_thread()) -> None:
        self.thread: Thread = thread[0] if not isinstance(thread, Thread) else thread
        
    def __str__(self) -> str:
        if isinstance(self.thread, (Thread, object)):
            return f"Speeding Up Thread -> {str(self.thread.name)}" if str(self.thread.name) is not None else f"Not Speeding Up Any Thread"
        return f"Not Speeding Up Any Thread"
        
    def __repr__(self) -> any:
        if isinstance(self.thread, (Thread, object)):
            return f"Assistant({str(self.thread)})" if str(self.thread.name) is not None else None
        return None

