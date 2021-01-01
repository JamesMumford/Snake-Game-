import pygame
import time
import random
import os

pygame.init()
display = pygame.display.set_mode((600,600))
pygame.display.set_caption("Snake [BY JAMES!]")

alphabet = "abcdefghijklmnopqrstuvwxyz"

dark_blue=(0,25,51)
black=(5,5,5)
red=(255,0,0)
green=(80,200,80)
dark_green=(0,51,25)
yellow_orange=(255,174,66)
crimson=(204,0,34)
white=(255,255,255)

def print_text(x,y,text,text_size):
    font=pygame.font.SysFont(None,text_size)
    message=font.render(str(text),True,white)
    display.blit(message,[x,y])

def draw_borders():
    pygame.draw.rect(display,black,[0,0,15,600])
    pygame.draw.rect(display,black,[0,600,600,-15])
    pygame.draw.rect(display,black,[600,600,-15,-600])

def display_leaderboard(playername,player_score):
    player_score = int(player_score)
    display.fill(dark_blue)
    draw_borders()
    print_text(160,40,"All Time Leaderboard!",40)
    
    pygame.draw.rect(display,black,[155,35,305,3])
    pygame.draw.rect(display,black,[155,35,3,40])
    pygame.draw.rect(display,black,[155,75,305,-4])
    pygame.draw.rect(display,black,[460,75,-4,-38])

    
    with open("/home/pi/.config/lxpanel/LXDE-pi/panels/panel control/Misc Txt Files/Snake Leaderboard.txt","r") as leaderboard_read:
        scores = []
        for line in leaderboard_read:
            details = line.split("~~~~~")
            if len(details) == 2:
                scores.append([details[0],details[1]])
                
    position_count = 0
    player_position = 0
    
    for highscore in scores:
        position_count += 1
        
        if player_score > int(highscore[1]):
            player_position = position_count
            break
        
    if player_position != 0:
        changing_positions = scores[player_position-1:]
        scores = scores[0:player_position-1]
        
        for i in range(1,len(changing_positions)):
            changing_positions[-i] = changing_positions[-(i+1)]
            
        changing_positions[0] = [playername,player_score]
        
        for item in changing_positions:
            scores.append(item)
            
    os.remove("/home/pi/.config/lxpanel/LXDE-pi/panels/panel control/Misc Txt Files/Snake Leaderboard.txt")
    with open("/home/pi/.config/lxpanel/LXDE-pi/panels/panel control/Misc Txt Files/Snake Leaderboard.txt","w") as update:
        
        for item in scores:
            update.write(str(item[0]).title())
            update.write("~~~~~")
            update.write(str(item[1]))
            update.write("\n")
            
    x,y = 50,100
    count = 1
    
    for score in scores:
        
        if count == player_position:
            pygame.draw.rect(display,(20,140,20),[x-5,y-5,18+9*len(str(count)),31])
            
        value = int(score[1])
        
        print_text(x,y,str(count),35)
        print_text(x+50,y,str(score[0]).title(),35)
        print_text(380,y,value,35)
        
        pygame.draw.rect(display,black,[x-5,y-5,18+9*len(str(count)),4])
        pygame.draw.rect(display,black,[x-5,y-5,4,30])
        pygame.draw.rect(display,black,[x-5,y+25,18+9*len(str(count)),4])
        pygame.draw.rect(display,black,[x-13+12*len(str(count))+20,y+27,4,-31])
        
        y += 38
        count += 1

    print_text(102,500,"Enter P to play again, or Ctrl C to quit.",28)
    pygame.display.update()

    
    play_again = False
    while play_again == False:
         for event in pygame.event.get():
             
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_p:
                    play_again = True
             

def gamerun():
        
    while True:
        
        game_over = False
        snake_x,snake_y = 270,270
        block_width = 30
        x_change = 0
        y_change = 0
        start_time = time.time()
        interval = 0.1
        spawned = False
        score = 0
        spawn_x,spawn_y = 0,0
        snake_components = [[snake_x,snake_y]]

        while game_over == False:
            display.fill(green)
            pygame.draw.rect(display,dark_blue,[545,5,50,25])
            print_text(555,7,score,25)
            current_time = time.time()-start_time

            if current_time > interval:
                interval += 0.1
                input_count = 0

                for event in pygame.event.get():
                    
                    if event.type == pygame.KEYDOWN and input_count == 0:
                        
                        if event.key == pygame.K_UP and y_change == 0:
                            y_change = -30
                            x_change = 0
                            input_count += 1
                            
                        elif event.key == pygame.K_DOWN and y_change == 0:
                            y_change = 30
                            x_change = 0
                            input_count += 1

                        elif event.key == pygame.K_LEFT and x_change == 0:
                            x_change = -30
                            y_change = 0
                            input_count += 1

                        elif event.key == pygame.K_RIGHT and x_change == 0:
                            x_change = 30
                            y_change = 0
                            input_count += 1

                if spawned == False:
                    
                    spawn_x = random.randint(0,19)
                    spawn_y = random.randint(0,19)
                    spawn_x *= block_width
                    spawn_y *= block_width
                    spawned = True

                remainder_if_single_1,remainder_if_single_2 = snake_x,snake_y
                snake_x += x_change
                snake_y += y_change
                snake_components_old = snake_components
                snake_components = [[snake_x,snake_y]]
                remainder_if_double_1,remainder_if_double_2 = snake_components[-1][0],snake_components[-1][1]

                if len(snake_components_old[:-1]) > 0:
                    for item in snake_components_old[:-1]:
                        snake_components.append(item)
                    
                
                pygame.draw.rect(display,red,[spawn_x,spawn_y,block_width,block_width])

                chunk_count = 0
                for item in snake_components:
                    
                    if item in snake_components[:chunk_count] or item in snake_components[(chunk_count+1):]:
                        game_over = True

                    chunk_count += 1
                    
                    chunk_colour = yellow_orange

                    if chunk_count % 4 == 0 or (chunk_count + 1) % 4 == 0:
                        chunk_colour = dark_green
                    #if chunk_count % 2 == 0:
                        #chunk_colour = dark_green

                    elif chunk_count == 1:
                        chunk_colour = black

                    pygame.draw.rect(display,chunk_colour,[item[0],item[1],block_width,block_width])

                if snake_y > 570 or snake_y < 0 or snake_x < 0 or snake_x > 570:
                    game_over = True

                if [snake_x,snake_y] == [spawn_x,spawn_y]:
                    score += 1
                    spawned = False

                    if score <= 100:
                        
                        if len(snake_components) == 1:
                            snake_components.append([remainder_if_single_1,remainder_if_single_2])
                            
                        else:
                            snake_components.append([remainder_if_double_1,remainder_if_double_2])

                pygame.display.update()


        pygame.draw.rect(display,crimson,[160,150,280,120])
        print_text(180,160,"GAME OVER!",55)
        print_text(225-10*len(str(score)),210,"SCORE: "+str(score),55)
        pygame.display.update()
        
        time.sleep(2)
        print_text(80,350,"View leaderboard [L], play again [P] or quit [Ctrl C].",28)
        pygame.display.update()

        view_leaderboard = False
        play_again_please = False
        while view_leaderboard == False and play_again_please == False:
            
            for event in pygame.event.get():
                    
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_l:
                            view_leaderboard = True
                            
                        elif event.key == pygame.K_p:
                            play_again_please = True
                            
        if view_leaderboard == True:
            playername = ""
            playername_entered = False
            while playername_entered == False:
                for event in pygame.event.get():
                    
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key > 96 and event.key < 123:
                            counter=event.key-97
                            letter_entered=alphabet[counter]
                            playername=playername+letter_entered
                            
                        elif event.key == pygame.K_BACKSPACE:
                            playername=playername[0:-1]
                            
                        elif event.key == pygame.K_SPACE:
                            playername=playername+" "
                            
                        elif event.key == pygame.K_RETURN and len(playername) > 1:
                            playername_entered=True
                            
                display.fill((dark_blue))
                draw_borders()
                pygame.draw.rect(display,crimson,[130,95,340,100])
                print_text(140,120,"TYPE YOUR NICKNAME AND HIT",30)
                print_text(180,150,"ENTER TO SAVE SCORE!",30)
                print_text(295-(len(playername)*7.2),300,playername.title(),40)
                pygame.display.update()

            player_name = playername
            display_leaderboard(player_name,score)      
gamerun()
