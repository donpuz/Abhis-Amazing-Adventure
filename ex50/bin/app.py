import sys
import time
import random
import math

t0 = time.time()
timeallowed = 0
max_backpack = 0
modes = ['easy', 'normal', 'hard', 'insane']
all_dropped = [] # list of all dropped items
dropped_lightRoom = [] # list of all dropped items in respective room
dropped_stairRoom = []
dropped_cataRoom = []
dropped_chanceRoom = []
doorOpened = False
sarc_opened = False
locked = True

class Player:
    backpack = [] # backpack list
    mode = ''
    
    def __init__(self): # opening code
        self.mode = raw_input('What difficulty would you like? 0-3 ')
        while True:
            if self.mode.isdigit() and int(self.mode) in [0, 1, 2, 3]: # catches invalid user input
                self.mode = modes[int(self.mode)]
                break
            else:
                print('Not a valid mode.')
        print 'You have chosen %s mode.' % (self.mode)
        
    def openBackpack(self): # open backpack
        if len(self.backpack)==0: # True if backpack is empty
            print 'Backpack is empty.'
        else:
            print 'Here is your inventory:'
            for item in self.backpack:
                print item
            
    def addItem(self, item): # adds given item
        global max_backpack
        if len(self.backpack)<max_backpack: # True if enough space in backpack
            self.backpack.append(item)
            print 'You picked up %s' % item
        else:
            print 'Backpack is full. Could not pick up %s' % item
    
    def removeItem(self, item): # removes given item
        if item in self.backpack: # True if item in backpack
            self.backpack.remove(item)
            print '%s has been dropped.' % item
            all_dropped.append(item)
            return item
        else:
            print 'You aren\'t carrying that item.'
            return None
            
    def pickUpIntent(self, item): # user decides whether pick up item
    	choice = raw_input('Do you want to pickup the ' + item + '? Please input y/yes or n/no. ')
    	active = True
    	state = False
    	while (active): # runs until user inputs valid input
            if (choice == 'y' or choice == 'yes'):
                self.addItem(item)
            	state = True
            	active = False
            elif(choice == 'n' or choice == 'no'):
                print('You leave the ' + item + '.')
            	active = False
            else:
            	choice = raw_input('Please input y/yes or n/no. ')
    	return state
            
    
        
def start(player): # start room
    global timeallowed
    global t0
    choices = [1, 2, 3] # list of choices player can make
    action = 0
    
    print('\nYou come across a crossroads.')
    print('You look around.')
    print('To the North is a bedroom.')
    print('To the West is an ominous door.')
    print('To the East is a dark stairwell.\n')
    
    if time.time()-t0 > timeallowed: # Timer countdown
        print '\nGame over! You ran out of time.'
        return None
    printStartChoices(choices) # prints all valid choices
    action = raw_input('\nYour choice: ')
    if action.isdigit() and int(action) in choices: # catches invalid user input
        action = int(action)
        if action == 1: # north bedroom
            print ('You go north.')
            time.sleep(0)
            lightRoom(player)
        elif action == 2: # west locked room
            print ('You go west.')
            time.sleep(0)
            doorRoom(player)
        else: # east stair room
            print ('You go east.')
            time.sleep(0)
            stairRoom(player)
    else:
        print('Not valid choice. Input again.')
                
        
def printStartChoices(choices): # prints all actions that can be taken
    time.sleep(0) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. go north','2. go west','3. go east'] # list of all possible choices
    for i in range(1,4): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice
            
def stairRoom(player):
    global timeallowed
    global t0
    global all_dropped
    global dropped_stairRoom
    choices = [1, 2, 3, 4, 5] # list of choices player can make
    action = 0
    torchout = False
    
    print('\nYou come to a dark stairwell. You smell death and decay.')
    print('You can not see what lies ahead.\n')
    
    
    if 'torch' in player.backpack and 6 not in choices: # adds valid choice
        choices.append(6)
    while True:
        if time.time() - t0 > timeallowed: # Timer countdown
            print '\nGame over! You ran out of time.'
            return None
        if torchout: # adds valid choices and removes valid choices
            if 6 in choices:
                choices.remove(6)
            if 7 not in choices:
                choices.append(7)
        if not torchout:
            if 6 not in choices and 'torch' in player.backpack:
                choices.append(6)
            if 7 in choices:
                choices.remove(7)
        printStairChoices(choices) # prints all valid choices
        action = raw_input('\nYour choice:')
        if action.isdigit() and int(action) in choices: # catches invalid user inputs
            action = int(action)
            if action == 1 and torchout == False: # staircase with no torch or torch not taken out
                print('\nYou fall down the staircase and swiftly break your neck. Game over!')
                return None
            elif action == 1 and torchout == True: # staircase with torch taken out
                print('\nYou descend the stairs.')
                time.sleep(0)
                catacombRoom(player)
                return None
            elif action == 2: # leave
                print('\nYou wisely turn around.')
                if torchout == True:
                    print('\nYou put away your torch.')
                time.sleep(0)
                start(player)
                return None
            elif (action == 3): # opening the backpack
                player.openBackpack()
            elif (action == 4): # dropping an item
                if (len(player.backpack) > 0):
                    drop = raw_input('Object you want to drop: ')
                    if drop in player.backpack:
                        dropped_stairRoom.append(drop)
                    player.removeItem(drop)
                else:
                    print('You have no items in your backpack to drop.')
            elif (action == 5): # pick up item
                print('\nThe items dropped in the current room are '+str(dropped_stairRoom))
                if (len(dropped_stairRoom) > 0): # Checks if there are dropped items
                    pickUp = raw_input('Object you want to pick up: ')
                    if (pickUp in dropped_stairRoom): # True if item is on the floor
                        player.addItem(pickUp)
                        all_dropped.remove(pickUp)
                        dropped_stairRoom.remove(pickUp)
                    else:
                        print('Not a valid item.')
                else:
                    print('There are currently no items dropped to pick up.')
            elif action == 6: # pull out torch
                print('\nYou pull out your torch, illuminating the stair case.')
                print('The staircase is made of bones.')
                torchout = True
            else: # put away torch
                print('\nYou put away your torch. The staircase falls into darkness.')
                torchout = False
        else:
            print('Not valid choice. Input again.\n')

    
        
def printStairChoices(choices): # prints all actions that can be taken
    time.sleep(0) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. descend the stairs','2. turn back', '3. open your backpack', '4. drop an item', '5. pick up dropped item', '6. pull out your torch', '7. put away your torch.'] # list of all possible choices
    for i in range(1, 8): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice
            
def catacombRoom(player):
    global timeallowed
    global t0
    global all_dropped
    global dropped_cataRoom
    global sarc_opened
    choices = [1, 2, 3, 4, 5, 6, 7, 8] # list of choices player can make
    action = 0
    
    if sarc_opened == True and 9 not in choices: # adds valid choices and removes invalid choices
        choices.append(9)
        
    if sarc_opened == True and 10 not in choices:
        choices.append(10)
        
    if sarc_opened == True and 2 in choices:
        choices.remove(2)
        
    if 'red coin' in all_dropped or 'red coin' in player.backpack and 3 in choices: # makes sure that if player has picked up item before, can't pick up again
        choices.remove(3)
    
    if 'crown' in all_dropped or 'crown' in player.backpack and 5 in choices:
        choices.remove(5)
        
    if 'finger' in all_dropped or 'finger' in player.backpack and 9 in choices:
        choices.remove(9)
    
    if 'toe' in all_dropped or 'toe' in player.backpack and 10 in choices:
        choices.remove(10)
    
    print('\nYou come to a room decorated in bones, lit only by your torch. The stench of death is more powerful now.')
    print('In the center of the room you see a golden sarcophagus.')
    print('Lying to the right side of the room is a red coin.')
    print('To the left side of the room lies a lever with a label attached: \"mortem\"')
    print('Lying next to the sarcophagus is a golden crown embedded with rubies.\n')
    
    while True:
        if sarc_opened == True and 9 not in choices:
            choices.append(9)
        
        if sarc_opened == True and 10 not in choices:
            choices.append(10)
        
        if sarc_opened == True and 2 in choices:
            choices.remove(2)
        
        if 'red coin' in all_dropped or 'red coin' in player.backpack and 3 in choices:
            choices.remove(3)
    
        if 'crown' in all_dropped or 'crown' in player.backpack and 5 in choices:
            choices.remove(5)
        
        if 'finger' in all_dropped or 'finger' in player.backpack and 9 in choices:
            choices.remove(9)
    
        if 'toe' in all_dropped or 'toe' in player.backpack and 10 in choices:
            choices.remove(10)
        
        if time.time() - t0 > timeallowed:   # Timer countdown
            print 'Game over! You ran out of time.'
            return None
        printCataChoices(choices) # prints all available choices
        action = raw_input('Your choice: ')
        if action.isdigit() and int(action) in choices: # catches invalid user inputs
            action = int(action)
            if action == 1: # leave
                print('\nYou wisely turn around.')
                time.sleep(0)
                start(player)
                return None
            elif action == 2: # sarcophagus
                sarc_opened = True
                print('\nYou open the sarcophagus.')
                print('In it lies the skeleton of a king long gone.')
                print('A gorgeous ruby ring on his left hand catches your attention.')
                print('You then see his grotesquely malformed big toe, which has fallen off of his foot.')
            elif action == 3: # red coin
                player.addItem('red coin')
            elif action == 4: # death lever
                print('The lever electrocutes you and you die. Game Over!')
                return None
            elif action == 5: # crown
                player.addItem('crown')
            elif action == 6: # open backpack
                player.openBackpack()
            elif action == 7: # dropping an item
                if (len(player.backpack) > 0):
                    drop = raw_input('Object you want to drop: ')
                    if drop in player.backpack:
                        dropped_cataRoom.append(drop)
                    player.removeItem(drop)
                else:
                    print('You have no items in your backpack to drop.')
            elif (action == 8): # pick up item
                print('\nThe items dropped in the current room are '+str(dropped_cataRoom))
                if (len(dropped_cataRoom) > 0): # Checks if there are dropped items
                    pickUp = raw_input('Object you want to pick up: ')
                    if (pickUp in dropped_cataRoom): # True if item is on the floor
                        player.addItem(pickUp)
                        all_dropped.remove(pickUp)
                        dropped_cataRoom.remove(pickUp)
                    else:
                        print('Not a valid item.')
                else:
                    print('There are currently no items dropped to pick up.')
            elif action == 9: # ring after sarcophagus
                print('As you try to grab the ring, the entire finger breaks off of the skeleton.')
                player.addItem('finger')
            else: # toe after sarcophagus
                player.addItem('toe')
                
        
def printCataChoices(choices):
    time.sleep(0) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. turn back','2. open sarcophagus', '3. pick up coin', '4. pull lever', '5. pick up crown', '6. open your backpack', '7. drop an item', '8. pick up dropped item', '9. take ring',
                    '10. take toe'] # list of all possible choices
    for i in range(1, 11): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice
            
def doorRoom(player): # locked door room
    global timeallowed
    global t0
    global doorOpened # True if locked door is open
    global locked
    
    choices = [1, 2, 3, 4]
    
    if doorOpened and 3 in choices: # removes invalid choices
        choices.remove(3)
    if doorOpened and 2 in choices:
        choices.remove(2)
    if doorOpened and 5 not in choices:
        choices.append(5)
    if not locked and not doorOpened and 3 in choices:
        choices.remove(3)
    
    print ('\nYou come to a door surrounded in bones.')
    print ('There is a large handle made of a human femur.')
    print ('There is a keyhole.\n')
    
    while True: # removes invalid choices
        if doorOpened and 3 in choices:
            choices.remove(3)
        if doorOpened and 2 in choices:
            choices.remove(2)
        if doorOpened and 5 not in choices:
            choices.append(5)
        if not locked and not doorOpened and 3 in choices:
            choices.remove(3)
        
        if time.time() - t0 > timeallowed:   # Timer countdown
            print '\nGame over! You ran out of time.'
            return None
        printDoorChoices(choices) # prints all valid choices
        action = raw_input('Your choice: ')
        if action.isdigit() and int(action) in choices: # catches invalid user inputs
            action = int(action)
            if action == 1:
                print ('\nYou turn around.')
                start(player)
                return None
            elif action == 2:
                if locked:
                    print ('\nThe door is locked.')
                else:
                    print ('\nThe door swings open. You see a roulette table in the distance.')
                    doorOpened = True
                    choices.append(5)
                    choices.remove(2)
            elif action == 3: # keyhole
                key = raw_input('\nWhich item would you like to place in the keyhole? ')
                if key not in player.backpack: # True if user doesn't have item they want to put in keyhole
                    print('You don\'t have that item.')
                else:
                    if key == 'finger':
                        print ('The finger fits perfectly in the key hole. You turn it and the door unlocks.')
                        locked = False
                        player.removeItem(key)
                    else:
                        print ('The %s does not fit in the key hole. It is returned to your inventory.') % key
            elif action == 5: # go through locked door
                print ('You go through the door.')
                chanceRoom(player)
                return None
            else: # open backpack
                player.openBackpack()
        else:
            print ('Not a valid choice.')
        
def printDoorChoices(choices):
    time.sleep(0) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. turn around','2. open the door','3. place item in keyhole', '4. open backpack', '5. go through door'] # list of all possible choices
    for i in range(1, 12): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice

def victoryRoom(player): # victory room
    print ("Congratulations! You have won Abhi's Amazing Adventure! They are serving fresh ice, just for victors.")
    print ('\nChoices:')
    print("1. get some ice\n2. end game")
    action = raw_input('Your choice: ')
    while True:
        if action.isdigit() and int(action) in [1, 2]: # catches invalid user inputs
            action = int(action)
            if action == 1:
                print ("You enjoy your ice and the rest of your life.")
                return None
            elif action == 2:
                print ("You can't leave without getting ice.")
                print ('\nChoices:')
                print("1. get some ice")
                action = raw_input('Your choice: ')
        else:
            print('Not a valid choice.')
    
    
    
    
    
'''Room with light'''

def lightRoom(player):
    global timeallowed
    global t0
    global all_dropped
    global dropped_lightRoom 
    
    choices = [1,2,3,4,5,6,7,8,9,10,11] # list of choices player can make
    if 'umbrella' in all_dropped or 'umbrella' in player.backpack: # makes sure that if player has picked up item before, can't pick up again
        choices.remove(3)
    if 'torch' in all_dropped or 'torch' in player.backpack:
        choices.remove(6)
    if 'bad book' in all_dropped or 'bad book' in player.backpack:
        choices.remove(4)
    if 'black coin' in all_dropped or 'black coin' in player.backpack:
        choices.remove(7)
    action = 0
    
    print('\nYou enter a room ominously lit with a torch.')
    print('There is a bed in the corner. It looks very comfortable.')
    print('Right next to the bed, you spot a black coin on the floor.')
    print('The room only has one window, just above the bed on the far wall.')
    print('Other than the bed, there are only two other pieces of furniture in the room: a closet and a bookshelf.')
    print('On top of the bookshelf lies a CD. It is labeled \'Mo Bamba.\'\n')
    
    while (action != 8): # Runs until user wants to leave the room (option 8)
        if time.time() - t0 > timeallowed:   # Timer countdown
            print 'Game over! You ran out of time.'
            return None
        printLightChoices(choices) # prints all available choices
        action = raw_input('Your choice: ')
        if action.isdigit() and int(action) in choices: # catches invalid user inputs
            action = int(action)
            if (action == 1): # sleep
                print('\nGame over. You slept until the timer ran out.')
                return None
                
                
            elif (action == 2): # window
                print('\nYou see nothing. It was a big waste of time.')
                
                
            elif (action == 3): # closet
                print('\nYou throw open the door of the closet. No Narnia here; it\'s not a wardrobe.')
                print('You find an umbrella.')
                if (not player.pickUpIntent('umbrella')): # True if the player does not pick up the object
                    choices.append(3) # If user does not pick up object, keep choice (can pick up in future)
                    
                    
            elif (action == 4): # bookshelf
                print('\nThe bookshelf has only one book on it: The Forest Unseen by David George Haskall.')
                print('You find it disgusting.')
                if (not player.pickUpIntent('bad book')):
                    choices.append(4)
                    
                    
            elif (action == 5): # Mo Bamba
                print('\nYou remember Ms. Pannapara\'s advice to have a respectful fear of fire.')
                print('You back away in sheer terror.')
                
                
            elif (action == 6): # torch
                print('\nExercising lab safety, you put on your rubber heat gloves.')
                if (not player.pickUpIntent('torch')):
                    choices.append(6)
                    
                    
            elif (action == 7): # mysterious black object
                print('You walk over and see that it is a black coin.')
                if (not player.pickUpIntent('black coin')):
                    choices.append(7)
                
                
            elif (action == 9): # pick up item
                print('\nThe items dropped in the current room are '+str(dropped_lightRoom))
                if (len(dropped_lightRoom) > 0): # Checks if there are dropped items
                    pickUp = raw_input('Object you want to pick up: ')
                    if (pickUp in dropped_lightRoom): # True if item is on the floor
                        player.addItem(pickUp)
                        all_dropped.remove(pickUp)
                        dropped_lightRoom.remove(pickUp)
                    else:
                        print('Not a valid item.')
                else:
                    print('There are currently no items dropped to pick up.')
                    
                    
            elif (action == 10): # dropping an item
                if (len(player.backpack) > 0): # checks if user can drop item
                    drop = raw_input('Object you want to drop: ')
                    if drop in player.backpack:
                        dropped_lightRoom.append(drop)
                    player.removeItem(drop)
                else:
                    print('You have no items in your backpack to drop.')
                    
                    
            elif (action == 11): # opening the backpack
                player.openBackpack()
                
                
            if (not action >= 9): # True if action is not picking up item, dropping item, or opening backpack
                choices.remove(action) # once action is taken, removes it from possible choices list if action is not picking up or dropping item or opening backpack
        else:
            print('Not valid choice. Input again.')
    print('\nYou turn around.') # leave
    start(player) # enter start room

def printLightChoices(choices): # prints all actions that can be taken
    time.sleep(0) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. sleep','2. look out the window','3. investigate the closet','4. check out the bookshelf','5. play Mo Bamba','6. take the torch','7. pick up the black coin','8. leave the room','9. pick up dropped item'
                    ,'10. drop an item','11. open backpack'] # list of all possible choices
    for i in range(1, 12): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice


def chanceRoom(player):
    global timeallowed
    global t0
    global all_dropped 
    global dropped_chanceRoom 
    
    choices = [1,2,3,4,5] # list of choices player can make
    if 'green coin' in all_dropped or 'green coin' in player.backpack: # makes sure that if player has picked up item before, can't pick up again
        print('why tho')
        choices.remove(2)
    action = 0
    
    print('\n\nYou enter a room which is very bright and flashy.')
    print('There is a roulette table in the middle of the room, but it doesn\'t appear to be working.')
    print('On the side of the table are three circular slots. They look like something needs to be inserted there.')
    print('Besides the slots rests a green coin.')
    
    while (action != 3): # Runs until user wants to leave the room (action 3)
        if time.time() - t0 > timeallowed:   # Timer countdown
            print 'Game over! You ran out of time.'
            sys.exit()
        printChanceChoices(choices)
        action = raw_input('Your choice: ')
        # 0 1 6 y 8 3 6 1 2 9 1 2 3 finger 2 5
        if action.isdigit() and int(action) in choices: # catches invalid user inputs
            action = int(action)
            if (action == 1 and 'red coin' in player.backpack and 'black coin' in player.backpack and 'green coin' in player.backpack): # gamble and True if all coins in backpack
                print('\nYou insert the the red, black, and green coins into the slots ')
                print('You are playing roulette. In order to win, guess the correct color 3 times in a row.')
                print('In roulette, a ball rolls around the roulette wheel and lands in a random slot.')
                print('There are 18 red spots, 18 black spots, and 1 green spot.')
                print('The spots are numbered 0-36. Zero is green, the odd spots are red, and the other even spots are black.')
                
                player.backpack.remove('black coin') # remove coins from backpack
                player.backpack.remove('red coin')
                player.backpack.remove('green coin')
                
                if (playRoulette()): # True if win roulette game
                    print('\nYou win! You hear a small click inside the walls and a creaking sound, like a door being opened.')
                    print('You go back through the door and see the previously locked door opened. Curious, you investigate.')
                    victoryRoom(player)
                    choices.remove(1)
                    
                    
            elif (action == 1 and not ('red coin' in player.backpack and 'black coin' in player.backpack and 'green coin' in player.backpack)): # gamble and True if not all coins in backpack
                print('\nThe roulette table doesn\'t seem to work. If only you could find a way to get it to work...')
                
                
            elif (action == 2): # green coin
                print('It looks like it would fit in one of the slots.')
                if (not player.pickUpIntent('green coin')): # True if the player does not pick up the object
                    choices.append(2)
                
                
            elif (action == 4): # pick up item
                print('\nThe items dropped in the current room are '+str(dropped_chanceRoom))
                if (len(dropped_chanceRoom) > 0): # Checks if there are dropped items
                    pickUp = raw_input('Object you want to pick up: ')
                    if (pickUp in dropped_chanceRoom): # True if item is on the floor
                        player.addItem(pickUp)
                        all_dropped.remove(pickUp)
                        dropped_chanceRoom.remove(pickUp)
                    else:
                        print('Not a valid item.')
                else:
                    print('There are currently no items dropped to pick up.')
                    
                    
            elif (action == 5): # dropping an item
                if (len(player.backpack) > 0): # checks if user can drop item
                    drop = raw_input('Object you want to drop: ')
                    if drop in player.backpack:
                        dropped_chanceRoom.append(drop)
                    player.removeItem(drop)
                else:
                    print('You have no items in your backpack to drop.')
                    
                    
            elif (action == 6): # opening the backpack
                player.openBackpack()
                
            if (action == 2): # True if action is not picking up item, dropping item, or opening backpack
                choices.remove(action) # once action is taken, removes it from possible choices list if action is not picking up or dropping item or opening backpack or gambling
        else:
            print('Not valid choice or action already taken. Input again.')
    print('\nYou leave the room.') # leave
    doorRoom(player) # opens locked door room
        
def printChanceChoices(choices):
    time.sleep(2) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. gamble','2. pick up the green coin','3. leave the room','4. pick up an item', '5. drop an item', '6. open backpack'] # list of all possible choices
    for i in range(0, 7): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice
            
def playRoulette(): # returns True if player wins, False otherwise
    guessRight = 0 # How many times the user guessed right
    success = False # If the user succeeded or not
    while (guessRight < 3):
        rGuess = raw_input('\nRed (r), Black (b), Green (g): ') # Red is odd numbers, Black is even numbers apart from 0, and Green is 0
        rNum = random.randint(0,36) # Random number rolled
        croupier(rNum) # animated roll
        print('\n')
        if (rGuess == 'r'): # True if user guessed red
            if (rNum % 2 == 1): # True if user is right
                guessRight += 1
                print('You guessed right! You have guessed right '+str(guessRight)+' time(s) in a row!')
            else: # If user is wrong
                print('You guessed wrong! Start over.')
                break
        elif (rGuess == 'b'): # True if user guessed black and got it right
            if (rNum % 2 == 0 and rNum != 0):   
                guessRight += 1
                print('You guessed right! You have guessed right '+str(guessRight)+' time(s) in a row!')
            else: # If user is wrong
                print('You guessed wrong! Start over.')
                break
        elif (rGuess == 'g'): # True if user guessed green and got it right
            if (rNum == 0):
                guessRight += 1
                print('You guessed right! You have guessed right '+str(guessRight)+' time(s) in a row!')
            else: # If user is wrong
                print('You guessed wrong! Start over.')
                break
        else: # Invalid input
            print('Invalid input. Try again.')
    if (guessRight == 3):
        success = True
    return success
    
def croupier(roll): # animated roll

    s = .05
    for i in range (37): # first cycle
        
        sys.stdout.write("\r%d " % i)

        sys.stdout.flush()
        time.sleep(s)

        
    for i in range (37): # second cycle
        
        sys.stdout.write("\r%d " % i)

        sys.stdout.flush()
        time.sleep(s)
        
    for i in range(roll): # third cycle
        
        sys.stdout.write("\r%d " % i)
        
        sys.stdout.flush()
        time.sleep(s)
        
    for i in range(roll,37+roll): # fourth cycle, slows down based on what number need to roll
        if (i >= 36):
            sys.stdout.write("\r%d " % (i - 37))
        else:
            sys.stdout.write("\r%d " % i)
        sys.stdout.flush()
        s *= 1.05
        time.sleep(s)

if __name__ == '__main__':
    player = Player()
    if player.mode == modes[0]: # mode selection
        print 'You will have 15 minutes to win the game and 10 backpack slots. You should be ashamed, scrub.'
        n=15
        max_backpack = 10
    elif player.mode == modes[1]:
        print 'You will have 10 minutes to win the game and 10 backpack slots. Good luck.'
        n=10
        max_backpack = 10
    elif player.mode == modes[2]:
        print 'You will have 5 minutes to win the game and 5 backpack slots. Good luck, you\'re gonna need it.'
        n=5
        max_backpack = 5
    elif player.mode == modes[3]:
        print 'You will have 1 minute to win the game and 3 backpack slots. Good luck, you\'re really gonna need it.'
        n=1
        max_backpack = 3
    timeallowed = n*60
    start(player) # enter start room