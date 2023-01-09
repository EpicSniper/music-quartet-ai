import music21

# tento skript nastavi program pro m21.show()
m21 = music21

us = m21.environment.UserSettings()

print(us['musicxmlPath'])
us['musicxmlPath'] = 'C:\Program Files\MuseScore 4\\bin\MuseScore4.exe'
print(us['musicxmlPath'])