import PySimpleGUI as sg                        # Part 1 - The import
import os

TK_SILENCE_DEPRECATION=1 

# Define the window's contents
layout = [  [sg.Input(), sg.FileBrowse('FileBrowse')], 
            [sg.Input(), sg.FolderBrowse('FolderBrowse')],
            [sg.Submit(), sg.Cancel()], 
            [sg.Multiline(key='files',size=(60,30), autoscroll=True)],
            ]

window = sg.Window('Files',layout)

while True:
    event, values = window.read()
    print('event:', event)
    print('values:', values)
    print('FolderBrowse:', values['FolderBrowse'])
    print('FileBrowse:', values['FileBrowse'])
     
    if event is None or event == 'Cancel':
        break
    
    if event == 'Submit':
        # if folder was not selected then use current folder `.`
        foldername = values['FolderBrowse'] or '.' 

        filenames = os.listdir(foldername)
        # it uses `key='files'` to access `Multiline` widget
        window['files'].update("\n".join(filenames))
        print('folder:', foldername)
        print('files:', filenames)
        print("\n".join(filenames))
    
# Finish up by removing from the screen
window.close()                                  # Part 5 - Close the Window
