from midiutil.MidiFile import MIDIFile

# create your MIDI object
mf = MIDIFile(1)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, 10, 90)

# add some notes
channel = 0
volume = 85

pitch = 60           # C4 (middle C)
time = 0             # start on beat 0
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 64           # E4
time = 0             # start on beat 2
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 67           # G4
time = 0             # start on beat 4
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

channel = 1

pitch = 72           # C4 (middle C)
time = 4             # start on beat 0
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 76           # E4
time = 4             # start on beat 2
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 79           # G4
time = 4             # start on beat 4
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60           # C4 (middle C)
time = 16             # start on beat 0
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 64           # E4
time = 16             # start on beat 2
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 67           # G4
time = 16             # start on beat 4
duration = 4         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)