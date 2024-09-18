import pygame
from pygame.locals import *
import sys
import time
import random
import Levenshtein

class Game:

    def __init__(self):
        self.w=750
        self.h=500
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255,255,255)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)

        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))

        self.bg = pygame.image.load('background.png')
        self.bg = pygame.transform.scale(self.bg, (750,500))

        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Speed test')
    
    
    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence
    
    def levenshtein_accuracy(self):
        return 100 - Levenshtein.distance(self.word, self.input_text)/len(self.word)*100
    
    def show_results(self, screen):
        if(not self.end):
            #Time calculation
            self.total_time = time.time() - self.time_start

            self.accuracy = self.levenshtein_accuracy()

            #WPM calculation
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time:'+str(round(self.total_time)) +" secs Accuracy:"+ str(round(self.accuracy)) + "%" + ' Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150,150))

            screen.blit(self.time_img, (self.w/2-75,self.h-140))
            self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (50,250,650,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)
            # Display user input
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                
                # Click
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # Click on input bar
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    # Click on reset button
                    if(x>=310 and x<=510 and y>=390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
                
                # Key entered
                elif event.type == pygame.KEYDOWN:
                    if not self.end:
                        if not self.active :
                            self.active = True
                            self.time_start = time.time()
                            self.input_text = ''
                            self.input_text += event.unicode
                        else :
                            if event.key == pygame.K_RETURN:
                                print(self.input_text)
                                self.show_results(self.screen)
                                print(self.results)
                                self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)
                                self.end = True
                                self.active = False
                            elif event.key == pygame.K_BACKSPACE:
                                self.input_text = self.input_text[:-1]
                            else:
                                try:
                                    self.input_text += event.unicode
                                except:
                                    pass 
                    elif self.end and not self.active: 
                        if event.key == pygame.K_RETURN:
                            self.reset_game()

            pygame.display.update()
        clock.tick(60)


    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

        self.reset=False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Randomly take a sentence
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
 
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg,80, 80,self.HEAD_C)
        # Input box
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)

        # Show the sentence
        self.draw_text(self.screen, self.word,200, 28,self.TEXT_C)

        pygame.display.update()
    
    
    
Game().run()