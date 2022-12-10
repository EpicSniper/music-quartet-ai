from MIDI import MIDIFile
import os


midi = MIDIFile("output.mid")
midi.parse()
os.remove("file.txt")
f = open("file.txt", "w")


def writeAll():
    for idx, track in enumerate(midi):
        track.parse()
        print(f'Track {idx}:')
        print(str(track))
        f.write(f'Track {idx}:')
        f.write(str(track))

def writeTest():
    for index, track in enumerate(midi):
        parse = track.parse()
        print (parse)

writeAll()