import GUI

mainWindow = None


def buildMainWindowSingleton():
    global mainWindow
    if mainWindow is None:
        mainWindow = GUI.GUIMainWindow.GUIMainWindow()
