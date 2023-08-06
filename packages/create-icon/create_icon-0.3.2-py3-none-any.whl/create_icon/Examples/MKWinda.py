import os
from tkinter import Tk

import create_icon

root = Tk()
title = (os.path.basename(__file__)[0:-3])
root.title(title.title())
root.geometry('400x200')

# Add Icon to window Titlebar
homepath = os.path.expanduser('~')
tempFile = '%s\Caveman Software\%s' % (homepath, 'Icon\icon.ico')

print(os.path.exists(tempFile))
print(tempFile)
if (os.path.exists(tempFile) == True):
    root.wm_iconbitmap(default=tempFile)

else:
    import create_icon
    print('File Created')
    root.wm_iconbitmap(default=tempFile)


root.mainloop()
