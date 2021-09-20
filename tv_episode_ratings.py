# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:07:18 2021

@author: madar
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

os.chdir('C:/Users/madar/Documents/GitHub/markrustad/tv_episode_ratings')

#%% import data

# choose which show to analyze
# ---------------------
# show = 'familyguy'
# show = 'curb'
# show = 'breakingbad'
# show = 'bettercallsaul'
# show = 'simpsons'
# show = 'seinfeld'
# show = 'southpark'
# show = 'blacklist'
# show = 'office'
# show = 'sunny'
# show = 'veep'
# show = 'got'
# show = 'wire'
# show = 'rickandmorty'
# show = 'truedetective'
# show = 'nathanforyou'
# ---------------------

shows =['familyguy',
        'curb',
        'breakingbad',
        'bettercallsaul',
        'simpsons',
        'seinfeld',
        'southpark',
        'blacklist',
        'office',
        'sunny',
        'veep',
        'got',
        'wire',
        'rickandmorty',
        'truedetective',
        'nathanforyou']

for show in shows:

    # episode ratings
    rate = pd.read_table('data/'+show+'.txt', header=None)

    # season details
    eps = pd.read_csv('data/'+show+'_seasons.txt', sep='\t')

    #%% multi index for ratings information: (episode no., [detals])

    episodes = range(1,1+eps.Episodes.sum())

    iterables = [episodes, ['title', 'title2', 'detail', 'rating', 'last']]

    index = pd.MultiIndex.from_product(iterables)

    rate.index = index

    #%% create dataframes

    # convert MultiIndex to columns using unstack()
    data = rate.unstack().droplevel(0,axis=1).rename_axis(index='number').reset_index()

    # create column of season no. and episode no. per season
    s = []
    e = []
    for i in range(len(eps)):
        x = eps.Episodes.iloc[i]    # episodes per season
        segment = [eps.Season.iloc[i]]*x

        e+=range(1,x+1)    # episode count per season
        s+=segment

    data['season'] = s
    data['ep'] = e
    data = data[['number', 'season', 'ep', 'title', 'rating']]
    data = data.astype({'rating': 'float64',
                        'season': 'int64',
                        'number': 'int64',
                        'ep': 'int64',
                        'title': 'string'})

    # group by season
    gp = data.groupby('season')

    # pivot table of ratings
    hm = data.pivot(index='season',
                    columns='ep',
                    values='rating')

    #%% visualize

    data.plot(x='season', y='rating', kind='scatter', xticks=range(1,eps.Season.max()+1))
    gp.rating.mean().plot(color='m', marker='*', lw=1, markersize=20, fillstyle='none')

    fig0 = plt.gcf()
    ax0 = plt.gca()

    # Rotate the tick labels and set their alignment.
    plt.setp(ax0.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    asp = data.season.max()/data.ep.max()
    dim = 10

    fig0.set_figheight(dim)
    fig0.set_figwidth(dim)

    ax0.set_title('IMDB rating of ' + show)
    ax0.set_xlabel('Season')
    ax0.set_ylabel('Rating')
    fig0.tight_layout()

    plt.savefig('results/' + show + '_scatter.png')
    plt.close()


    #%% visualize: heatmap

    # https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html

    seasons = range(1,eps.Season.max()+1)
    episodes = range(1,eps.Episodes.max()+1)

    fig, ax = plt.subplots()
    im = ax.imshow(hm.to_numpy(),
                   cmap='Blues',
                   vmin=data.rating.min()*.85)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(episodes)))
    ax.set_yticks(np.arange(len(seasons)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(episodes)
    ax.set_yticklabels(seasons)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(seasons)):
        for j in range(len(episodes)):
            text = ax.text(j, i, hm.to_numpy()[i, j],
                           ha="center", va="center", color='w')

    ax.set_title('IMDB rating of ' + show)
    ax.set_xlabel('Episode')
    ax.set_ylabel('Season')

    fig.set_figheight(dim)
    fig.set_figwidth(dim/asp)

    fig.tight_layout()

    plt.savefig('results/' + show + '_heatmap.png')
    plt.close()
