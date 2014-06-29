#! /usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random

def main():

    pygame.init()
    window = pygame.display.set_mode((400, 400))
    font = pygame.font.Font(None,90)

    jeu = 1

    fond = pygame.image.load("background.jpg").convert()

    #On initialise le plateau de jeu 4x4
    board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
    board = addTile(board)
    board = addTile(board)


    while jeu:

        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus

            if event.type == QUIT:   

                jeu = 0

            if event.type == KEYDOWN:

                if event.key == K_DOWN:

                    board = move(board,'down')

                elif event.key == K_UP:

                    board = move(board,'up')

                elif event.key == K_RIGHT:

                    board = move(board,'right')

                elif event.key == K_LEFT:

                    board = move(board,'left')

                if defeat(board) == 1:

                    jeu = 0

                else:

                    board = addTile(board)


        window.blit(fond, (0,0))

        for i,line in enumerate(board):

            for j,val in enumerate(line):

                if val != None:

                    window.blit(font.render(str(val), 1, (255,0,0)), (j*100,i*100))

        pygame.display.flip()

def move(board,direction): #Fonction principale pour faire bouger les pieces.

    if direction == 'left':
        
        for i,line in enumerate(board):

            fusion(line)

    elif direction == 'right':

        for i,line in enumerate(board):

            line.reverse()

            fusion(line)

            line.reverse()

    elif direction == 'up':

        board = transpose(move(transpose(board),'left'))

    elif direction == 'down':

        board = transpose(move(transpose(board),'right'))

    else:

        print('error')

    return board

def fusion(line): #Fonction qui permet de fusionner les pieces.

    fusion = 0 #Permet de ne pas tout fusionner d'un coup.

    for j,tile in enumerate(line):

        for n in range(j):

            if tile == None:

                pass

            else: 

                if  line[j-n-1] == None:

                    line[j-n-1] = line[j-n]
                    line[j-n] = None

                if line[j-n-1] != None:

                    if line[j-n-1] == line[j-n] and fusion == 0:

                        line[j-n-1] = 2*line[j-n]
                        line[j-n] = None
                        fusion = 1

                    else: # board[i][j-1] != tile

                        pass

def transpose(board): #Transpose la matrice "board" pour simplifier les mouvements.

    lineR = []
    rotated = []

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            lineR.append(line.pop(0))

        rotated.append(lineR)
        lineR = []

    return rotated

def addTile(board): #Ajoute une pieces de façon random.

    i = int(random.random()*4)
    j = int(random.random()*4)

    while board[i][j] != None:

         i = int(random.random()*4)
         j = int(random.random()*4)

    a = random.random()

    if a < 0.8:

    	board[i][j] = 2

    else:

    	board[i][j] = 4

    return board

def defeat(board): #Fonction qui parametre la defaite.

    compteur = 0

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            if board[i][j] != None: # j'ai pas vraiment compris à partir de là ce que tu fais.

                compteur += 1
                #compteur += compteur #Plutôt "compteur += 1" non ? Tu double sa valeur en partant de 0.

    if compteur == (len(board[0]) * len(board)):

        return 1

    else:
    	
        return 0

if __name__ == "__main__":
    main()