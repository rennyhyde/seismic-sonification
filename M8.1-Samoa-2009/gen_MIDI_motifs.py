import pandas as pd
import numpy as np
from IPython.display import display
import datetime
from midiutil.MidiFile import MIDIFile
import itertools

from parse import * 
df = parse_txt("./20090929_M8.1_Samoa_EQ_PKD_LFE_pos.txt")

# Scale times to target length
original_time = total_time(df)
target_time = 3 # minutes
time_scaling = (target_time*60)/original_time.total_seconds()
df['playback-time'] = df['playback-time']*time_scaling
# display(df)

# Melody generation
scale = [0, 2, 4, 5, 7, 9, 11]
note_durs = [4, 8, 16, 32]
BPM = 120
whole = (60/120)*4
combs = []
for i in range(len(scale)+1):
    els = [list(x) for x in itertools.combinations_with_replacement(scale, i)]
    # els = [list(x) for x in itertools.combinations(scale, i)] #Use this for combinations without repetition
    combs.extend(els)

# print(len(combs))
class motif:
    import random
    notes = []
    timing = []
    ID = 0
    def __init__(self, index):
        self.notes = combs[index * 12]
        for i in range(len(self.notes)):
            self.timing.append(note_durs[int(self.random.random()*len(note_durs))])
            if self.random.random() > 0.8:
                if self.random.random() > 0.5:
                    self.notes[i] = self.notes[i]+12
                else:
                    self.notes[i] = self.notes[i]-12
        self.ID = index
    def play(self, mf, time, rel_time):
        #MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        for i in range(len(self.notes)):
            mf.addNote(self.ID-1, 1, self.notes[i]+60, (time - time%(whole/16))*(whole/4), (whole / self.timing[i])*(whole/4), 127)
            time = time + whole / self.timing[i]
            # print("MIDI play")


# Generate MIDI
mf = MIDIFile(numTracks=88, removeDuplicates=False, deinterleave=False)

motifs = []
for i in range(88):
    motifs.append(motif(i))
for index, row in df.iterrows():
    motifs[row['along-strike-id(1-88)']].play(mf, row['playback-time'].total_seconds(), 0)    

# print(mf)
with open("output_motifs.mid", 'wb') as outf:
    mf.writeFile(outf)