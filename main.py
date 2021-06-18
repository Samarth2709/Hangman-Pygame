import pygame
import math
import random
import time


def text_objects(text, font, color = (0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def conv_deg(deg):
    rad = (deg/180)*math.pi
    return rad

class HangManMain:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (230, 230, 230)
        self.blue = (10, 10, 255)
        self.red = (255, 20, 20)
        self.green = (0, 225, 0)
        self.game_size = (2000, 1000)
        self.display = pygame.display.set_mode(self.game_size, pygame.NOFRAME, pygame.RESIZABLE)
        self.updated_size = pygame.display.get_window_size()
        self.background_pic = pygame.image.load('desert_background.png')
        self.clock = pygame.time.Clock()
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.dist_mouse_center = 0
        self.words_txt = open('words.txt', 'r')
        self.words = []
        self.word = ''
        self.letter_click = ''
        self.start_x = 0
        self.numb_dashes = 0
        self.ind = []
        self.display_word_l = []
        self.last_ind = 0
        self.even = True
        self.incorrect_ans = 0
        self.incorrect_let = []
        self.start_inc_ans = []
        self.end = False
        self.keys = {'a': pygame.K_a, 'b': pygame.K_b, 'c': pygame.K_c, 'd': pygame.K_d, 'e': pygame.K_e,
                     'f': pygame.K_f,
                     'g': pygame.K_g, 'h': pygame.K_h, 'i': pygame.K_i, 'j': pygame.K_j, 'k': pygame.K_k,
                     'l': pygame.K_l,
                     'm': pygame.K_m, 'n': pygame.K_n, 'o': pygame.K_o, 'p': pygame.K_p, 'q': pygame.K_q,
                     'r': pygame.K_r,
                     's': pygame.K_s, 't': pygame.K_t, 'u': pygame.K_u, 'v': pygame.K_v, 'w': pygame.K_w,
                     'x': pygame.K_x,
                     'y': pygame.K_y, 'z': pygame.K_z}
        self.key_pressed = ''

    def set_cap(self, caption='Game'):
        pygame.display.set_caption(caption)

    def fill_back(self, color):
        self.display.fill(color)

    def letter_press(self, event):
        if event.key in list(self.keys.values()):
            self.key_pressed = list(self.keys.keys())[list(self.keys.values()).index(event.key)]
            return self.key_pressed

    def update_size(self):
        self.updated_size = pygame.display.get_window_size()

    def text(self, text, size, x, y, color = (0, 0, 0)):
        self.smallText = pygame.font.Font("freesansbold.ttf", size)
        self.textSurf, self.textRect = text_objects(text, self.smallText, color)
        self.textRect.center = (x, y)
        self.display.blit(self.textSurf, self.textRect)

    def display_buttons(self, display, color, in_color, first_center, radius):
        for i in range(26):
            self.mouse_pos = pygame.mouse.get_pos()

            if 0 <= i < 13:
                pygame.draw.circle(display, color, (((radius * 2 + 5) * i + first_center[0]), first_center[1]), radius,
                                   5)
                pygame.draw.circle(display, in_color, (((radius * 2 + 5) * i + first_center[0]), first_center[1]),
                                   radius - 5)
                self.dist_mouse_center = abs(math.sqrt(
                    (self.mouse_pos[0] - ((radius * 2 + 5) * i + first_center[0])) ** 2 + (
                            self.mouse_pos[1] - first_center[1]) ** 2))

                if self.dist_mouse_center <= radius:  # IF MOUSE IS OVER CIRCLE
                    self.click = pygame.mouse.get_pressed()
                    pygame.draw.circle(display, in_color, (((radius * 2 + 5) * i + first_center[0]), first_center[1]),
                                       radius)
                    if self.click[0]:
                        print(list(self.keys.keys())[i])  # ACTION IF BUTTON IS CLICKED
                self.smallText = pygame.font.Font("freesansbold.ttf", 20)
                self.textSurf, self.textRect = text_objects(list(self.keys.keys())[i].upper(), self.smallText)
                self.textRect.center = (
                    ((radius * 2 + 5) * i + first_center[0]), first_center[1])
                self.display.blit(self.textSurf, self.textRect)

            elif 13 <= i < 26:
                pygame.draw.circle(display, color,
                                   (((radius * 2 + 5) * (i - 13) + first_center[0]), first_center[1] + 5 + radius * 2),
                                   radius, 5)
                pygame.draw.circle(display, in_color,
                                   (((radius * 2 + 5) * (i - 13) + first_center[0]), first_center[1] + 5 + radius * 2),
                                   radius - 5)
                self.dist_mouse_center = abs(math.sqrt(
                    (self.mouse_pos[0] - ((radius * 2 + 5) * (i - 13) + first_center[0])) ** 2 + (
                            self.mouse_pos[1] - (first_center[1] + 5 + radius * 2)) ** 2))

                if self.dist_mouse_center <= radius:  # IF MOUSE IS OVER CIRCLE
                    self.click = pygame.mouse.get_pressed()
                    pygame.draw.circle(display, in_color, (
                        ((radius * 2 + 5) * (i - 13) + first_center[0]), first_center[1] + 5 + radius * 2),
                                       radius)
                    if self.click[0]:
                        print(list(self.keys.keys())[i])  # ACTION IF BUTTON IS CLICKED
                self.smallText = pygame.font.Font("freesansbold.ttf", 20)
                self.textSurf, self.textRect = text_objects(list(self.keys.keys())[i].upper(), self.smallText)
                self.textRect.center = (
                    ((radius * 2 + 5) * (i - 13) + first_center[0]), first_center[1] + 5 + radius * 2)
                self.display.blit(self.textSurf, self.textRect)

    def hangman_struct(self):
        pygame.draw.rect(self.display, self.black, (50, 650, 250, 8))
        pygame.draw.rect(self.display, self.black, (120, 250, 8, 400))
        pygame.draw.rect(self.display, self.black, (125, 250, 125, 8))
        pygame.draw.rect(self.display, self.black, (247.5, 250, 5, 20))

    def resize_back(self):
        back_size = pygame.Surface.get_size(self.background_pic)
        wind_size = pygame.Surface.get_size(self.display)
        if wind_size[0] > back_size[0] and wind_size[0] - back_size[0] > wind_size[1] - back_size[1]:
            # RESIZE BASED ON X
            # WINDOW IS LARGER THAN BACKGROUND -- INCREASE BACK

            self.background_pic = pygame.transform.rotozoom(self.background_pic, 0, wind_size[0] / back_size[0])
        elif wind_size[1] > back_size[1] and wind_size[1] - back_size[1] > wind_size[0] - back_size[0]:
            # RESIZE BASED ON Y
            # WINDOW IS LARGER THAN BACKGROUND -- INCREASE BACK
            print(int(wind_size[1] / back_size[1]))
            self.background_pic = pygame.transform.rotozoom(self.background_pic, 0, wind_size[1] / back_size[1])
        elif wind_size[0] < back_size[0] and back_size[0] - wind_size[0] > back_size[1] - wind_size[1]:
            # RESIZE BASED ON X
            # WINDOW IS SMALLER THAN BACKGROUND -- DECREASE BACK
            print(int(wind_size[0] / back_size[0]))
            self.background_pic = pygame.transform.rotozoom(self.background_pic, 0, wind_size[0] / back_size[0])
        elif wind_size[1] < back_size[1] and back_size[1] - wind_size[1] > back_size[0] - wind_size[0]:
            # RESIZE BASED ON Y
            # WINDOW IS SMALLER THAN BACKGROUND -- DECREASE BACK\
            print(int(wind_size[1] / back_size[1]))
            self.background_pic = pygame.transform.rotozoom(self.background_pic, 0, wind_size[1] / back_size[1])

    def display_background(self):
        back_size = pygame.Surface.get_size(self.background_pic)
        wind_size = pygame.Surface.get_size(self.display)
        self.background_pic.set_alpha(160)
        self.display.blit(self.background_pic, (wind_size[0] - back_size[0], wind_size[1] - back_size[1]))

    def get_words(self):
        self.words = self.words_txt.read()
        if '\n' in self.words:
            self.words = self.words.split('\n')
        for word in self.words:
            if len(word) <= 1:
                self.words.remove(word)

    def init_display_word(self):
        #self.word = "applesp"
        while True:
            self.word = (self.words[random.randint(0, len(self.words))]).lower()
            if len(self.word)>7 or len(self.word)<4:
                continue
            else:
                break



        if len(self.word) == 4:
            self.display_order = [(self.display_head()), (self.display_body()), (self.display_left_arm(), self.display_right_arm()), (self.display_right_leg(), self.display_left_leg())]
        elif len(self.word) == 5:
            self.display_order = [(self.display_head()), (self.display_body()), (self.display_left_arm(), self.display_right_arm()), (self.display_right_leg(), self.display_left_leg()), (self.display_face())]
        elif len(self.word) == 6:
            self.display_order = [(self.display_head()), (self.display_body()), (self.display_left_arm()), (self.display_right_arm()), (self.display_right_leg()), (self.display_left_leg())]
        elif len(self.word) == 7:
            self.display_order = [(self.display_head()), (self.display_body()), (self.display_left_arm()), (self.display_right_arm()), (self.display_right_leg()), (self.display_left_leg()), (self.display_face())]

        for i in range(len(self.word)):
            self.display_word_l.append(False)
        self.numb_dashes = len(self.word)
        # print(self.game_size[0] - ((700 - 10 - (self.numb_dashes / 2) * 50) + 70*11))

    def display_dash(self):
        middle_word = (self.updated_size[0]/2, self.updated_size[1] - 20)
        if self.numb_dashes % 2 == 0:
            even = True
        elif self.numb_dashes % 2 == 1:
            even = False
        if even:
            self.start_x = middle_word[0] - 10 - (self.numb_dashes / 2) * 70
            for i in range(self.numb_dashes):
                pygame.draw.rect(self.display, self.black, (self.start_x + 70 * i, middle_word[1], 50, 5))
        elif not even:
            self.start_x = middle_word[0] - 25 - (self.numb_dashes / 2) * 70
            for i in range(self.numb_dashes):
                pygame.draw.rect(self.display, self.black, (self.start_x + 70 * i, middle_word[1], 50, 5))

    def check_click(self):
        for i in range(26):
            self.mouse_pos = pygame.mouse.get_pos()
            first_center = (self.updated_size[0] / 2 - 390, 50)
            radius = 30
            if 0 <= i < 13:
                self.dist_mouse_center_top = abs(math.sqrt(
                    (self.mouse_pos[0] - ((radius * 2 + 5) * i + first_center[0])) ** 2 + (
                            self.mouse_pos[1] - first_center[1]) ** 2))
                if self.dist_mouse_center_top <= radius:
                    self.click = pygame.mouse.get_pressed()
                    if self.click[0] and self.letter_click != list(self.keys.keys())[i]:
                        # ACTION IF BUTTON IS CLICKED
                        self.take_try = False
                        self.letter_click = list(self.keys.keys())[i]
            elif 13 <= i < 26:
                self.dist_mouse_center_bot = abs(math.sqrt(
                    (self.mouse_pos[0] - ((radius * 2 + 5) * (i - 13) + first_center[0])) ** 2 + (
                            self.mouse_pos[1] - (first_center[1] + 5 + radius * 2)) ** 2))
                if self.dist_mouse_center_bot <= radius:  # IF MOUSE IS OVER CIRCLE
                    self.click = pygame.mouse.get_pressed()
                    if self.click[0] and self.letter_click != list(self.keys.keys())[i]:
                        # ACTION IF BUTTON IS CLICKED
                        self.take_try = False
                        self.letter_click = list(self.keys.keys())[i]

        if self.letter_click in self.word and self.letter_click != '':
            middle_word = (800, 615)
            for i in range(len(self.word)):
                if self.word[i] == self.letter_click:
                    self.display_word_l[i] = True
            self.letter_click = ''
        elif (not self.letter_click in self.word) and self.letter_click != '' and not self.take_try and not(str(self.letter_click + ',') in self.incorrect_let):
            self.incorrect_ans += 1
            self.take_try = True
            self.incorrect_let.append(self.letter_click+ ',')
            self.incorrect_let.sort()

    def display_letter(self):
        if self.numb_dashes % 2 == 0:
            self.even = True
        elif self.numb_dashes % 2 == 1:
            self.even = False
        # text(self, text, size, coor)
        for i in range(len(self.word)):
            if self.display_word_l[i]:
                display_let_xy = (self.start_x + 70 * i, self.updated_size[1]-20)
                self.text(self.word[i].upper(), 40, display_let_xy[0] + 25, display_let_xy[1] - 25)
                # (580.0, 620)
                # (650.0, 620)
                # (930.0, 620)
                # (1000.0, 620)

    def display_left_mistake(self):
        self.text("Tries Left: " + str(int(len(self.word) - self.incorrect_ans)), 25, self.updated_size[0] - 100,
                  self.updated_size[1] - 30)

    def display_incorrect_let(self):
        self.start_inc_ans = [self.updated_size[0]/2 - 100, self.updated_size[1]/2-50]
        self.text("Incorrect Answers:", 25, self.updated_size[0]/2-100, self.updated_size[1]/2-100, self.red)
        for i in range(len(self.incorrect_let)):
            self.text(self.incorrect_let[i], 25, self.start_inc_ans[0] + 25 * i,self.start_inc_ans[1], self.red)

    def display_head(self):
        head_center = (250, 300)
        pygame.draw.circle(self.display, self.black, head_center, 30, 5)

    def display_body(self):
        body_top_left = (246.5,330)
        pygame.draw.rect(self.display, self.black, (body_top_left[0], body_top_left[1], 7, 100))

    def display_left_arm(self):
        left_arm = (246.4, 350)
        for i in range(10):
            pygame.draw.line(self.display, self.black, (left_arm[0], left_arm[1]-(i*0.5)), (left_arm[0] - 50, left_arm[1]-25-(i*0.5)))

    def display_right_arm(self):
        right_arm = (250, 350)
        for i in range(10):
            pygame.draw.line(self.display, self.black, (right_arm[0], right_arm[1]-(i*0.5)), (right_arm[0] + 50, right_arm[1]-25-(i*0.5)))

    def display_left_leg(self):
        left_leg = (246.5, 430)
        for i in range(10):
            pygame.draw.line(self.display, self.black, (left_leg[0]+3.5, left_leg[1] - (i*0.5)), (left_leg[0] - 50, left_leg[1]+ 35 - (i*0.5)))

    def display_right_leg(self):
        right_leg = (246.5, 430)
        for i in range(10):
            pygame.draw.line(self.display, self.black, (right_leg[0]+3.5, right_leg[1]-(i*0.5)), (right_leg[0] + 50, right_leg[1] + 35 - (i*0.5)))

    def display_face(self):
        face = (250, 300)
        pygame.draw.circle(self.display, self.black, (face[0]-10, face[1]-5), 5, 3)
        pygame.draw.circle(self.display, self.white, (face[0]-10, face[1]-5), 2)

        pygame.draw.circle(self.display, self.black, (face[0]+10, face[1]-5), 5, 3)
        pygame.draw.circle(self.display, self.white, (face[0]+10, face[1]-5), 2)
        for i in range(-2, 3):
            pygame.draw.arc(self.display, self.black, (face[0]-20, face[1]+7+(i), 40, 40), conv_deg(45), conv_deg(135), 1)

        # if len(self.incorrect_let) >= 1:
        #     for i in range(len(self.display_order[0])):
        #         self.display_order[0][i]
        # if len(self.incorrect_let) >= 2:
        #     for i in range(len(self.display_order[1])):
        #         self.display_order[1][i]
        # if len(self.incorrect_let) >= 3:
        #     for i in range(len(self.display_order[2])):
        #         self.display_order[2][i]
        # if len(self.incorrect_let) >= 4:
        #     for i in range(len(self.display_order[3])):
        #         self.display_order[3][i]
        # if len(self.incorrect_let) >= 5:
        #     for i in range(len(self.display_order[4])):
        #         self.display_order[4][i]
        # if len(self.incorrect_let) >= 6:
        #     for i in range(len(self.display_order[5])):
        #         self.display_order[5][i]
        # if len(self.incorrect_let) >= 7:
        #     for i in range(len(self.display_order[6])):
        #         self.display_order[6][i]
    def display_ordes(self):
        if len(self.word) == 4:
            if len(self.incorrect_let) >= 1:
                self.display_head()
            if len(self.incorrect_let) >= 2:
                self.display_body()
            if len(self.incorrect_let) >= 3:
                self.display_left_arm()
                self.display_right_arm()
            if len(self.incorrect_let) >= 4:
                self.display_left_leg()
                self.display_right_leg()
        if len(self.word) == 5:
            if len(self.incorrect_let) >= 1:
                self.display_head()
            if len(self.incorrect_let) >= 2:
                self.display_body()
            if len(self.incorrect_let) >= 3:
                self.display_left_arm()
                self.display_right_arm()
            if len(self.incorrect_let) >= 4:
                self.display_left_leg()
                self.display_right_leg()
            if len(self.incorrect_let) >=5:
                self.display_face()
        if len(self.word) == 6:
            if len(self.incorrect_let) >= 1:
                self.display_head()
            if len(self.incorrect_let) >= 2:
                self.display_body()
            if len(self.incorrect_let) >= 3:
                self.display_left_arm()
            if len(self.incorrect_let) >= 4:
                self.display_right_arm()
            if len(self.incorrect_let) >=5:
                self.display_left_leg()
            if len(self.incorrect_let) >=6:
                self.display_right_leg()
        if len(self.word) == 7:
            if len(self.incorrect_let) >= 1:
                self.display_head()
            if len(self.incorrect_let) >= 2:
                self.display_body()
            if len(self.incorrect_let) >= 3:
                self.display_left_arm()

            if len(self.incorrect_let) >= 4:
                self.display_right_arm()
            if len(self.incorrect_let) >=5:
                self.display_left_leg()
            if len(self.incorrect_let) >= 6:
                self.display_right_leg()
            if len(self.incorrect_let) >= 7:
                self.display_face()



pygame.init()

active = HangManMain()
active.set_cap('HangMan')

active.resize_back()
active.get_words()
active.init_display_word()
active.display_dash()

while not active.end:

        # EVENT TYPES ARE ANY MAJOR EVENT (QUIT, ACTIVEEVENT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP,
        # MOUSEBUTTONDOWN, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN, VIDEORESIZE,
        # VIDEOEXPOSE, USEREVENT)


    active.fill_back(active.white)
    active.display_background()
    active.update_size()

    active.display_buttons(active.display, active.green, active.white, (active.updated_size[0] / 2 - 390, 50), 30)
    active.hangman_struct()
    active.display_dash()

    active.check_click()
    active.display_letter()
    active.display_left_mistake()
    active.display_incorrect_let()

    # print(active.display_order)
    # active.display_head()
    # active.display_body()
    # active.display_left_arm()
    # active.display_right_arm()
    # active.display_left_leg()
    # active.display_right_leg()
    # active.display_face()
    active.display_ordes()

    for event in pygame.event.get():  # ANY EVENTS THAT HAPPEN WITHIN WINDOW
        print(event)
        if event.type == pygame.QUIT or len(active.word) - active.incorrect_ans < 1:
            active.end = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active.end = True
            print(active.letter_press(event))

    pygame.display.update()
    active.clock.tick(190)  # REFRESH RATE

    if active.end:
        time.sleep(2)
pygame.quit()
