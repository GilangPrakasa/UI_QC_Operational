import sys
import re
import os
from datetime import datetime

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

class StdoutRedirector:
    def __init__(self, filename=None):
        self.terminal = sys.stdout
        self.filename = filename or self.generate_filename()
        self.log = open(self.filename, "a")

    def generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"dump_{timestamp}.txt"

    def update_filename(self, new_filename):
        self.filename = new_filename
        self.log.close()
        self.log = open(self.filename, "a")

    def write(self, message):
        global data
        data = ansi_escape.sub('', message)
        self.terminal.write(message)
        self.log.write(data)
        self.log.flush()
        os.fsync(self.log.fileno())

    def flush(self):
        pass


import sys
import re
from datetime import datetime

class StdoutRedirector:
    def __init__(self):
        self.terminal = sys.stdout
        self.log_filename = self.generate_log_filename()
        self.log = open(self.log_filename, "a")

    def generate_log_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"dump_{timestamp}.txt"

    def write(self, message):
        # Assuming ansi_escape is defined elsewhere in your code
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        global data
        data = ansi_escape.sub('', message)
        
        self.terminal.write(message)
        
        if self.log.closed:
            # If the log file is closed, open a new one
            self.log_filename = self.generate_log_filename()
            self.log = open(self.log_filename, "a")

        self.log.write(data)

    def close(self):
        self.log.close()

# Example usage:
# Redirect standard output to the custom class
sys.stdout = StdoutRedirector()

# Your code that produces output
print("Hello, this will be logged to a new file (dump_timestamp.txt)")

# Close the log file when done
sys.stdout.close()
