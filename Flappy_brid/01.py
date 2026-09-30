import pygame
import random 
import sys

pygame.init() 
WIDTH,HEIGH = 400,500
screen = pygame.display.set_mode((WIDTH,HEIGH)) #ขนานหน้าจอ
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock() #เฟรมเรท

font_score = pygame.font.SysFont("sarabun TH",20)
font_gamrover = pygame.font.SysFont("sarabun TH",20)
sys_font = pygame.font.SysFont("arial",20)

#ตั้งค่าFPS
Fps = 60

#โหลดพื้นหลัง
bg = pygame.image.load("Flappy_brid/bg.png.jpg")
bg = pygame.transform.scale(bg,(400,500))

start_time = pygame.time.get_ticks()

#สี
blue = (135,206,235)
red = (255,0,0)
yello = (255,215,0)
brown = (165,42,42)
White = (255, 255, 255)

screen.fill(blue) #สีหน้าจอ
massage_taxt1 = font_score.render("SCORE :",True,red)
massage_taxt2 = font_gamrover.render("GAME OVER",True,red)


class Bird:
    def __init__(self, x, y):
        # โหลดภาพและปรับขนาดนก
        self.image = pygame.image.load("Flappy_brid/brid.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # ค่าความเร็วและแรงโน้มถ่วง
        self.speed = 0
        self.gravity = 0.3
        self.jump_force = -6

    def update(self):
        self.speed += self.gravity
        self.rect.y += self.speed

        if self.rect.y > 433:
            self.rect.y = 433
            self.speed = 0

    def jump(self):
        if self.rect.top > 0:
            self.speed = self.jump_force

    def draw(self, surface):
        # วาดตัวนกบนหน้าจอ
        surface.blit(self.image, self.rect)

class Pipe :
    def __init__(self,x_pos):
        self.x = float(x_pos)
        self.width = 60
        self.gab = 150
        self.speed = 3
        self.top_heigth = random.randint(100,HEIGH - self.gab - 100)
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        #วางถ่อบน
        pygame.draw.rect(surface, brown, (int(self.x), 0, self.width, self.top_heigth))
        #วางถ่อล้าง
        pygame.draw.rect(surface, brown, (int(self.x), self.top_heigth + self.gab, self.width, HEIGH - (self.top_heigth + self.gab)))
    
    def get_rects(self):
         # ส่งค่า Hitbox ของทั้งท่อบนและท่อล่างกลับไป
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.top_heigth)
        bottom_rect = pygame.Rect(int(self.x), self.top_heigth + self.gab, self.width, HEIGH - (self.top_heigth + self.gab))
        return top_rect, bottom_rect

my_bird = Bird(150, 250)
pipes = []
spawn_pipe_time = 0

running =True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_bird.jump()  # เรียกใช้ฟังก์ชันกระโดด

    screen.blit(bg,(0,0))

    spawn_pipe_time += 1
    if spawn_pipe_time > 100:
        pipes.append(Pipe(WIDTH))
        spawn_pipe_time = 0
        
    # อัปเดตและวาดท่อทั้งหมด
    for pipe in pipes[:]:
        pipe.update()
        pipe.draw(screen)

        # ลบท่อที่หลุดหน้าจอไปแล้วเพื่อประหยัดความจำ
        if pipe.x < -pipe.width:
            pipes.remove(pipe)

        # อัปเดตการเคลื่อนไหวของนก
    my_bird.update()
    my_bird.draw(screen) 

    current_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = sys_font.render(f"Time : {current_time}", True, White)
    screen.blit(timer_text,(20,20))

    pygame.display.update()
    clock.tick(Fps)
pygame.quit()
sys.exit()