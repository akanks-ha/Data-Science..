# q1
# print("""Twinkle twinkle little star.
# How I wonder what you are.
# Up above the world so high.
# Like a diamond in the sky.
# Twinkle twinkle little star.
# How I wonder what you are.

# Twinkle twinkle little star.
# How I wonder what you are.
# Up above the world so high.
# Like a diamond in the sky.
# Twinkle twinkle little star.
# How I wonder what you are.""")

#q3 python text to speak
# import pyttsx3
# engine = pyttsx3.init()
# engine.say("Hello Ayu")
# engine.say("Hello Aku")
# engine.runAndWait() 

# q4
import os

# specify the directory you want to list
directory_path = '/Users/akankshanupadhyay/Desktop'

# List all files and directories in the specified path
contents = os.listdir(directory_path)

# print each file and directory name
for item in contents:
    print(item)