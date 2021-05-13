from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import sys
from os import path
import numpy as np

application_path = path.dirname(__file__)

def get_winners():
    '''
    Pulls information from the nba scores url.
    :return: List containing winning teams of the day.
    '''
    url = 'https://www.basketball-reference.com/boxscores/'
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    pattern = r'>.{1,21}<'
    winnerlst = soup.findAll('tr', {'class': 'winner'})
    for i in range(len(winnerlst)):
        winnerlst[i] = re.findall(pattern, str(winnerlst[i]))[0:2]
        winnerlst[i][0] = winnerlst[i][0][1:-5]
        winnerlst[i][1] = winnerlst[i][1][1:-1]
        winnerlst[i]=' '.join(winnerlst[i])
    return winnerlst


def get_losers():
    '''
    Pulls information from the nba scores url.
    :return: List containing losing teams of the day.
    '''
    url = 'https://www.basketball-reference.com/boxscores/'
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    pattern = r'>.{1,21}<'
    loserlst = soup.findAll('tr', {'class': 'loser'})
    for i in range(len(loserlst)):
        loserlst[i] = re.findall(pattern, str(loserlst[i]))[0:2]
        loserlst[i][0] = loserlst[i][0][1:-5]
        loserlst[i][1] = loserlst[i][1][1:-1]
        loserlst[i]=' '.join(loserlst[i])
    return loserlst


def get_score():
    '''
    Combines winners and losers lists into dataframe.
    :return: Dataframe containing winners and losers, and their respective scores.
    '''
    loser_lst = get_losers()
    winner_lst = get_winners()
    d = {'Winners': winner_lst, 'Losers': loser_lst}
    df = pd.DataFrame(data=d)
    df.to_csv(path.join(application_path) + 'scores' + '.csv')

#Insert functions to merge losers/winners into dataframe and export as csv.

def find_bos_url():
    '''
    Gets the url containing detailed stats and boxscores for the game the Boston Celtics played in.
    :return: String containing boxscore URL.
    '''
    url = 'https://www.basketball-reference.com/boxscores/'
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    loser_lst=get_losers()
    winner_lst=get_winners()
    newloser=[]
    newwinner=[]
    for i in range(len(loser_lst)):
        loser_lst[i]=loser_lst[i].split(' ')
        winner_lst[i]=winner_lst[i].split(' ')
        newloser.append(loser_lst[i][0])
        newwinner.append(winner_lst[i][0])
    if 'Boston' in newloser:
        bos_index=newloser.index('Boston')
    elif 'Boston' in newwinner:
        bos_index=newwinner.index('Boston')
    else:
        exit()
    bos_game_info = soup.findAll('tr')[bos_index]
    pattern=r'href.+>F<span'
    dirty_url = re.findall(pattern, str(bos_game_info))
    dirty_url[0]=dirty_url[0][17:-8]
    half_url='' + dirty_url[0]
    full_url = url + half_url
    return full_url


def get_bos_stats():
    '''
    Specifically looks for details on Boston Celtics players, get their detailed in-game stats, and form a dataframe.
    :return: Dataframe containing detailed stats of Boston Celtics players for the game that they played.
    '''
    newurl = find_bos_url()
    newhtml = urlopen(newurl)
    newsoup = BeautifulSoup(newhtml,features='html.parser')
    newsoup1 = newsoup.findAll('tr')
    pattern = r'tr>, <tr><th class="left" csk="Tatum,.+, <tr class="thead">'
    listt = re.findall(pattern, str(newsoup1))
    if listt == None:
        exit()
    newlist=str(listt[0]).split(' ')
    namelist_incomp=[]
    mp_incomp=[]
    fg_incomp=[]
    fga_incomp=[]
    three_pt_fg=[]
    three_pa=[]
    ftmade_incomp=[]
    fta_incomp=[]
    totalreb_incomp=[]
    assist_incomp=[]
    pts_incomp=[]
    for i in newlist:
        if 'csk=' in i:
            namelist_incomp.append(i)
        if 'data-stat="mp"' in i:
            mp_incomp.append(i)
        if 'data-stat="fg"' in i:
            fg_incomp.append(i)
        if 'data-stat="fga"' in i:
            fga_incomp.append(i)
        if 'data-stat="fg3"' in i:
            three_pt_fg.append(i)
        if 'data-stat="fg3a"' in i:
            three_pa.append(i)
        if 'data-stat="ft"' in i:
            ftmade_incomp.append(i)
        if 'data-stat="fta"' in i:
            fta_incomp.append(i)
        if 'data-stat="trb"' in i:
            totalreb_incomp.append(i)
        if 'data-stat="ast"' in i:
            assist_incomp.append(i)
        if 'data-stat="pts"' in i:
            pts_incomp.append(i)
    namelist = []
    for i in range(len(namelist_incomp)):
        if i%2 == 0:
            namelist.append(namelist_incomp[i])
    for i in range(len(namelist)):
        namelist[i]=namelist[i].strip('csk=')[1:-1]
    mp = []
    for i in range(len(mp_incomp)):
        mp_incomp[i] = re.findall(r'\d{2}:\d{2}',mp_incomp[i])
        mp.append(mp_incomp[i][0])
    fg = []
    for i in range(len(mp_incomp)):
        fg_incomp[i] = re.findall(r'\d+', fg_incomp[i])
        fg.append(fg_incomp[i][0])
    fga= []
    for i in range(len(fga_incomp)):
        fga_incomp[i] = re.findall(r'\d+', fga_incomp[i])
        fga.append(fga_incomp[i][0])
    threeptfg=[]
    for i in range(len(three_pt_fg)):
        three_pt_fg[i] = re.findall(r'\d+', three_pt_fg[i])
        threeptfg.append(three_pt_fg[i][1])
    threepa=[]
    for i in range(len(three_pa)):
        three_pa[i] = re.findall(r'\d+', three_pa[i])
        threepa.append(three_pa[i][1])
    free_throws_made=[]
    for i in range(len(ftmade_incomp)):
        ftmade_incomp[i] = re.findall(r'\d+', ftmade_incomp[i])
        free_throws_made.append(ftmade_incomp[i][0])
    free_throw_attempts=[]
    for i in range(len(fta_incomp)):
        fta_incomp[i] = re.findall(r'\d+', fta_incomp[i])
        free_throw_attempts.append(fta_incomp[i][0])
    total_rebounds=[]
    for i in range(len(totalreb_incomp)):
        totalreb_incomp[i] = re.findall(r'\d+', totalreb_incomp[i])
        total_rebounds.append(totalreb_incomp[i][0])
    total_assists=[]
    for i in range(len(assist_incomp)):
        assist_incomp[i] = re.findall(r'\d+', assist_incomp[i])
        total_assists.append(assist_incomp[i][0])
    total_points=[]
    for i in range(len(assist_incomp)):
        pts_incomp[i] = re.findall(r'\d+', pts_incomp[i])
        total_points.append(pts_incomp[i][0])
    data_fordf = {'Starters':namelist , 'MP':mp,'FG':fg,'FGA':fga,'3P':threeptfg,'3PA':threepa,'FT':free_throws_made,
                  'FTA':free_throw_attempts,'TRB':total_rebounds,'AST':total_assists,'PTS':total_points}
    final_df = pd.DataFrame(data=data_fordf)
    final_df.to_csv(path.join(application_path) + 'playerdata' + '.csv')



get_excel_score = get_score()
get_bos_excel = get_bos_stats()
