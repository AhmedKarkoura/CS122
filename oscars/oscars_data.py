import numpy as np
import pandas as pd 

CATEGORIES = ['ACTOR', 'ACTRESS', 'ART DIRECTION', 'CINEMATOGRAPHY',
       'DIRECTING ', 'ENGINEERING EFFECTS', 'OUTSTANDING PICTURE',
       'UNIQUE AND ARTISTIC PICTURE', 'WRITING ', 'DIRECTING', 'WRITING',
       'OUTSTANDING PRODUCTION', 'SOUND RECORDING', 'SHORT SUBJECT ',
       'ASSISTANT DIRECTOR', 'FILM EDITING', 'MUSIC ', 'DANCE DIRECTION',
       'ACTOR IN A SUPPORTING ROLE', 'ACTRESS IN A SUPPORTING ROLE',
       'IRVING G. THALBERG MEMORIAL AWARD', 'SPECIAL AWARD',
       'CINEMATOGRAPHY ', 'SPECIAL EFFECTS',
       'SCIENTIFIC OR TECHNICAL AWARD ', 'ART DIRECTION ', 'DOCUMENTARY ',
       'OUTSTANDING MOTION PICTURE', 'DOCUMENTARY', 'BEST MOTION PICTURE',
       'COSTUME DESIGN ', 'HONORARY FOREIGN LANGUAGE FILM AWARD',
       'FOREIGN LANGUAGE FILM', 'JEAN HERSHOLT HUMANITARIAN AWARD',
       'COSTUME DESIGN', 'SOUND', 'BEST PICTURE', 'SOUND EFFECTS',
       'SPECIAL VISUAL EFFECTS', 'SPECIAL ACHIEVEMENT AWARD ',
       'SHORT FILM ', 'ACTOR IN A LEADING ROLE',
       'ACTRESS IN A LEADING ROLE', 'VISUAL EFFECTS', 'MAKEUP',
       'GORDON E. SAWYER AWARD', 'SOUND EFFECTS EDITING',
       'AWARD OF COMMENDATION', 'SOUND EDITING', 'ANIMATED FEATURE FILM',
       'SOUND MIXING', 'MAKEUP AND HAIRSTYLING', 'PRODUCTION DESIGN']
       
BEST_PICTURE = ["BEST MOTION PICTURE", "OUTSTANDING MOTION PICTURE", "OUTSTANDING PRODUCTION", "BEST PICTURE"]
BEST_ACTOR = ["ACTOR", "ACTOR IN A LEADING ROLE", "ACTOR IN A SUPPORTING ROLE"]
BEST_ACTRESS = ["ACTRESS", "ACTRESS IN A LEADING ROLE", "ACTRESS IN A SUPPORTING ROLE"]

oscars_db = pd.read_csv('oscars.csv')
oscars_db = oscars_db.loc[oscars_db.entity.str.startswith("To") == False]

best_pic_nominees = oscars_db.loc[oscars_db.category.isin(BEST_PICTURE) == True]
best_pic_winners = best_pic_nominees.loc[best_pic_nominees.winner == True]

best_actor_nominees = oscars_db.loc[oscars_db.category.isin(BEST_ACTOR) == True]
best_actor_winners = best_actor_nominees.loc[best_actor_nominees.winner == True]

best_actress_nominees = oscars_db.loc[oscars_db.category.isin(BEST_ACTRESS) == True]
best_actress_winners = best_actress_nominees.loc[best_actress_nominees.winner == True]

oscars_db['cat'] = oscars_db['category'].str.split('(').str.get(0)