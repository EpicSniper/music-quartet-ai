import music21

m21 = music21

us = m21.environment.UserSettings()

print(us['musicxmlPath'])
us['musicxmlPath'] = 'C:\Program Files\MuseScore 3\\bin\MuseScore3.exe'
print(us['musicxmlPath'])
