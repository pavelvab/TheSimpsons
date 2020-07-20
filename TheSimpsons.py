import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import pylab as pl
from PIL import ImageColor
import re
import os.path
from os import path

from matplotlib import rcParams
plt.rcParams["font.family"] = "serif"

# Variables
MinimumWords = 1000
KEYWORDS1 = ['BEER', 'BEERS', 'WINE', 'DUFF', 'DRUNK', 'ALCOHOLIC', 'ALCOHOLICS', 'ALCOHOL', 'DRINKING', 'BAR', 'CIGAR', 'CIGARETTE', 'DRUGS', 'REEFER', 'MARIJUANA', 'BONG', 'BONGS', 'COCAINE']
KEYWORDS2 = ['ROMANTIC', 'ROMANCE', 'SEX', 'SEXUAL', 'SEXY', 'HOTTIE', 'LUST', 'LOVER', 'LIBIDO', 'LOVERS', 'LUSTS', 'BOOB', 'BOOBS', 'BREAST', 'BREASTS', 'BUTT', 'BUTTS', 'WONANIZE', 'WONAMIZER', 'KINKY', 'KINK', 'UNDERWEAR', 'BRA', 'BRAS', 'PANTIES']
PATH_TO_DATA = './553928_1008865_bundle_archive/simpsons_script_lines.csv'
IMAGE_PATH = './TheSimpsons/Headshots/'

def get_freqs(DICT, KEYWORDS):
    DICT1 = {}
    for character in DICT.keys():
        X = 0
        for kw in KEYWORDS:
            if kw in DICT[character].keys():
                X += DICT[character][kw]
        TotalWords = sum(DICT[character].values())
        X /= TotalWords
        if TotalWords > MinimumWords:
            #print(character, X)
            DICT1[character] = X
    sorted_DICT1 = sorted(DICT1.items(), key=lambda x: x[1])
    return sorted_DICT1, DICT1


# Used to plot images in matplotlib
def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists


# Create the plot
def plot_scatter(DICT1, DICT2, sorted_DICT2):
    fig, ax = plt.subplots(figsize=(12,8))

    for C in reversed(sorted_DICT2):
        character = C[0]
        #print(character)
        if character in DICT2.keys():
            if character == "Crowd" or character == "Announcer": # Skip because they are not Individual characters
                continue
            X = np.log10(DICT1[character])
            Y = np.log10(DICT2[character])

            logopath = IMAGE_PATH + character + ".png"
            if os.path.exists(logopath):
                image_path = get_sample_data(logopath)
                imscatter(X, Y, image_path, zoom=0.5, ax=ax)
            else:
                plt.scatter(X, Y)
                plt.annotate(character, # this is the text
                             (X, Y), # this is the point to label
                             textcoords="offset points", # how to position the text
                             xytext=(0,3), # distance from text to points (x,y)
                             ha='center',
                             color='black',
                             fontsize=7) # horizontal alignment can be left, right or center

    plt.suptitle('The Simpsons References to Drugs/Alcohol and Sex', fontsize=22)
    plt.title('Log likelihood by character. Using 600 episodes', fontsize=16)
    plt.xlabel('References to drugs / alcohol', fontsize=15)
    plt.ylabel('References to sex', fontsize=15)

    plt.grid(color='k', linestyle='--', linewidth=1, alpha=0.15)
    plt.figtext(.7,.04,'Data: kaggle/the-simpsons-dataset\nPlot: @Pavel_Vab',fontsize=9)
    plt.show()


def main():

    # Load data into pandas
    DATA = pd.read_csv(PATH_TO_DATA)

    # Keep only the columns for the character name and spoken words
    Words = DATA[['raw_character_text', 'spoken_words']]
    Lines = Words.values.tolist()

    # Create word counts dictionary for each character
    DICT = {}
    for line in Lines:
        character = str(line[0])
        character = re.sub(r'[^\w]','',character) # Remove white space from character

        sentence = str(line[1])
        sentence = re.sub(r'[^\w\s]','',sentence) # Remove any puntucation from the line
        sentence = sentence.upper() # Make uppercase

        words = sentence.split()

        if character in DICT.keys():
            x = 1
        else:
            DICT[character] = {}
        for w in words:
            if w in DICT[character].keys():
                DICT[character][w] += 1
            else:
                DICT[character][w] = 1

    sorted_DICT1, DICT1 = get_freqs(DICT, KEYWORDS1)
    sorted_DICT2, DICT2 = get_freqs(DICT, KEYWORDS2)
    plot_scatter(DICT1, DICT2, sorted_DICT2)

main()
