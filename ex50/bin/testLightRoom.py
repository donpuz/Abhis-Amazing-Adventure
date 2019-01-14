import sys
import time

'''Room with light'''

'''t0 = time.time()
timeallowed = 0
max_backpack = 0'''
all_dropped = []
dropped_lightRoom = []

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
    print('Right next to the bed, you spot a black object on the floor.')
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
    choicesText = ['1. sleep','2. look out the window','3. investigate the closet','4. check out the bookshelf','5. play Mo Bamba','6. take the torch','7. pick up the black object','8. leave the room','9. pick up dropped item'
                    ,'10. drop an item','11. open backpack'] # list of all possible choices
    for i in range(1, 12): # loops through all possible actions
        if i in choices: # True if action number i is a valid action
            print(choicesText[i-1]) # prints the corresponding valid choice
            
if __name__ == '__main__':
    player = Player()
    if player.mode == modes[0]:
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
    lightRoom(player)