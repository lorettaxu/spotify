import numpy as np
import json
import pandas as pd
import time
import os
import random


time_start=time.time()


path='spotify_mpd/data'
filenames = os.listdir(path)


for i in filenames:
	if i[-4:]!='json':
		filenames.remove(i)
print(filenames)



playlist=[]
trackslist=[]
durations=[]


# adjust according to dataset size
test_pid=random.sample(range(0,1000),200)
test_pid=set(test_pid)

test_playlist=[]
test_tracklist=[]
test_duration=[]


for filename in filenames:
	fullpath = os.sep.join((path, filename))
	with open(fullpath, 'r') as f:
		load_data = json.load(f)
	data=load_data.get("playlists")

	for lists in data:
		pid=lists.get('pid')
		if pid in test_pid:
			num_tracks=lists.get('num_tracks')
			# pick half of the tracks in test playlists as holdout tracks
			test_tracks=random.sample(range(0,num_tracks),num_tracks//2)
			for tracks in lists.get("tracks"):
				#build test set
				if tracks.get('pos') in test_tracks:
					test_playlist.append(pid)
					test_tracklist.append(tracks.get('track_uri'))
					duration=tracks.get('duration_ms')/60000
					test_duration.append(duration)

				else:
					playlist.append(pid)
					trackslist.append(tracks.get('track_uri'))
					duration=tracks.get('duration_ms')/60000
					durations.append(duration)
		else:
			for tracks in lists.get("tracks"):

				playlist.append(pid)
				trackslist.append(tracks.get('track_uri'))
				#transform ms to minutes
				duration=tracks.get('duration_ms')/60000
				durations.append(duration)



a=trackslist+test_tracklist
dataframe3=pd.DataFrame({'track_uri':a})


#set track index
unique_tracks = dataframe3['track_uri'].unique()
print(len(unique_tracks))

tracks = pd.DataFrame({
        'track' :unique_tracks,
        'track_index': range(len(unique_tracks))
    })

dataframe1=pd.DataFrame({"playlist": playlist,"track":trackslist,"duration":durations})
dataframe2=pd.DataFrame({"playlist": test_playlist,"track":test_tracklist,"duration":test_duration})


dataframe1 = pd.merge(dataframe1, tracks, how = 'inner', left_on='track', right_on = 'track')
dataframe1.to_csv("durations.csv",index=False,sep=",")


dataframe2=pd.merge(dataframe2, tracks, how = 'inner', left_on='track', right_on = 'track')
dataframe2.to_csv("test_durations.csv",index=False,sep=",")





time_end=time.time()
print('total:',time_end-time_start)













# with open('spotify_mpd/data/mpd.slice.0-999.json', 'r') as f:
#     load_data = json.load(f)


# data=load_data.get("playlists")

# playlist=[]
# trackslist=[]
# durations=[]
# for lists in data:
# 	pid=lists.get('pid')
# 	for tracks in lists.get("tracks"):
# 		playlist.append(pid)
# 		trackslist.append(tracks.get('track_uri'))
# 		duration=tracks.get('duration_ms')/60000
# 		#durations.append(int(tracks.get('duration_ms')))
# 		durations.append(duration)


# dataframe=pd.DataFrame({"playlist": playlist,"track":trackslist,"duration":durations})
# print(dataframe.shape)

# time_start=time.time()
# dataframe.to_csv("slice1.csv",index=False,sep=",")
# time_end=time.time()
# print('total:',time_end-time_start)



# time_start=time.time()
# dataframe.to_hdf('slice1.hdf', key='slice1')
# time_end=time.time()
# print('total:',time_end-time_start)

