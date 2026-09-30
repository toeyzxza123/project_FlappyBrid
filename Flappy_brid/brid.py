import pygame

pygame.init() 

WIDTH,HEIGH = 400,500

#ขนาดหน้าจอ
screen = pygame.display.set_mode((WIDTH, HEIGH))

sys_font = pygame.font.SysFont("arial",20)

#ตั้งค่าFPS
Fps = 60
clock = pygame.time.Clock()

bg = pygame.image.load("Flappy_brid/bg.png.jpg")
bg = pygame.transform.scale(bg,(400,500))

start_time = pygame.time.get_ticks()

#ฟ้อน
font_score = pygame.font.SysFont("sarabun TH",20)
font_gamrover = pygame.font.SysFont("sarabun TH",20)

#สี
blue = (135,206,235)
red = (255,0,0)
yello = (255,215,0)
White = (255,255,255)

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

        if self.rect.y > 337:
            self.rect.y = 337
            self.speed = 0

    def jump(self):
        if self.rect.top > 0:
            self.speed = self.jump_force

    def draw(self, surface):
        # วาดตัวนกบนหน้าจอ
        surface.blit(self.image, self.rect)

my_bird = Bird(150, 250)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_bird.jump()  # เรียกใช้ฟังก์ชันกระโดด

    # อัปเดตการเคลื่อนไหวของนก
    my_bird.update()

    current_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = sys_font.render(f"Time : {current_time}", True, White)

    screen.blit(bg, (0, 0))
    my_bird.draw(screen)  # วาดนก
    screen.blit(timer_text, (20, 20))
    
    pygame.display.update()
    clock.tick(Fps)

pygame.quit()