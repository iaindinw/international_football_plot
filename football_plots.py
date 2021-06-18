# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 11:08:42 2021

@author: iaind
"""
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler


plt.style.use('ggplot')

df = pd.read_csv('results.csv')

team_1 = 'Scotland'
team_2 = 'England'

team_1_col = 'tab:blue'
team_2_col = 'tab:red'
draw_col = 'tab:gray'

default_cycler = (cycler(color=[team_1_col, team_2_col, draw_col, 'black']))
plt.rc('axes', prop_cycle=default_cycler)


fixtures = df.loc[(df['home_team'].isin([team_1,team_2])) &
                  (df['away_team'].isin([team_1,team_2])), :].copy()

team_1_home = fixtures['home_team'] == team_1
team_1_away = ~team_1_home


fixtures.loc[ team_1_home, 'team_1_score'] = fixtures.loc[team_1_home, 'home_score']
fixtures.loc[ team_1_away, 'team_1_score'] = fixtures.loc[team_1_away, 'away_score']


fixtures.loc[team_1_home, 'team_2_score'] = -fixtures.loc[team_1_home, 'away_score']
fixtures.loc[team_1_away, 'team_2_score'] = -fixtures.loc[team_1_away, 'home_score']

fixtures['date'] = pd.to_datetime(fixtures['date'], format='%Y-%m-%d')

fixtures = fixtures.set_index('date')

fixtures = fixtures.resample('D').mean()

fixtures = fixtures.reset_index()

team_1_win = fixtures['team_1_score'] > fixtures['team_2_score'].abs()
team_2_win = fixtures['team_1_score'] < fixtures['team_2_score'].abs()
draw = fixtures['team_1_score'] == fixtures['team_2_score'].abs()


fig1, ax1 = plt.subplots(figsize=(12,6))

if sum(team_1_win) > 0:

    ax1.stem(fixtures.loc[team_1_win, 'date'], fixtures.loc[team_1_win, 'team_1_score'],
             linefmt=team_1_col, markerfmt='C0'+'o')
    ax1.stem(fixtures.loc[team_1_win, 'date'], fixtures.loc[team_1_win, 'team_2_score'],
             linefmt=team_1_col, basefmt=" ", markerfmt='C0'+'o',
             label=f'{team_1} - {sum(team_1_win)} win(s)')

if sum(team_2_win) > 0:
    ax1.stem(fixtures.loc[team_2_win, 'date'], fixtures.loc[team_2_win, 'team_1_score'],
             linefmt=team_2_col, markerfmt='C1'+'o')
    ax1.stem(fixtures.loc[team_2_win, 'date'], fixtures.loc[team_2_win, 'team_2_score'],
             linefmt=team_2_col, basefmt=" ", markerfmt='C1'+'o',
             label=f'{team_2} - {sum(team_2_win)} win(s)')

if sum(draw) > 0:
    ax1.stem(fixtures.loc[draw, 'date'], fixtures.loc[draw, 'team_1_score'],
             linefmt=draw_col, markerfmt='C2'+'o')
    ax1.stem(fixtures.loc[draw, 'date'], fixtures.loc[draw, 'team_2_score'],
             linefmt=draw_col, basefmt=" ", markerfmt='C2'+'o',
             label=f'Draw - {sum(draw)}')

max_score = fixtures[['home_score','home_score']].max().max()

ax1.set_ylim(-max_score-0.5, max_score+0.5)

ax1.set_yticks(range(int(-max_score), int(max_score)+1))

ax1.set_yticklabels([int(abs(x)) for x in ax1.get_yticks()])

ax1.legend()

plt.figtext(0.08, 0.6 ,f'{team_1} Score', rotation = 'vertical', ha='center')

plt.figtext(0.08, 0.3 ,f'{team_2} Score', rotation = 'vertical', ha='center')







