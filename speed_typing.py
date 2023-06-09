import pygame
from pygame.locals import *
import sys
import time
import random

# 750 x 500    


class Game:
   
    def __init__(self):
        self.__width=750
        self.__height=500
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.precision = '0%'
        self.results = 'Time:0 Precision:0 % Wpm:0 '   
            #Time: include how long you have texted? 
            #Precision: how accuracy you are? 
            #WPM: word per minuted
        self.word_per_min = 0
        self.end = False
        #colors of header, text, result
        self.header_color = (255,213,102)
        self.text_color  = (240,240,240)
        self.result_color = (255,70,70)
            
        
       
        pygame.init()
        self.open_img = pygame.image.load('duo_speedtyping_open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.__width,self.__height))


        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (750,500)) #resize the background.jpg to width = 750, height = 500 

        self.screen = pygame.display.set_mode((self.__width,self.__height))
        pygame.display.set_caption('Multiplayer Speedtyping Game')
        
    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.__width/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()    #update the changes 
        

    def take_sentence(self):
        f = open('sentences.txt').read() #read the document 
        sentences = f.split('\n')  #identify sentences
        sentence = random.choice(sentences) #choose sentences randomly 
        return sentence
    

    def display_results (self, screen):
        if(not self.end):
            #Calculate time
            self.total_time = time.time() - self.time_start
               
            #Calculate precision
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.precision = count/len(self.word)*100
           
            #Calculate words per minute
            self.word_per_min = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)
                
            self.results = 'Time:'+str(round(self.total_time)) +" secs   Precision:"+ str(round(self.precision)) + "%" + '   Wpm: ' + str(round(self.word_per_min))

            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (100,100))

            #screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.__width/2-75,self.__height-140))
            self.draw_text(screen,"Reset", self.__height - 70, 26, (100,100,100))
            
            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
    
       
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (50,250,650,50))
            pygame.draw.rect(self.screen,self.header_color, (50,250,650,50), 2)

            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    # position of input box
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                        
                     # position of reset box
                    if(x>=310 and x<=510 and y>=390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
         
                        
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.display_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,350, 28, self.result_color) 
                            self.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
             
                
        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update() 
        time.sleep(1)  #pause the program for 1 second 
        
        self.reset = False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.word_per_min = 0

        # Get random sentence 
        self.word = self.take_sentence()
        if (not self.word): self.reset_game()

        #drawing heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg,80, 80,self.header_color)  
        # draw the rectangle for input box
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word,200, 28,self.text_color )
        
        pygame.display.update()


Game().run()

