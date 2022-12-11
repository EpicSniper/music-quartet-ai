from mido import MidiFile
import os

mid = MidiFile('Noshing_just_an_inchident.mid', clip=True)
print(mid)

#os.remove("file.txt")
f = open("file.txt", "w")

for track in mid.tracks:
    #print(str(track))
    f.write(str(track) + "\n")
    for msg in track:
        msg = str(msg)
        if msg.startswith('note_on'):
            print(str(msg))
            f.write(str(msg) + "\n")