import numpy as np
import pandas as pd 

DISREGARD_CATEGORIES = [
   'SHORT SUBJECT (One-reel)', 'SHORT SUBJECT (Two-reel)', 
   'ASSISTANT DIRECTOR', 'DANCE DIRECTION', 'ENGINEERING EFFECTS',
   'WRITING (Original Story)', 'MUSIC (Scoring of a Musical Picture)',
   'MUSIC (Music Score of a Dramatic or Comedy Picture)',
   'SHORT SUBJECT (Color)', 'SHORT SUBJECT (Comedy)', 
   'SHORT SUBJECT (Novelty)', 'WRITING (Title Writing)',
   'ACTOR IN A SUPPORTING ROLE', 'ACTOR IN A LEADING ROLE', 
   'ACTRESS IN A LEADING ROLE', 'ACTRESS IN A SUPPORTING ROLE', 
   'ACTOR', 'ACTRESS']

def get_awards():
   oscars = pd.read_csv('oscars.csv')
   oscars = oscars.loc[oscars.entity.str.startswith("To") == False]
   oscars = oscars.loc[oscars.category.str.contains("SPECIAL") == False]
   oscars = oscars.loc[oscars.category.str.contains("AWARD") == False]
   oscars = oscars.loc[oscars.category.isin(DISREGARD_CATEGORIES) == False]
   oscars = oscars.loc[oscars.year >= 1929]
   oscars.to_csv(r'oscars_awards.csv', index = False)

