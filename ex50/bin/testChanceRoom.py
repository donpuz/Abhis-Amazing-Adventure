import sys
import time
import random
import math

'''red, black, or green roulette choice 3 times''' # 18 red and black spaces, 1 green space
# Make so that can only open when certain amount of items are found
# Could be that need certain items (say 3 coins) needed to start the roulette game
def chanceRoom(player): # Make a player parameter later
    global timeallowed
    global t0
    global all_dropped # global list with all dropped items across rooms
    global dropped_chanceRoom # global list with dropped items in roulette room
    
    choices = [1,2,3,4,5]
    action = 0
    droppedItems = []
    
    print('The room is very bright and flashy.')
    print('There is a roulette table in the middle of the room, but it doesn\'t appear to be working.')
    print('On the side of the table are three circular slots. They look like someone needs to be inserted there.')
    print('Besides the slots rests a green coin.')
    
    while (action != 3): # Runs until user wants to leave the room
        '''if time.time() - t0 > timeallowed:   # Timer countdown
            print 'Game over! You ran out of time.'
            sys.exit()'''
        printChanceChoices(choices)
        action = int(raw_input('Your choice: '))
        if (action in choices):
            
            
            # if (action == 1 and 'red coin' in player.backpack and 'black coin' in player.backpack and 'green coin' in player.backpack): # gamble and True if all coins in backpack
            if (action == 1):
                print('You insert the coins into the slots ')
                print('\nYou are playing roulette. In order to win, guess the correct color 3 times in a row.')
                print('In roulette, a ball rolls around the roulette wheel and lands in a random slot.')
                print('There are 18 red spots, 18 black spots, and 1 green spot.')
                print('The spots are numbered 0-36. Zero is green, the odd spots are red, and the other even spots are black.')
                if (playRoulette()):
                    print('\nYou win! You hear a small click inside the walls and a creaking sound, like a door being opened.')
                    print('You go back through the door and see the previously locked door opened. Curious, you investigate.')
                    # <-------------------------------------------------------------------------------------------------------------- function to open victory room
                    choices.remove(1)
                    
                    
            elif (action == 1 and not ('red coin' in player.backpack and 'black coin' in player.backpack and 'green coin' in player.backpack)): # gamble and True if not all coins in backpack
                print('\nThe roulette table doesn\'t seem to work. If only you could find a way to get it to work...')
                
                
            elif (action == 2): # green coin
                print('It looks like it would fit in one of the slots.')
                if (not player.pickUpIntent('green coin')): # True if the player does not pick up the object
                    choices.append(2)
                
                
            elif (action == 4):
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
                if (len(player.backpack) > 0):
                    drop = raw_input('Object you want to drop: ')
                    if drop in player.backpack:
                        dropped_chanceRoom.append(drop)
                    player.removeItem(drop)
                else:
                    print('You have no items in your backpack to drop.')
                    
                    
            elif (action == 6): # opening the backpack
                player.openBackpack()
                
            if (action == 2): # True if action is 2 or 3
                choices.remove(action) # once action is taken, removes it from possible choices list if action is not picking up or dropping item or opening backpack
        else:
            print('Not valid choice or action already taken. Input again.')
    print('\nYou leave the room.')
        
def printChanceChoices(choices):
    time.sleep(2) # allows the user to process what happened after their last action
    print('\nChoices: ')
    choicesText = ['1. gamble','2. pick up the green coin','3. leave the room','4. pick up an item', '5. drop an item', '6. open backpack'] # list of all possible choices
    for i in range(1, 7): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice
            
def playRoulette(): # returns True if player wins, False otherwise
    guessRight = 0 # How many times the user guessed right
    success = False # If the user succeeded or not
    while (guessRight < 3): # <---------------------------------------------------------------------------------------------------------- CHANGE TO 3 LATER
        rGuess = raw_input('\nRed (r), Black (b), Green (g): ') # Red is odd numbers, Black is even numbers apart from 0, and Green is 0
        rNum = random.randint(0,36) # Random number rolled
        croupier(rNum)
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
    if (guessRight == 3): # <------------------------------------------------------------------------------------------------------------ CHANGE TO 3 LATER
        success = True
    return success
    
def croupier(roll):

    s = .05
    for i in range (37):
        
        sys.stdout.write("\r%d " % i)

        sys.stdout.flush()
        time.sleep(s)

        
    for i in range (37):
        
        sys.stdout.write("\r%d " % i)

        sys.stdout.flush()
        time.sleep(s)
        
    for i in range(roll):
        
        sys.stdout.write("\r%d " % i)
        sys.stdout.flush()
        time.sleep(s)
        
    for i in range(roll,37+roll):
        if (i >= 36):
            sys.stdout.write("\r%d " % (i - 36))
        else:
            sys.stdout.write("\r%d " % i)
        sys.stdout.flush()
        s *= 1.05
        time.sleep(s)
    
chanceRoom('test')

# https://stackoverflow.com/questions/3249524/print-in-one-line-dynamically