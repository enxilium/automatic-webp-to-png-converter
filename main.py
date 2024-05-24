# Import libraries
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class OnMyWatch:
    # Set directory to be monitored to be downloads folder
    watchDirectory = "C:/Users/enxil/Downloads"
 
    def __init__(self):
        self.observer = Observer()
 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer stopped")
 
        self.observer.join()
 
 
class Handler(FileSystemEventHandler):
 
    @staticmethod
    def on_any_event(event):

        if event.is_directory:
            return None
 
        elif event.event_type == 'created':
            filename = event.src_path.split("\\")[1]
            if filename[-4:] == "webp" or filename[-4:] == "jpg":
                print("Watchdog received webp - % s. Now converting." % event.src_path)
                try:
                    # Delay the procedure to allow Windows to finish processing the download, otherwise there will be an error.
                    time.sleep(1)
                    image = Image.open(event.src_path).convert("RGB")
                    image.save(event.src_path.replace("webp", "png"), "png")

                    print("Conversion complete. Deleting old webp image...")
                    os.remove(event.src_path)
                    print("Old image succesfully removed.")
                except:
                    print("No such file found! Error!")
 
if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()