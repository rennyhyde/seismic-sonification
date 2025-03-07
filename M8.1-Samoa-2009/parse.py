"""
Data parsing for tremor data from: https://earthquake.usgs.gov/earthquakes/eventpage/usp000h1ys/executive


"""
def parse_txt(path):
    import pandas as pd
    import numpy as np
    from IPython.display import display
    import datetime

    # Read in file, create pandas dataframe
    infile = open(path)
    lines = infile.readlines()
    data = []
    for i in range(len(lines)):
        if (len(lines[i].split()) < 18):        # Some of the lines at the end of the file are 16 items long -> figure out why
            continue                            # For now, ignore these lines
        data.append(lines[i].split())
    df = pd.DataFrame(data, columns = ['along-strike-id(1-88)', 'along-strike-distance_km', 'year', 'month', 'day', 's_of_day', 'hr', 'min', 'sec', 'ccsum', 'meancc', 'med_cc', 'seqday', 'ID', 'latitude', 'longitude', 'depth', 'n_chan'])
    # display(df)

    # Calculate relative time
    # All of these tremors occur on the same day, so we can neglect the year, month, and day for now
    abs_times = []
    rel_times = []
    playback_times = []
    rel_i = 0
    ref = datetime.datetime(2009, 9, 29, 17, 48, 10)

    for series_name, series in df.items():
        if series_name == 'ID':
            continue
        df[series_name] = pd.to_numeric(df[series_name])


    for index, row in df.iterrows():
        abs = datetime.datetime(row['year'], row['month'], row['day'], row['hr'], row['min'], int(row['sec']), int((row['sec']*100)%100)*10000)
        abs_times.append(abs)
        if (index == 0):
            rel_i = abs - ref
        rel_times.append(abs - ref)
        playback_times.append(abs - ref - rel_i)
    df['absolute-time'] = abs_times
    df['relative-time'] = rel_times
    df['playback-time'] = playback_times
    return df

def total_time(df):
    import pandas as pd
    import datetime
    return df.max(axis=0)['relative-time'] - df.min(axis=0)['relative-time']
