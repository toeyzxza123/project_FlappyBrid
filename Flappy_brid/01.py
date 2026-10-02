import pygame
import random 
import sys

pygame.init() 
WIDTH,HEIGH = 400,500
screen = pygame.display.set_mode((WIDTH,HEIGH)) #ขนานหน้าจอ
pygame.display.set_caption("Flappy Bird")

font_gamrover = pygame.font.SysFont("sarabun TH",20)
sys_font = pygame.font.SysFont("arial",20)

#ตั้งค่าFPS
Fps = 60
clock = pygame.time.Clock() #เฟรมเรท

#โหลดพื้นหลัง
bg = pygame.image.load("Flappy_brid/bg.jpg")
bg = pygame.transform.scale(bg,(400,500))

start_time = pygame.time.get_ticks()

#สี
RGB = (156,39,176)
red = (255,0,0)
yello = (255,215,0)
brown = (165,42,42)
White = (255, 255, 255)
Green = (0,255,0)

class Bird:
    def __init__(self, x, y):
        # โหลดภาพและปรับขนาดนก
        self.image = pygame.image.load("Flappy_brid/bird.png.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # ค่าความเร็วและแรงโน้มถ่วง
        self.speed = 0
        self.gravity = 0.3
        self.jump_force = -4

    def update(self):
        self.speed += self.gravity
        self.rect.y += self.speed

        if self.rect.y > 430:
            self.rect.y = 430 
            self.speed = 0

    def jump(self):
        if self.rect.top > 0:
            self.speed = self.jump_force
            
    def draw(self, surface):
        # วาดตัวนกบนหน้าจอ
        surface.blit(self.image, self.rect)
        # วาดกรอบรอบนก
        #pygame.draw.rect(surface, Green, self.rect, 2)
    
class Pipe :
    def __init__(self,x_pos,lavel):
        self.x = float(x_pos)
        self.width = 60
        self.gab = 175
        
        #ความเร็วเพิ่มขึ้นตาม 
        self.speed = 3 + max(0,lavel - 1) * 0.5
        self.top_heigth = random.randint(100,HEIGH - self.gab - 100)
        
        #เก็บตำแหน่งเริ่มต้นไว้
        self.start_y = self.top_heigth
        
        #ระยะที่ท่อสามารถเลื่อนขึ้น-ลง
        self.move_distance = 10
        
        #ความเร้วขึ้น-ลง
        self.vertical_speed = 0.5
        
        #ท่อจะเลื่อนตั้งแต่ level 3
        self.moving = level >= 3
        
        #ทิดทางการเลื่อน
        self.direction = 1
        self.passed = False

    def update(self):
        #ท่อเลื่อนไปทางซ้าย
        self.x -= self.speed

        #ถ้า lavel 3 ขึ้นไป ให้ท่อเลื่อนขึ้น-เลื่อนลง
        if self.moving:
            self.top_heigth += self.vertical_speed * self.direction

            #ถ้าเลื่อนลงครบ 30 pixels
            if self.top_heigth >= self.start_y + self.move_distance:
                self.direction = -1

            # ถ้าเลื่อนขึ้นครบ 30 pixels
            if self.top_heigth <= self.start_y - self.move_distance:
                self.direction = 1
            

    def draw(self, surface):
        #วางถ่อบน
        pygame.draw.rect(surface, brown, (int(self.x), 0, self.width, self.top_heigth))
        #วางถ่อล้าง
        pygame.draw.rect(surface, brown, (int(self.x), self.top_heigth + self.gab, self.width, HEIGH - (self.top_heigth + self.gab)))
         # สร้างขอบเขตท่อ
        top_rect, bottom_rect = self.get_rects()

        # วาดกรอบขอบเขตท่อบน
        #pygame.draw.rect(surface, Green, top_rect, 2)

        # วาดกรอบขอบเขตท่อล่าง
        #pygame.draw.rect(surface, Green, bottom_rect, 2)

    def get_rects(self):
         # ส่งค่า Hitbox ของทั้งท่อบนและท่อล่างกลับไป
        top_rect = pygame.Rect(int(self.x), 0, self.width, self.top_heigth)
        bottom_rect = pygame.Rect(int(self.x), self.top_heigth + self.gab, self.width, HEIGH - (self.top_heigth + self.gab))
        return top_rect, bottom_rect

#ฟังก์ชันการชน
def check_collision(bird, pipes):
    # ตรวจสอบท่อทุกอัน
    for pipe in pipes:

        # รับกรอบของท่อบนและท่อล่าง
        top_rect, bottom_rect = pipe.get_rects()

        # ตรวจสอบกรอบนกชนกับท่อหรือไม่
        if bird.rect.colliderect(top_rect) or bird.rect.colliderect(bottom_rect):
            return True
        
    # ถ้าไม่ชน
    return False

my_bird = Bird(150, 250)
pipes = []
spawn_pipe_time = 0

game_started = False
running =True
game_over = False
# เก็บเวลาสุดท้ายตอนเกมจบ
final_time = 0
# สถิติเวลาที่เล่นได้นานที่สุด
best_time = 0
#ระดับเริ่มต้น
level = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

            # ถ้ายังไม่เริ่มเกม
                if not game_started:
                    game_started = True

                    # เริ่มจับเวลาเมื่อกดเริ่ม
                    start_time = pygame.time.get_ticks()

                # ถ้าเริ่มเกมแล้ว และยังไม่ Game Over
                elif not game_over:
                    my_bird.jump()
            if event.key == pygame.K_r:

                # ถ้า Game Over อยู่
                if game_over:

                    # เริ่มเกมใหม่
                    game_started = True
                    game_over = False

                    # รีเซ็ตนกกลับตำแหน่งเริ่มต้น
                    my_bird = Bird(150, 250)

                    # ล้างท่อเก่าทั้งหมด
                    pipes.clear()

                    # รีเซ็ตเวลาเกิดท่อ
                    spawn_pipe_time = 0

                    # เริ่มจับเวลาใหม่
                    start_time = pygame.time.get_ticks()

                    # รีเซ็ตเวลาสุดท้าย
                    final_time = 0
    screen.blit(bg,(0,0))

    if game_started and not game_over:        
        spawn_pipe_time += 1
        current_time = (pygame.time.get_ticks() - start_time) // 1000
        level = current_time // 5 

        if spawn_pipe_time > 100:
            pipes.append(Pipe(WIDTH,level))
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

        # ตรวจสอบว่านกชนกับท่อหรือไม่
        if check_collision(my_bird, pipes):
            # เปลี่ยนสถานะเป็น Game Over
            game_over = True

            # เก็บเวลาสุดท้าย
            final_time = (pygame.time.get_ticks() - start_time) // 1000
            
            # ถ้าเวลารอบนี้มากกว่าสถิติเดิม
            if final_time > best_time:
                best_time = final_time         

        #ตรวจสอบว่านกชนพื้นมั้ย
        if my_bird.rect.bottom >= HEIGH:
            # เปลี่ยนสถานะเป็น Game Over
            game_over = True

            # เก็บเวลาสุดท้าย
            final_time = (pygame.time.get_ticks() - start_time) // 1000
            # อัปเดตสถิติ
            if final_time > best_time:
                best_time = final_time

    #แสดงข้องความก่อนเริ่ม strt
    if not game_started:
        start_text = sys_font.render("PRESS SPACE TO START",True,White)

        screen.blit(start_text,(WIDTH // 2 - start_text.get_width() // 2,HEIGH // 2))
    
    
    # แสดงข้อความ GAME OVER
    if game_over:
        massage_taxt1 = font_gamrover.render("GAME OVER",True,red)

        # สร้างข้อความให้กด R
        restart_text = sys_font.render("PRESS R TO RESTART",True,White)

        # แสดง GAME OVER ตรงกลางหน้าจอ
        screen.blit(massage_taxt1,(WIDTH // 2 - massage_taxt1.get_width() // 2,HEIGH // 2 - 50))

        # แสดง PRESS R TO RESTART
        screen.blit(restart_text,(WIDTH // 2 - restart_text.get_width() // 2,HEIGH // 2))

        # แสดงเวลาสุดท้าย
        timer_text = sys_font.render(f"Time : {final_time}",True,White)
        screen.blit(timer_text,(20, 20))

        # แสดงสถิติสูงสุด
        best_text = sys_font.render(f"Best : {best_time}",True,yello)
        screen.blit(best_text,(WIDTH // 2 - best_text.get_width() // 2,HEIGH // 2 + 40))   

    # ถ้ายังเล่นอยู่
    elif game_started:
        # คำนวณเวลาปัจจุบัน
        current_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = sys_font.render(f"Time : {current_time}",True,White)
        screen.blit(timer_text,(20, 20))
        
        # แสดงสถิติสูงสุด
        best_text = sys_font.render(f"Best Time: {best_time}",True,yello)
        screen.blit(best_text, (20, 45))
        
        # แสดงเลเวล
        socre_level = sys_font.render(f"Level : {level}", True, yello)
        screen.blit(socre_level, (20,70))
    
    pygame.display.update()
    clock.tick(Fps)
pygame.quit()
sys.exit()