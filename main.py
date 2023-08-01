import pygame
from random import randint
import time 

start_time=time.time()

class msg:
    def __init__(self) -> None:
        self.frames=-1
    def top_right(self):
        if self.frames>=0 and self.frames<150:
            self.frames+=1
            return True
        elif self.frames==150:
            self.frames=-1
            return True
        return False

msg_display=msg()

pygame.init()
screen=pygame.display.set_mode((1200,800))
bg = pygame.image.load(f"bg1.jpg")

clock=pygame.time.Clock()

curr=0 

def getimage(number):
    Image = pygame.image.load(f"numbers/{number}.png")
    Image.set_colorkey((255,255,255))
    #Image.convert_alpha()
    return Image


#board setup
def board_exe():
    global board, track
    board=[]
    for i in range(0,1200,40):
        temp=[]
        for j in range(0,800,40):
            temp.append(pygame.Rect((i,j),(40,40)))
        board.append(temp)

#board=[pygame.Rect((i,j),(40,40)) for i in range(0,1200,40) for j in range(0,800,40)]
    #track creation
    track=[]
    for _ in range(30):
        track.append([[-1,-1],False])

    #randomization
    for i in range(30):
        while True:
            loc=[randint(0,29),randint(0,19)]
            for j in track:
                if j[0]==loc:
                    break
            else:       
                print(i)
                print(track[i])
                track[i]=[loc,True]
                break

board_exe()

box=pygame.Surface((40,40))

font=pygame.font.SysFont('arial',20)
font2=pygame.font.SysFont('arial',30)

phase="playing"

while True:
    for i in pygame.event.get():
        if i.type==256:
            pygame.quit()
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_SPACE and phase=="end_game":
                phase="playing"
                curr=0
                start_time=time.time()
                board_exe()
    screen.blit(bg, (0,0))
    if phase=="playing":
        mouse_buttons=pygame.mouse.get_pressed()

        #drawing lines
        for i in range(1,30):
            if not track[i][1] and not track[i-1][1]:
                x,y=((track[i][0][0]*40)+20,(track[i][0][1]*40)+20),((track[i-1][0][0]*40)+20,(track[i-1][0][1]*40)+20)
                pygame.draw.line(screen, (0,0,0), x,y, width=5)
            else: 
                break
        
        #box coloring and blitting
        for j,i in enumerate(track):
            #i.topleft=(randint(0,1160),randint(0,760))
            if track[j][1]:
                box.fill((255,255,255))
            else:
                box.fill((255,255,0))
            img = getimage(j+1)
            #txt=font.render(f"{j+1}",True,(0,0,0))
            #box.blit(img,(0,0))
            screen.blit(img,board[i[0][0]][i[0][1]])

        
        mouse=pygame.mouse.get_pos()
        i=mouse[0]//40
        j=mouse[1]//40
        #print(i,j)

        if mouse_buttons[0]:
            for l,k in enumerate(track):
                if k[0]==[i,j]:
                    if curr==l:
                        print(curr,l)
                        k[1]=False
                        curr+=1
                    elif curr>l:
                        pass
                    else:
                        print(curr,l)
                        msg_display.frames=0
        #print(msg_display.frames)
        if msg_display.top_right():
            #print(f)
            txt=font2.render("Have to go through in ascending order!!",True,(200,10,10))
            screen.blit(txt,(600,0))
        if curr==30:
            phase="end_game"
            t=time.time()-start_time
    if phase=="end_game":
        txt=font2.render(f"Time taken to complete: {t}",True,(200,10,10))
        screen.blit(txt,(400,380))
        txt=font2.render(f"Press SPACE BAR to try again!",True,(0,0,0))
        screen.blit(txt,(400,420))
        


    
    clock.tick(45)
    pygame.display.update()