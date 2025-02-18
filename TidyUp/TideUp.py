import os
import shutil

current_folder = os.getcwd()

for filename in os.listdir(current_folder):
    if filename != "TidyUp.py":             # Skip this python file
        if os.path.isfile(filename):        # Check if file to ignore folders
            extension = os.path.splitext(filename)[1][1:]
        
            if extension:                   # Ingore files without extensions
                if not os.path.exists(extension):
                    os.mkdir(extension)

                shutil.move(filename, os.path.join(extension, filename))
