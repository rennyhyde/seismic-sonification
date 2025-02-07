"""
Data parsing for tremor data from: https://earthquake.usgs.gov/earthquakes/eventpage/usp000h1ys/executive


"""
import pandas as pd
infile = open("./20090929_M8.1_Samoa_EQ_PKD_LFE_pos.txt")
lines = infile.readlines()
for line in lines:
    print(len(line))