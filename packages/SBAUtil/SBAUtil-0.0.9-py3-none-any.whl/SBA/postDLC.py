import pandas as pd
from tables import HDF5ExtError
import os

def convertLabeledMP4toAVI(folder,destFolder=None):
    """
    Convert all mp4 files in the `folder` to AVI using ffmpeg
    If `destFolder` is None, the converted file will be saved in the current directory
    """

    if not os.path.exists(folder):
        print("{} does not exist".format(folder))
        return

    if not destFolder:
        destFolder = os.getcwd()
    
    files = os.listdir(folder)
    for file in files:
        
        if file.split(".")[-1] not in {"mp4", "MP4"}:
            continue
        videoName = file.split('.')[0]
        inputPath = os.path.join(folder,file)
        outputPath = os.path.join(destFolder, videoName+".avi")
        os.system("ffmpeg -i {} -vcodec mpeg4 {}".format(inputPath,outputPath))

    print("Done.")

def flipIdentity(frames, h5file, mouse1Name = "Mouse1", mouse2Name = "Mouse2"):
    """
    Flip identities for mouse1 and mouse2 at the frames given by the list of integers `frames`
    Input:
        `frames`: iterable(list) of int, the frames or frame where the two mice switch identity
        `h5file`: path to the DLC output file
        `mouse1Name`: the name of the first mouse
        `mouse2Name`: the name of the second mouse
    """
    if len(frames) == 0:
        print("list is empty.")
        return
    try:
        data = pd.read_hdf(h5file)
    except FileNotFoundError:
        print("File {} does not exists!".format(h5file))
        return
    except HDF5ExtError:
        return
    
    numFrames = len(data.index)

    frames = sorted(frames)
    
    if len(frames) % 2:
        frames.append(numFrames)
    
    id = data.iloc[0].index.get_level_values(0)[0]
    def flip(start,end):
        for i in range(start,end):
            temp = data.iloc[i][id][mouse1Name].copy()
            temp2 = data.iloc[i][id][mouse2Name].copy()
            data.iloc[i][id][mouse1Name] = temp2
            data.iloc[i][id][mouse2Name] = temp

    for i in range(0,len(frames),2):
        flip(frames[i],frames[i+1])
    
    
    data.to_hdf(h5file,key="df_with_missing", mode= "w")
    print("Done.")

if __name__ == "__main__":
    OriData = pd.read_hdf("./sample.h5")
    print(OriData.iloc[1955:1980])
    flipIdentity([1957,8261,9293,13278],"./sample.h5","mouse1","mouse2")

    newData = pd.read_hdf("./sample.h5")
    print(newData.iloc[1955:1980])
