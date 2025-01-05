'''
Created by: ABDUL BASIT
This is an interactive game with a computer.
It is like odd or even game you must have played in school.
If you dont understand the code....no worries!!!
Just play the game a few times and you'll get it
Enjoy and thanks for playing!!!
'''


# Odd or Even Game

# 1. First do TOSS
# Check TOSS conditions:
# Tie then re-TOSS
# if comp more, comp random select
# if player more, then provide options to player

# Then create defs for Comp batting, player batting
# Comp batting def
# Player batting def
# Keep playing even when Score is crossed to build a highscore

# make wicket options

# score calculating
# keep track of scores during game

# give a time break if possible

# result declaration
# winner!

# extension

'''
1] Make List of teams
2] Make points Table in SQL
3] Manipulate Points Table

Win=2 points
Draw==1 point each
Lose=no change
Continuous tournament
'''


import random
import time
import sys
import mysql.connector as m

db=m.connect(host='localhost', user='root', passwd='SQL', database='MyPL')
cur=db.cursor()

print('Welcome to MyPL'.center(180))
Options=['Bat', 'Ball']
Wicket_Options=['Stumped!', 'Bowled Out!', 'LBW!', 'Caught Out!', 'Run Out!', 'Hit Wicket!']
CTA=['MM', 'VV', 'LGE', 'MH', 'JG', 'SR', 'IN', 'US']
#Player and Computer Runs
CR,PR=0,0
T=0

Team_List=['1. Melter Mercury [ MM ]',
       '2. Venomous Venus [ VV ]',
       '3. LifeGreeny Earth [ LE ]',
       '4. Mars Heat [ MH ]',
       '5. Jupiter Giants [ JG ]',
       '6. Saturn Rockers [ SR ]',
       '7. Icy Neptune [ IN ]',
       '8. Uranus Strikers [ US ]']
print('Team List'.center(185))
for I in Team_List:
    print(I.center(180))

Light2='Green'
while Light2=='Green':
    try:
        Player_Team=input('Enter Team Abbreviation ONLY')
        if Player_Team.upper() in CTA:
            break
        else:
            print('Enter valid input')
    except:
        break
Flag2='Green'
while Flag2=='Green':
    Comp_Team=CTA[random.randint(0,7)]
    if Comp_Team!=Player_Team:
        break
print('Computer Team', Comp_Team)


def TOSS():
    print('TOSS in Progress')
    print()
    while True:
        CompMove=random.randint(1,6)
        Flag='Green'
        while Flag=='Green':
            try:
                PlayerMove=int(input('Enter a number from 1 to 6'))
                while PlayerMove>0 and PlayerMove<7:
                    Flag='Red'
                    break
                else:
                    print('Enter Valid Choice')
            except:
                print('Enter Valid Choice')
        print(Comp_Team, 'Plays [TOSS] >', CompMove)
        print()
        if CompMove==PlayerMove:
            continue
        
        elif CompMove!=PlayerMove:
            if CompMove>PlayerMove:
                CompChoice=Options[random.randint(0,1)]
                print()
                print(Comp_Team,'Chose To >', CompChoice)
                if CompChoice=='Bat':
                    COMPBAT()
                    break
                
                else:
                    PLAYERBAT()
                    break
                
            elif PlayerMove>CompMove:
                for I in Options:
                    print(I)
                UC=input('Make your choice [words]')
                while UC.lower()=='bat' or UC.lower()=='ball':
                    break
                else:
                    print('Enter Valid Choice')
                    
                if UC.lower()=='bat':
                    PLAYERBAT()
                    break
                
                elif UC.lower()=='ball':
                    COMPBAT()
                    sys.exit()


def PLAYERBAT():
    global CR
    global PR
    global T
    Light='Green'
    while Light!='Red':
        Flag='Green'
        while Flag=='Green':
            try:
                CompMove=random.randint(1,6)
                print(Comp_Team,'Plays [BALL] >', CompMove)
                PlayerMove=int(input('Enter a number from 1 to 6'))
                while PlayerMove>0 and PlayerMove<7:
                    Flag='Red'
                    break
                else:
                    print('Enter Valid Choice')
            except:
                print('Enter Valid Choice')
        print()
        if PlayerMove!=CompMove:
            PR+=PlayerMove
        else:
            if CR==0: # None has played yet or duck               
                if CompMove==PlayerMove:
                    print('You are', Wicket_Options[random.randint(0,3)])
                    time.sleep(2)
                    print()
                    
                    if T==0:
                        print(Player_Team,'Score >', PR)
                        time.sleep(2)
                        print(Comp_Team, 'Needs to Score', PR+1, 'Runs to Win')
                        print()
                        T+=1
                        time.sleep(5)
                        COMPBAT()
                        Light='Red'
                        
                    elif T!=0:
                        if PR==CR:
                            print('Game Drawn!')
                            time.sleep(2)
                            print()
                            print(Player_Team,'Score >', PR)
                            time.sleep(2)
                            print(Comp_Team,'Score >', CR)
                            cur.execute("update PT set Points=Points+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                            cur.execute("update PT set Drawn=Drawn+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                            cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                            db.commit()
                            cur.close()
                            db.close()
                            Light='Red'
                            
                elif CompMove!=PlayerMove and PR>CR and T!=0:
                    print('You Win!')
                    time.sleep(2)
                    print()
                    print(Player_Team,'Score >', PR)
                    time.sleep(2)
                    print(Comp_Team,'Score >', CR)
                    cur.execute("update PT set Points=Points+2 where Team_abbrev='{}'".format(Player_Team))
                    cur.execute("update PT set Games_Won=Games_Won+1 where Team_abbrev='{}'".format(Player_Team))
                    cur.execute("update PT set Games_Lost=Games_Lost+1 where Team_abbrev='{}'".format(Comp_Team))
                    cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                    db.commit()
                    cur.close()
                    db.close()
                    Light='Red'
                    
                else:
                    continue
            #
            #
            elif CR!=0: # If Computer has already played
                if PR>CR:
                    print('You Win!')
                    time.sleep(2)
                    print()
                    print(Player_Team,'Score >', PR)
                    time.sleep(2)
                    print(Comp_Team,'Score >', CR)
                    cur.execute("update PT set Points=Points+2 where Team_abbrev='{}'".format(Player_Team))
                    cur.execute("update PT set Games_Won=Games_Won+1 where Team_abbrev='{}'".format(Player_Team))
                    cur.execute("update PT set Games_Lost=Games_Lost+1 where Team_abbrev='{}'".format(Comp_Team))
                    cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                    db.commit()
                    db.close()
                    cur.close()
                    Light='Red'
                    
                elif PR<CR:
                    if CompMove==PlayerMove:
                        print('You are', Wicket_Options[random.randint(0,3)])
                        time.sleep(2)
                        print()
                        print('You Lose!')
                        time.sleep(2)
                        print()
                        print(Player_Team,'Score >', PR)
                        time.sleep(2)
                        print(Comp_Team,'Score >', CR)
                        cur.execute("update PT set Points=Points+2 where Team_abbrev='{}'".format(Comp_Team))
                        cur.execute("update PT set Games_Won=Games_Won+1 where Team_abbrev='{}'".format(Comp_Team))
                        cur.execute("update PT set Games_Lost=Games_Lost+1 where Team_abbrev='{}'".format(Player_Team))
                        cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                        db.commit()
                        cur.close()
                        db.close()
                        Light='Red'
                        
                    elif CompMove!=PlayerMove:
                        continue
                    
                elif PR==CR and PlayerMove==CompMove:
                    print('Game Drawn!')
                    time.sleep(2)
                    print()
                    print(Player_Team,'Score >', PR)
                    time.sleep(2)
                    print(Comp_Team,'Score >', CR)
                    cur.execute("update PT set Points=Points+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                    cur.execute("update PT set Drawn=Drawn+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                    cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                    db.commit()
                    cur.close()
                    db.close()
                    Light='Red'
                    
                else:
                    continue


def COMPBAT():
    global CR
    global PR
    global T
    Light='Green'
    while Light!='Red':
        Flag='Green'
        while Flag=='Green':
            try:
                CompMove=random.randint(1,6)
                print(Comp_Team,'Plays [BAT] >', CompMove)
                PlayerMove=int(input('Enter a number from 1 to 6'))
                while PlayerMove>0 and PlayerMove<7:
                    Flag='Red'
                    break
                else:
                    print('Enter Valid Choice')
            except:
                print('Enter Valid Choice')
        print()
        if PlayerMove!=CompMove:
            CR+=CompMove
        else:
            if PR==0: # None has played yet or duck
                if CompMove==PlayerMove:
                    print('Computer is', Wicket_Options[random.randint(0,3)])
                    time.sleep(2)
                    print()
                    
                    if T==0:
                        print(Comp_Team,'Score >', CR)
                        time.sleep(2)
                        print('You Need to Score', CR+1, 'Runs to Win')
                        print()
                        T+=1
                        time.sleep(5)
                        PLAYERBAT()
                        Light='Red'
                        
                    elif T!=0:
                        if PR==CR:
                            print('Game Drawn!')
                            time.sleep(2)
                            print()
                            print(Player_Team,'Score >', PR)
                            time.sleep(2)
                            print(Comp_Team,'Score >', CR)
                            cur.execute("update PT set Points=Points+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                            cur.execute("update PT set Drawn=Drawn+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                            cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                            db.commit()
                            cur.close()
                            db.close()
                            Light='Red'
                            
                elif CompMove!=PlayerMove and CR>PR and T!=0:
                    print('You Lose!')
                    time.sleep(2)
                    print()
                    print(Player_Team,'Score >', PR)
                    time.sleep(2)
                    print(Comp_Team,'Score >', CR)
                    cur.execute("update PT set Points=Points+2 where Team_abbrev='{}'".format(Comp_Team))
                    cur.execute("update PT set Games_Won=Games_Won+1 where Team_abbrev='{}'".format(Comp_Team))
                    cur.execute("update PT set Games_Lost=Games_Lost+1 where Team_abbrev='{}'".format(Player_Team))
                    cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                    db.commit()
                    cur.close()
                    db.close()
                    Light='Red'
                    
                else:
                    continue
                #
                #
            elif PR!=0: # If Player has already played
                if CR>PR:
                    print('You Lose!')
                    time.sleep(2)
                    print()
                    print(Player_Team,'Score >', PR)
                    time.sleep(2)
                    print(Comp_Team,'Score >', CR)
                    cur.execute("update PT set Points=Points+2 where Team_abbrev='{}'".format(Comp_Team))
                    cur.execute("update PT set Games_Won=Games_Won+1 where Team_abbrev='{}'".format(Comp_Team))
                    cur.execute("update PT set Games_Lost=Games_Lost+1 where Team_abbrev='{}'".format(Player_Team))
                    cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                    db.commit()
                    cur.close()
                    db.close()
                    Light='Red'
                    
                elif CR<PR:
                    if CompMove==PlayerMove:
                        print('Computer is', Wicket_Options[random.randint(0,3)])
                        time.sleep(2)
                        print()
                        print('You Win!')
                        time.sleep(2)
                        print()
                        print(Player_Team,'Score >', PR)
                        time.sleep(2)
                        print(Comp_Team,'Score >', CR)
                        cur.execute("update PT set Points=Points+2 where Team_abbrev='{}'".format(Player_Team))
                        cur.execute("update PT set Games_Won=Games_Won+1 where Team_abbrev='{}'".format(Player_Team))
                        cur.execute("update PT set Games_Lost=Games_Lost+1 where Team_abbrev='{}'".format(Comp_Team))
                        cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                        db.commit()
                        cur.close()
                        db.close()
                        Light='Red'
                        
                    elif CompMove!=PlayerMove:
                        continue
                    
                elif PR==CR and PlayerMove==CompMove:
                    print('Game Drawn!')
                    time.sleep(2)
                    print()
                    print(Player_Team,'Score >', PR)
                    time.sleep(2)
                    print(Comp_Team,'Score >', CR)
                    cur.execute("update PT set Points=Points+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                    cur.execute("update PT set Drawn=Drawn+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Comp_Team, Player_Team))
                    cur.execute("update PT set Matches_Played=Matches_Played+1 where Team_abbrev='{}' or Team_abbrev='{}'".format(Player_Team, Comp_Team))
                    db.commit()
                    cur.close()
                    db.close()
                    Light='Red'
                    
                else:
                    continue

#TOSS()


# To Display points table Results at any time

UC=input('Do you wanna see points table? [Y/N]')
if UC.lower()=='y':
    db=m.connect(host='localhost', user='root', passwd='SQL', database='MyPL')
    cur=db.cursor()
    cur.execute('select * from PT order by Points desc')
    recs=cur.fetchall()
    for I in range(len(recs)):
        print(str(I+1)+'. '+ recs[I][0] + ' (' + recs[I][1] + ') - ' + str(recs[I][6]))
        print()
    cur.close()
    db.close()


# Input values into Table

'''
db=m.connect(host='localhost', user='root', passwd='SQL', database='MyPL')
cur=db.cursor()
N=int(input("Enter number of records you want to enter"))
for I in range(N):
    TN=input('Enter team name')
    WON = 0
    LOST = 0
    DRAWN = 0
    MATCHES_PLAYED = 0
    POINTS = 0
    TA=input('Enter Team Abbreviation')
    cur.execute("insert into PT values('{}','{}',{},{},{},{},{})".format(TN,TA,WON,LOST,MATCHES_PLAYED,DRAWN,POINTS))
    db.commit()
cur.close()
db.close()
'''

#Table creating command

"create Table PT(Team_Name varchar(50), Team_abbrev varchar(2), Games_Won int, Games_Lost int, Drawn int, Matches_Played int, Points int);"
