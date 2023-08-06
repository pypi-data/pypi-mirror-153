# In Japan, there is a saying, "When the autumn rains fall, the cat's face becomes three feet long.
# This means that the cat's face is longer and more joyful on rainy days than on sunny days in autumn, because the temperature is higher on rainy days.
# We assume that the more it rains, the more pleased the cat will be.
# Of course, this is limited to autumn.
# If it is autumn now, this will help.
# There is a lot going on in the world right now.
# But it does not matter to cats.
# If cats are happy, the world will be peaceful.

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time
import warnings
import subprocess as sp
import requests
import io

def imscatter(x, y, image, ax=None, zoom=1): 
    if ax is None: 
        ax = plt.gca() 
    try: 
        image = plt.imread(image) 
    except:
        pass 
    im = OffsetImage(image, zoom=zoom) 
    artists = [] 
    for x0, y0 in zip(x, y): 
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False) 
        artists.append(ax.add_artist(ab)) 
    return artists 


def main():
    week_rain = []
    for i in range(7):
        if i == 0:
            url = "https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/predaily00_rct.csv"
            # sp.call("wget https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/predaily00_rct.csv", shell=True)
        else:
            url = "https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/predaily0"+str(i)+".csv"
            # sp.call("wget https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/predaily0"+str(i)+".csv", shell=True)
        
        # sp.call("wget https://www.data.jma.go.jp/obd/stats/data/mdrr/pre_rct/alltable/predaily00_rct.csv -O 'rain.csv'", shell=True)
        

        r = requests.get(url).content
        df = pd.read_csv(io.BytesIO(r), encoding="shift_jis")
        # df = pd.read_csv('./rain.csv', encoding='shift-jis')
        # if i == 0:
        #     df = pd.read_csv('predaily00_rct.csv', encoding='shift-jis')
        # else:
        #     df = pd.read_csv('predaily0'+str(i)+'.csv', encoding='shift-jis')
            
        rain_list = df.iloc[:,9].values.tolist()
        rain = []
        for a in rain_list:
            if str(a) == "nan":
                a = 0
            rain.append(a)
        week_rain.append(sum(rain))

    print("In Japan, there is a saying, \"When the autumn rains fall, the cat's face becomes three feet long.\"")
    time.sleep(1)
    print("This means that the cat's face is longer and more joyful on rainy days than on sunny days in autumn, because the temperature is higher on rainy days.")
    time.sleep(1)
    print("We assume that the more it rains, the more pleased the cat will be.")
    time.sleep(1)
    print("Of course, this is limited to autumn.")
    time.sleep(1)
    print("If it is autumn now, this will help.")
    time.sleep(1)
    print("There is a lot going on in the world right now.")
    time.sleep(1)
    print("But it does not matter to cats.")
    time.sleep(1)
    print("If cats are happy, the world will be peaceful.")
    time.sleep(1)
    
    label = ["5 days ago", "4 days ago", "3 days ago", "2 days ago", "Yesterday", "Today", "Tomorrow"]
    warnings.simplefilter('ignore')
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.set_yticklabels(["", "", "sad", "", "normal", "", "happy"])

    imscatter(label, week_rain, "cat.png", ax=ax,  zoom=.03)
    plt.xticks(rotation=30)
    ax.plot(label, week_rain, marker="o")
    fig.savefig("result.png")
    plt.show()

if __name__ == "__main__":
    main()
