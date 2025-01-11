#GameState - Werewolf

game_state = {
    'players': {
        'A': 'Dorfbewohner',
        'B': 'Dorfbewohner',
        'C': 'Dorfbewohner',
        'D': 'Dorfbewohner',
        'E': 'Werwolf',
        'Agent': 'Werwolf' #Agent F
    },
    'history': [
       "night": 1 #showing, dass wir uns in der Nacht-Phase befinden, day- cvar vllt redundant
       "day": 0
       "lover": 0, # 2 players are set lover=1, the other lover gets added in the ally array
       "asleep":1
       "in_love" : 0, #Because werewolves are not the first to wake up in night 1
       "last_statement": { (Role, Statement): "Moderator", "Die Nacht beginnt. Amor erwachen. Verliebten wählen . "},
       "verbliebene_Players" : {A,B,C,D,E},
       "ally" : {'E'},
       "target" : { (ID, Sonderrolle): (A, NULL), (B, NULL), (C, NULL), (D, NULL)},
       #mögliche Werte --> Sonderrolle: Seher, Hexe, Jäger, Amor
       "findsme_suspicious" : {}
    ]
}
#Prioritätsvariable to be added --- erste_DiskTeilnehmen = A (B,C,D,E)
#Wenn variablen "target" und "findsme_suspicious" lerr --> keine Strategie --> Llama entscheidet random


#GameState - Dorfbewohner
game_state = {
    'players': { #(ID, Rolle)
        'A': NULL,
        'B': NULL,
        'C': NULL,
        'E': NULL,
        'F': NULL,
        'Agent': 'Dorfbewohner' #Agent D
    },
    'history': [
       "night": 1, #showing, dass wir uns in der Nacht-Phase befinden
       "day": 0,
       "lover": 0,
"asleep": 1,
"last_statement": { { (Role, Statement): "Moderator", "Die Nacht beginnt. Amor erwachen. Verliebten wählen . "}},
       "eliminated" : {},
       "ally" : [],
       "target_möglicheWW" : [], #(A), (B), (C), (E), (F)
       "findsme_suspicious" : {}
    ]
}

#GameState - Amor
game_state = {
    'players': { #(ID, Rolle)
        'B': NULL,
        'C': NULL,
        'D': NULL,
        'E': NULL,
        'F': NULL,
        'Agent': 'Amor' #Agent A
    },
    'history': [
       "night": 1, #showing, dass wir uns in der Nacht-Phase befinden
       "day": 0,
       "lover": 0, #final variable
"asleep": 0,
"last_statement": { (Role, Statement): "Moderator", "Die Nacht beginnt. Amor erwachen. Verliebten wählen . "},
       "eliminated" : {},
       "ally" : [],
       "lovers" : [], #max array size: 2 (IDs - B,C,D,E,F)
       "target_möglicheWW" : [], #(B), (C), (D), (E), (F)
       "findsme_suspicious" : {}
    ]

# lovers array wird automatisch ausgefüllt, players lover(var) = 1 --> amor: rolle: dorfbewohner --> moderator: summary for amor --> asleep: 1-->
# the players with the ausgewähle IDs --> asleep: 0, andere Player with lover=1 wird in das ally-array eingefügt -->
# moderator summary for verliebte: game rules and strategy instr. --> asleep: 1
}

#GameState - Seher
game_state = {
    'players': { #(ID, Rolle)
        'A': NULL,
        'C': NULL,
        'D': NULL,
        'E': NULL,
        'F': NULL,
        'Agent': 'Seher' #Agent B
    },
    'history': [
       "night": 1, #showing, dass wir uns in der Nacht-Phase befinden
       "day": 0,
       "lover": 0,
"asleep": 0,
"last_statement":  { (Role, Statement): "Moderator", "Seherin erwahe. Wähle der Spieler aus, von dem du sie Rolle sehen willst."},
       "eliminated" : {},
       "ally" : [],
       "target_möglicheWW" : [], #(A), (B), (C), (E), (F)
       "findsme_suspicious" : {}
    ]
    #!!! Er muss immer als erstes aufstehen (außer Initialrunde)
    #ID wählen --> die Rolle des Players mit dem ausgewählte ID wird gefüllt (vom Moderator übernommen)--> Moderator summary für seher
}
#Werewolf, Dorfbewoner, Amor, Seher, Hexe

