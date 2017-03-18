""" 

 CMPUT 396 Assignment 3
 Created by Andrea Whittaker 1386927
 And Mercy Woldmariam 1413892

 --- RUSH HOUR ---

 The Objective: slide the red car through the exit to freedom!
 
 To Play: slide the blocking cars and trucks in their lanes
 (up and down, left and right) until the path is clear for the red
 car to escape
 
"""
from sys import exit
import random
from random import shuffle

blocking_vehicles = ['B','C','E','F','G','H','I','J','K','L','M','N','O','P','Q'] # the game has 15 blocking cars and trucks
wall = '#'
space = '.'
exit = '!'
red = 'R'  # this is your red car
directions = ['w', 'a', 's', 'd'] # up, left, down, right
side_len = 8
selected_vehicle = red

class Board:
    
    # read the puzzle from a file
    def __init__(self, infile):
        
        self.lines = []
        self.original = []
        
        for line in infile:
            self.lines.append(line.strip('\n'))
        
        for i in range(side_len):
            assert(self.lines[0][i] == wall 
                   and self.lines[side_len-1][i] == wall)   # make sure top and bottom walls are solid
        assert(self.lines[3][side_len-1] == exit)           # make sure there is an exit at the right spot
        for line in self.lines:
            assert(line[0] == wall and (line[7] == wall or exit))   # make sure left and right walls are solid
        
        infile.close()
        self.original = self.lines[:]  
            
        return

    def resetBoard(self):
        
        self.lines = self.original[:]
        return
    
    # print the current state to stdout in a more readable format
    def prettyPrint(self):
        
        for line in self.lines:
            for x in line:
                print(x,' ',end='') # add spaces for readability
            print('')
        print('')
        
        return
    
    # match vehicles with their legal moves and size
    def organizeVehicles(self):
        
        self.vehicles = {}
        self.vehicles[red] = (0, 2)                         # add the direction that red can go to the dictionary        
        for i in range(side_len):
            for j in range(side_len):
                letter = self.lines[i][j]
                if letter in blocking_vehicles and letter not in self.vehicles:
                    if self.lines[i][j+1] == letter:                # vehicle is horizontal
                        if self.lines[i][j+2] == letter:
                            self.vehicles[letter] = (0, 3) # 0 for moving left or right, 3 for size 3
                        else:
                            self.vehicles[letter] = (0, 2) # 0 for moving left or right, 2 for size 2
                        
                    else:                                   # if it isn't horizontal, it must be vertical
                        if self.lines[i+2][j] == letter:                           
                            self.vehicles[letter] = (1, 3) # 1 for moving up or down, 3 for size 3
                        else:
                            self.vehicles[letter] = (1, 2) # 1 for moving up or down,, 2 for size 2 
                            
        
        return
        
    # move the selected vehicle in a legal direction
    # returns 0 if changing vehicles (won't print the board again),
    def chooseMove(self, move):
        
        bump = False
        result = 0
        if move not in directions:  # if the user selected a new vehicle, change it and return
            move = move.upper()
            if move not in self.vehicles and move != red:    # vehicle does not exist
                print("that vehicle does not exist!")
            else:
                global selected_vehicle
                selected_vehicle = move
                print("changed vehicle to " + selected_vehicle + ".")
            return 0, bump
        
        # make sure that the move does not run into a wall or another vehicle
        if move == 'w':
            if self.vehicles[selected_vehicle][0] != 1:
                print("stay in your lane!")
                return 0, bump
            
            for i in range(side_len-1, -1, -1):       # travel through the lines from bottom left to top right
                for j in range(side_len):
                    if self.lines[i][j] == selected_vehicle:
                        size = self.vehicles[selected_vehicle][1]
                        if self.lines[i-size][j] != space and self.lines[i-size][j] != exit:    # the spot above it is not an empty space
                            #print("* bump *")
                            bump = True
                            return 0, bump
                        result = self.moveVehicle(i, j, i-size, j) # sends the index of the bottom character and the space  
                        
                        return result, bump
                        
        # make sure that the move does not run into a wall or another vehicle
        elif move == 's':
            if self.vehicles[selected_vehicle][0] != 1:
                print("stay in your lane!")
                return 0, bump
            
            for i in range(side_len): # travel through the lines from top left to bottom right 
                for j in range(side_len):
                    if self.lines[i][j] == selected_vehicle:
                        size = self.vehicles[selected_vehicle][1]
                        if self.lines[i+size][j] != space and self.lines[i+size][j] != exit:    # the spot below it is not an empty space
                            #print("* bump *")
                            bump = True
                            return 0, bump
                        result = self.moveVehicle(i, j, i+size, j) # sends the index of the top character and the space
                        
                        return result, bump
                        
        # make sure that the move does not run into a wall or another vehicle
        elif move == 'a':
            if self.vehicles[selected_vehicle][0] != 0:
                print("stay in your lane!")
                return 0, bump
            
            for i in range(side_len): # travel through the lines from top right to bottom left
                for j in range(side_len-1, -1, -1):
                    if self.lines[i][j] == selected_vehicle:
                        size = self.vehicles[selected_vehicle][1]
                        if self.lines[i][j-size] != space and self.lines[i][j-size] != exit:    # the spot to the left is not an empty space
                            #print("* bump *")
                            bump = True
                            return 0, bump
                        result = self.moveVehicle(i, j, i, j-size) # sends the index of the right character and the space
                                               
                        return result, bump
                        
        # make sure that the move does not run into a wall or another vehicle
        else: # move == 'd'
            if self.vehicles[selected_vehicle][0] != 0:
                print("stay in your lane!")
                return 0, bump
            
            for i in range(side_len): # travel through the lines from top left to bottom right
                for j in range(side_len):
                    if self.lines[i][j] == selected_vehicle:
                        size = self.vehicles[selected_vehicle][1]
                        if self.lines[i][j+size] != space and self.lines[i][j+size] != exit:    # the spot to the right is not an empty space
                            #print("* bump *")
                            bump = True
                            return 0, bump
                        result = self.moveVehicle(i, j, i, j+size) # sends the index of the left character and the space

                        return result, bump
                
        
    def bfs(self, board):
            
        current_board = self.lines[:]
        original_board = self.lines[:]
        winning_state = False
        queue = []
        moves = ""
        past_moves = ""
        vehicle_to_make_move = ""
        past_order_of_vehicles = ""
        seen_states = []
        
        queue.append((current_board, moves, vehicle_to_make_move))
        
        while winning_state == False:
            
            #pick first item in queue
            current_state = queue.pop(0)
            boardC = current_state[0][:]
            moves = ""
            
            vehicle_to_make_move = ""
            past_order_of_vehicles = ""
            
            past_moves = ""
            seen_states.append(boardC[:])
            
            for previous_move in current_state[1]:
                moves += previous_move
                past_moves += previous_move
                
            for previous_vehicle in current_state[2]:
                vehicle_to_make_move += previous_vehicle
                past_order_of_vehicles += previous_vehicle            

                #check to see if its a winning state
            if boardC[3][7] == 'R':
                winning_state = True
                makeMove = "Vehicle " + vehicle_to_make_move[0] + " should move " + moves[0]
                return makeMove
                    
            else: #not a winning state, begin bfs 
                
                v =[]
                
                for key in self.vehicles:
                    v.append(key)
                
                shuffle(v)
                
                
                for vehicle in v:
                        
                    global selected_vehicle 
                    selected_vehicle = vehicle
                                        
                    if self.vehicles[vehicle][0] == 0:
                            
                        #possible_movesRLR1 = ["a", "d"]
                        possible_movesRLR2 = ["d", "a"]
                        shuffle(possible_movesRLR2)
                            
                        for move in possible_movesRLR2:
                                    
                            result, bump = board.chooseMove(move)
                            moves += move
                            vehicle_to_make_move += vehicle
                            
                            if self.lines[3][7] == 'R':
                                winning_state = True
                                self.lines = original_board[:]
                                makeMove = "Vehicle " + vehicle_to_make_move[0] + " should move " + moves[0]
                                return makeMove
                        
                            
                            board_after_move = self.lines[:]
                            
                            #if the new state did not result in bumping into the way or we have not seen it before, we will add it to the queue
                            if bump == False  and self.lines[:] not in seen_states:
                                
                                queue.append((board_after_move, moves, vehicle_to_make_move))
                                #print(queue)
                                
                            moves = past_moves
                            vehicle_to_make_move = past_order_of_vehicles
                            self.lines = boardC[:]
                                
                    else:  #self.vehicles[vehicle][0] == 1 
                                            
                        possible_movesRUD2 = ["s", "w"]
                        shuffle(possible_movesRUD2)
                                            
                        #if self.vehicles[vehicle][0] == 1:
                            
                        for move in possible_movesRUD2:
                                
                            result, bump = board.chooseMove(move)
                            moves += move
                            vehicle_to_make_move += vehicle
                            
                            if self.lines[3][7] == 'R':
                                winning_state = True
                                self.lines = original_board[:]
                                makeMove = "Vehicle " + vehicle_to_make_move[0] + " should move " + moves[0]
                                return makeMove   
                            
                            board_after_move = self.lines[:]
                             
                            
                            #if the new state did not result in bumping into the way or we have not seen it before, we will add it to the queue 
                            if bump == False and self.lines[:] not in seen_states:
    
                                queue.append((board_after_move, moves, vehicle_to_make_move))
                                
                            moves = past_moves 
                            vehicle_to_make_move = past_order_of_vehicles
                            self.lines = boardC[:]                           
        
        self.lines = original_board[:]
        makeMove = "Vehicle " + vehicle_to_make_move[0] + " should move " + moves[0]
        return makeMove       
                        
    def moveVehicle(self, i, j, x, y):
        
        # exchange space with end of vehicle if blocking vehicle
        # if you have reached the goal, return success
        if self.lines[x][y] == exit:
            self.lines[i] = self.lines[i][0:j] + space + self.lines[i][j+1:]
            self.lines[x] = self.lines[x][0:y] + red + self.lines[x][y+1:]
            return 2
            
        else:
            self.lines[i] = self.lines[i][0:j] + space + self.lines[i][j+1:]
            self.lines[x] = self.lines[x][0:y] + selected_vehicle + self.lines[x][y+1:]
            return 1
        
        return result
        
def printHello():
    
    print("-"*10 + " RUSH HOUR " + "-"*10, end='\n\n')
    
    print("The Objective: slide the red car R R through the exit ! to freedom!", end='\n\n')
 
    print("To Play: slide the blocking cars and trucks in their lanes")
    print("(up and down, left and right) until the path is clear for")
    print("the red car to escape.", end='\n\n')
    
    print("Enter the letter of the car you wish to move, then move")
    print("it up and down or left and right with the w, a, s, d keys.")
    print("Type \"reset\" to reset the board.")
    print("Type \"help\" tp get what your next move should be.")
    print("Enter \"0\" to quit the game.", end="\n\n")
    
    print("-"*31, end='\n\n')
    
    
def main():
    
    print(" ")
    try:
        filename = input("Enter the name of the puzzle: ")
        infile = open(filename,'r')
    except IOError:
        raise SystemExit("File name does not exist.")
        

    board = Board(infile)
    board.organizeVehicles()
    printHello()
    board.prettyPrint()
    result = -1
    bump = ""
    
    # while the goal has not been reached, get input from the user,
    # make a move, and print the current state.
    while result != 2:
        
        move = input()
        
        if move == "0":
            print("Goodbye!")
            print("-"*31, end='\n\n')
            raise SystemExit()
        
        elif move == "help":
            next_move = board.bfs(board)
            print("Here is your next move: " + next_move)
        
        elif move == "reset":
            board.resetBoard()
            print("The board has been reset.")
        
        else:
            result, bump = board.chooseMove(move)
        
        if bump:
            print("* bump *")
        
        if result != 0:
            board.prettyPrint()
        
    print("Congratulations, you escaped rush hour! Thanks for playing.")
    print("-"*31, end='\n\n')
    
main()