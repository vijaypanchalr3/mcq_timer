import pygame as pg
import time
import sys
import os



class timer:
    def __init__(self,bg,fg,size):
        self.initial_time = int(time.time())
        self.bg = bg
        self.fg = fg
        self.red = "#ff0d0d"
        self.credit_main = 60
        self.credit_cut = 0.001
        self.credit = self.credit_main
        self.size = size
        self.time = 60
    def elapse(self):
        self.initial_time = int(time.time())
        
    def show(self,ff,window,paused):
        clock_color = self.fg
        if paused==True:
            exact=0
            self.initial_time = int(time.time())
        else:
            exact = int(time.time())-self.initial_time
        if exact > self.time:
            self.credit -= self.credit_cut
            clock_color = self.red
            
        minute = exact//60
        second =exact%60
        text_time = ff.render(str(minute)+" : "+str(second),True,clock_color,self.bg)
        text_time_size = text_time.get_size()
        text_time_rect = pg.draw.rect(window,self.bg,(self.size[0]//2,self.size[1]//2-75,text_time_size[0]+50,text_time_size[1]+20))
        
        # text_time_rect.center = (self.size[0]//2,self.size[1]//2)
        window.blit(text_time, text_time_rect)
        text_credit = ff.render(str(format(self.credit,".2f")),True,self.fg,self.bg)
        text_credit_size = text_credit.get_size()
        text_credit_rect = pg.draw.rect(window,self.bg,(self.size[0]//2-20,self.size[1]//2+50,text_credit_size[0]+50,text_credit_size[1]+20))
        # text_credit_rect.center = (self.size[0]//2,self.size[1]//2+100)
        window.blit(text_credit,text_credit_rect)
    def reset(self):
        self.credit = self.credit_main
        self.initial_time = int(time.time())
    def manual_time(self,time=60):
        if time==0:
            time = self.time
        self.time = time

    def manual_credit(self,credit=60):
        if credit==0:
            credit = self.credit_main
        self.credit_main = credit
    def manual_credit_cut(self,cut=1000):
        if cut==0:
            cut=self.credit_cut
        self.credit_cut = 1/cut

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class loop:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((1300,720),pg.FULLSCREEN)
        self.bg = "#000000"
        self.fg = "#ffffff"
        self.special = "#34be5b"
        self.ff = pg.font.Font(resource_path("Lato-BoldItalic.ttf"),45)
        self.size = self.window.get_size()
        self.TIMER = timer(self.bg,self.fg,self.size)
    def menu(self):
        run = True
        clock = pg.time.Clock()
        color_active = pg.Color("#03fc5e")
        color_passive = pg.Color(self.special)
        input_rect1 = pg.Rect(self.size[0]//2+100, self.size[1]/2-35, 200, 70)
        input_rect2 = pg.Rect(self.size[0]//2+100, self.size[1]/2+100-35, 200, 70)
        input_rect3 = pg.Rect(self.size[0]//2+100, self.size[1]/2+200-35, 200, 70)
        user_text = '0'
        active1 = False
        active2 = False
        active3 = False
        
        
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    break
                
                if event.type == pg.KEYDOWN:
                    
                    if event.key == pg.K_ESCAPE:
                        run = False
                        break

                    if event.key==pg.K_UP:
                        if active1==True:
                            active1=False
                            active2=False
                            active3=True
                            user_text = "0"
                            
                        elif active2==True:
                            active1=True
                            active2=False
                            active3=False
                            user_text = "0"
                        elif active3==True:
                            active1 =False
                            active2=True
                            active3 =False
                        else:
                            active3=True
                    if event.key==pg.K_DOWN:
                        if active1==True:
                            active1=False
                            active2=True
                            active3=False
                            user_text = "0"
                            
                        elif active2==True:
                            active2=False
                            active3=True
                            active1=False
                            user_text = "0"
                        elif active3==True:
                            active3 =False
                            active1 =True
                            active2=False
                        else:
                            active1=True
                    if event.key == pg.K_BACKSPACE:
                        user_text = user_text[:-1]
                        if user_text=="":
                            user_text="0"
                    else:
                        if event.key==pg.K_RETURN or event.key==pg.K_KP_ENTER:
                            run = False
                            break
                            
                        try:
                            int(event.unicode)
                            user_text += event.unicode
                        except:
                            pass
                       
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_rect1.collidepoint(event.pos):
                        active1 = True
                        active2 = False
                        active3 = False
                        user_text = "0"
                    elif input_rect2.collidepoint(event.pos):
                        active1 = False
                        active2 = True
                        active3 = False
                        user_text = "0"
                    elif input_rect3.collidepoint(event.pos):
                        active1 = False
                        active2 = False
                        active3 = True
                        user_text = "0"
                    else:
                        active1 = False
                        active2 = False
                        active3 = False
                        user_text = "0"
            clock.tick(60)
            self.window.fill(self.bg)
            if active1:
                color1 = color_active
                color2 = color_passive
                color3 = color_passive
            elif active2:
                color1 = color_passive
                color2 = color_active
                color3 = color_passive
            elif active3:
                color1 = color_passive
                color2 = color_passive
                color3 = color_active
            else:
                color1 = color_passive
                color2 = color_passive
                color3 = color_passive
                
            
            
            pg.draw.rect(self.window, color1, input_rect1)
            stamp1 = self.ff.render("Time : ", True,self.fg,self.bg)
            stamp1_rect = stamp1.get_rect()
            stamp1_rect.center = (self.size[0]//2-100,self.size[1]//2)
            self.window.blit(stamp1,stamp1_rect)
            
            stamp2 = self.ff.render("Credit : ",True,self.fg,self.bg)
            stamp2_rect = stamp2.get_rect()
            stamp2_rect.center = (self.size[0]//2-100,self.size[1]//2+100)
            self.window.blit(stamp2,stamp2_rect)

            stamp3 = self.ff.render("Credit cut : ",True,self.fg,self.bg)
            stamp3_rect = stamp3.get_rect()
            stamp3_rect.center = (self.size[0]//2-100,self.size[1]//2+200)
            self.window.blit(stamp3,stamp3_rect)
            
            menu_text = self.ff.render("Menu",True,self.bg,self.fg)
            menu_text_size = menu_text.get_size()
            menu_text_rect = pg.draw.rect(self.window,self.fg,(self.size[0]//2-menu_text_size[0]//2-250,100,menu_text_size[0]+500,menu_text_size[1]+20),border_radius=5)
            self.window.blit(menu_text, (menu_text_rect.x+250,menu_text_rect.y+10))
            
           
            pg.draw.rect(self.window, color2, input_rect2)
            pg.draw.rect(self.window, color3, input_rect3)
        
            text_surface = self.ff.render(user_text, True, self.fg)
            if active1:
                self.window.blit(text_surface, (input_rect1.x+5, input_rect1.y+5))
                self.TIMER.manual_time(int(user_text))
                self.TIMER.reset()
            elif active2:
                self.window.blit(text_surface, (input_rect2.x+5, input_rect2.y+5))
                self.TIMER.manual_credit(int(user_text))
                self.TIMER.reset()
            elif active3:
                self.window.blit(text_surface, (input_rect3.x+5, input_rect3.y+5))
                self.TIMER.manual_credit_cut(float(user_text))
                self.TIMER.reset()
            else:
                user_text = '0'
                
            input_rect1.w = max(200, text_surface.get_width()+10)
            input_rect2.w = max(200, text_surface.get_width()+10)
            input_rect3.w = max(200, text_surface.get_width()+10)

            pg.display.flip()
            
        self.play()
        
    def play(self):
        run = True
        clock = pg.time.Clock()
        self.window.fill(self.bg)

        study_time = self.ff.render("MCQ timer",True,self.fg,self.bg)
        study_time_rect = study_time.get_rect()
        study_time_rect.center = (self.size[0]//2+50,100)
        self.window.blit(study_time, study_time_rect)


        menu_text = self.ff.render("Menu",True,self.fg,self.special)
        menu_text_size = menu_text.get_size()
        menu_text_rect = pg.draw.rect(self.window,self.special,(self.size[0]//2-200-menu_text_size[0],self.size[1]-100,menu_text_size[0]+20,menu_text_size[1]+20),border_radius=5)
        self.window.blit(menu_text, (menu_text_rect.x+10,menu_text_rect.y+10))


        reset_text = self.ff.render("Reset",True,self.fg,self.special)
        reset_text_size = reset_text.get_size()
        reset_text_rect = pg.draw.rect(self.window,self.special,(self.size[0]//2+200,self.size[1]-100,reset_text_size[0]+20,reset_text_size[1]+20),border_radius=5)
        self.window.blit(reset_text, (reset_text_rect.x+10,reset_text_rect.y+10))

        paused = False
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    sys.exit()
                    
                if event.type == pg.KEYDOWN:
                    
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_SPACE:
                        self.TIMER.elapse()

                    if event.key == pg.K_m:
                        self.menu()
                    if event.key ==pg.K_r:
                        self.TIMER.reset()
                    if event.key ==pg.K_p:
                        paused = not paused
                if event.type==pg.MOUSEBUTTONDOWN:
                    if menu_text_rect.collidepoint(event.pos):
                        self.menu()
                    if reset_text_rect.collidepoint(event.pos):
                        self.TIMER.reset()
                        
            clock.tick(30)
            

                       
            self.TIMER.show(self.ff,self.window,paused)
            pg.display.flip()
        pg.quit()


if __name__=="__main__":
    Run = loop()
    Run.play()
