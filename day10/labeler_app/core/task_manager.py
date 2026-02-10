import threading
import time
from typing import Callable, Optional
from ..utils.logger import app_logger

class TaskManager:
    """Manages background tasks to prevent UI freezing."""
    
    def __init__(self):
        self._current_task: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._is_running = False
        
    def start_task(self, target: Callable, args: tuple = (), on_complete: Callable = None):
        """Starts a new background task."""
        if self._is_running:
            app_logger.warning("Task already running. Stopping it first.")
            self.stop_task()
            
        self._stop_event.clear()
        self._is_running = True
        
        def wrapper():
            result = None
            try:
                result = target(self._stop_event, *args)
            except Exception as e:
                app_logger.error(f"Task failed: {e}")
            finally:
                self._is_running = False
                if on_complete:
                    try:
                        on_complete(result)
                    except TypeError:
                        on_complete()
                    
        self._current_task = threading.Thread(target=wrapper, daemon=True)
        self._current_task.start()
        app_logger.info("Background task started.")

    def stop_task(self):
        """Signals the current task to stop."""
        if self._is_running:
            self._stop_event.set()
            if self._current_task:
                 self._current_task.join(timeout=1.0)
            self._is_running = False
            app_logger.info("Background task stopped.")

    @property
    def is_running(self):
        return self._is_running
