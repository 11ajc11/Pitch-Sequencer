import mlbgame
import operator
from mlbgame.info import *
from mlbgame.stats import *
from mlbgame.events import *
from mlbgame.game import *
from mlbgame.data import *


#returns all roster info from team_id(see cats) cat: info
def getroster(team_id):
    cats = [
    'name_display_first_last',
    'jersey_number',
    'position_txt',
    'throws',
    'bats',
    'weight',
    'college',
    'height_feet',
    'height_inches',
    'starter_sw',
    'pro_debut_date',
    'status_code',
    'primary_position',
    'birth_date',
    'player_id',
]
    i = roster(team_id)
    allinfo = i['players']
    #print(allinfo)
    for player in range(len(allinfo)):
        for cat in cats:
            #if allinfo[player][cat] == 'P':
            print(cat,':',allinfo[player][cat])


#returns names from roster team_id 
def getrosternames(team_id):
    i = roster(team_id)
    allinfo = i['players']
    for player in range(len(allinfo)):
        print(allinfo[player]['name_display_first_last'])

#give team_id and pos gives names, pos
def getpos(team_id,pos):
    i = roster(team_id)
    allinfo = i['players']
    for player in range(len(allinfo)):
        if allinfo[player]['position_txt'] == pos:
            print(allinfo[player]['name_display_first_last'],pos)

#returns teams_ids in dict key = commom name
def teamids():
    teams = {}
    i = team_info()
    #allteam = i[]
    for team in range(len(i)):
        teams[i[team]['club_common_name']] = i[team]['team_id']
    return(teams)

def teamnames():
    teams = {}
    i = team_info()
    #allteam = i[]
    for team in range(len(i)):
        teams[i[team]['team_id']] = i[team]['club_common_name']
    return(teams)

#give pos and returns all players of that pos(needs refining)
def getplayerbypos(pos):
    teams = teamids()
    for i in teams:
        getpos(teams[i],pos)

#give string and get dict of team: teamid
def teamid(strname):
    matchname = {}
    teams = teamids()
    for i in teams:
        if strname in i:
            matchname[i] = teams[i]
    return(matchname)

def inj(team):
    i = injury()
    for item in i:
        if item['team_name'] == team:
            print(item['team_name'],item['name_first'],item['name_last'])
            print(item['injury_desc'])
            print(item['injury_update'])
            print()

def getname(pitcherid, gameid):
    t = teamnames()
    allplayers = players(gameid)
    for player in range(len(allplayers['home_team']['players'])):
        if allplayers['home_team']['players'][player]['id']==pitcherid:
            name = t[(allplayers['home_team']['players'][player]['team_id'])]
            return(name, allplayers['home_team']['players'][player]['first'] + " " + allplayers['home_team']['players'][player]['last'])
    for player in range(len(allplayers['away_team']['players'])):
        if allplayers['away_team']['players'][player]['id']==pitcherid:
            name = t[(allplayers['away_team']['players'][player]['team_id'])]
            return(name, allplayers['away_team']['players'][player]['first'] + " " + allplayers['away_team']['players'][player]['last'])
   
        
    

def getgamedata(year, month, hometeam):
    homepitch = {}
    awaypitch = {}
    homesequence = {}
    awaysequence = {}
    prpitch = {}
    month = mlbgame.games(int(year), int(month), home = hometeam, away = hometeam)
    games = mlbgame.combine_games(month)
    chpitch = ""
    capitch = ""
    i = 0
    for game in games:
        print(game.game_id)
        try:
            
            data = game_events(game.game_id)
            for inning in data:
                for tb in data[inning]:
                    #print (tb + " of the " + inning)
                    #print(data[inning])
                    for batter in data[inning][tb]:
                        pname = getname(batter['pitcher'], game.game_id)
                        #bname = getname(batter['batter'], game.game_id)
                        #print("batter number " + batter['num'])
                        #print("pitcher: " + pname)
                        #print("batter: " + bname)
                        #print("result: " + batter['event'])  Put this back
                        #print(batter)
                        pitches = batter['pitches']
                        pitchseq = ""
                        for pitch in pitches:
                            pitchseq = pitchseq + " "+ pitch['pitch_type']
                            #print(pitch['pitch_type'], pitch['start_speed'], pitch['des'])
                        pitchseq = pitchseq + " " + batter['event']
                        pitchseq = pitchseq[1:len(pitchseq)]
                        #print(batter['team'])
                        #if batter['event'] in prpitch:
                            #prpitch[batter['event']] = prpitch[batter['event']]+1
                        #else:
                            #prpitch[batter['event']] = 1
                        if pname[0] == hometeam:
                            if bool(homepitch) == False:
                                homepitch[pname]={}
                                #print(awaypitch)
                            if pname[1] in homepitch:
                                homesequence = homepitch[pname[1]]
                                #print(awaysequence)
                            else:
                                homepitch[pname[1]] = {}
                                homesequence = homepitch[pname[1]]  
                            if pitchseq in homesequence:
                                homesequence[pitchseq]=homesequence[pitchseq]+1
                                awaypitch[pname[1]]=awaysequence
                            else:
                                homesequence[pitchseq]=1
                                homepitch[pname[1]]=homesequence

                        else:
                            if bool(awaypitch) == False:
                                awaypitch[pname[1]]={}
                                #print(awaypitch)
                            if pname[1] in awaypitch:
                                awaysequence = awaypitch[pname[1]]
                                #print(awaysequence)
                            else:
                                awaypitch[pname[1]] = {}
                                awaysequence = awaypitch[pname[1]]  
                            if pitchseq in awaysequence:
                                awaysequence[pitchseq]=awaysequence[pitchseq]+1
                                awaypitch[pname[1]]=awaysequence
                            else:
                                awaysequence[pitchseq]=1
                                awaypitch[pname[1]]=awaysequence
        except:
            print("coulnt find this game")
                            
                        #print()

##
##    print("ab tot: " + str(count))
##    for item in awaypitch:
##        print(item)
##        print()
##        us = 0
##        sorted_away = sorted(awaypitch[item].items(), key=operator.itemgetter(1))
##        for seq in sorted_away:
##            if seq[1]>1:
##                print(seq)
##            else:
##                us += 1
##                #print(seq)
##    print()
##    print("Unique Sequences: " + str(us))
##    print()
##    
##    print()
##    for item in homepitch:
##        print(item)
##        print()
##        us = 0
##        sorted_home = sorted(homepitch[item].items(), key=operator.itemgetter(1))
##        for seq in sorted_home:
##            if seq[1]>1:
##                print(seq)
##            else:
##                us += 1
##    print()
##    print("Unique Sequences: " + str(us))
##    print()
    #print(homepitch,awaypitch)
    return(homepitch,awaypitch)


def formatstuff(data):
    for haset in data:
        for pitcher in haset:
            print(pitcher)
            print()
            us = 0
            for seq in haset[pitcher]:
                if haset[pitcher][seq]>1:
                    print(seq, haset[pitcher][seq])
                else:
                    #print(seq)
                    us += 1
            print()
            print("total unique sequences: " + str(us))
            print()
    #for item in homepitch:
        #print(item)
        #for seq in homepitch[item]:
            #print(seq)
    

    #getgamedata(2017, 4, "Yankees")

def firstpitch(data):
    fpd = {}
    abtot = 0
    for haset in data:
        for pitcher in haset:
            print(pitcher)
            print()
            print("first pitch percentages")
            for seq in haset[pitcher]:
                #print(seq[0:2])
                if seq[0:2] in fpd:
                    fpd[seq[0:2]]=fpd[seq[0:2]]+1
                    abtot = abtot + 1
                else:
                    fpd[seq[0:2]]=1
                    abtot = abtot + 1
            for i in fpd:
                print(i, "{:.2%}".format(float(fpd[i]/abtot)))
            fpd = {}
            abtot = 0
            print()

def stuff(data):
    for haset in data:
        for pitcher in haset:
            print(pitcher)
            print()
            for seq in haset[pitcher]:
                print(seq)  
            print()
    

       
            

        
    


