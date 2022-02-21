#! /usr/bin/env python3
from pygame import *
from random import randint
init()
class main:
    def __init__(this):
        this.correctbits = [False]*8
        this.number = 0
        this.score = 0
        this.previousnumberwidth = 0
        this.screen = display.set_mode([640,480],FULLSCREEN)
        display.set_caption("Sign and Magnitude")
        clock = time.Clock()
        submittext = Bit.bitfont.render("Submit",True,(0,0,200))
        this.submit_topleft = [320 - submittext.get_width() / 2,200]
        this.submit_bottomright = [this.submit_topleft[0] + submittext.get_width(),this.submit_topleft[0] + submittext.get_height()]
        draw.rect(this.screen,(200,0,0),(*this.submit_topleft,submittext.get_width(),submittext.get_height()))
        this.screen.blit(submittext,this.submit_topleft)
        this.bitgroup = BitGroup(this.screen)
        for i in range(40,640,80):
            this.bitgroup.append(Bit(this.screen,(i,100)))
        this.bitgroup.draw()
        this.screen.blit(Bit.bitfont.render("Score: 0",True,(200,200,200)),(0,0))
        this.newnumber()
        display.flip()
        running = True
        while running:
            if key.get_pressed()[27]: running = False
            for e in event.get():
                if MOUSEBUTTONDOWN == e.type:
                    if this.checksubmit(mouse.get_pos()) or this.bitgroup.toggleat(mouse.get_pos()):
                        display.flip()
                elif QUIT == e.type: running = False
            clock.tick(20)
        quit()
    def newnumber(this):
        previousnumber = this.number
        while True:
            this.number = randint(-127,127)
            if this.number != 0 and this.number != previousnumber: break
        total = abs(this.number)
        this.correctbits[0] = this.number < 0
        for i in range(1,8):
            value = 2 ** (7-i)
            if total - value >= 0:
                this.correctbits[i] = True
                total -= value
            else:
                this.correctbits[i] = False
        text = Bit.bitfont.render(str(this.number),True,(255,255,255))
        draw.rect(this.screen,(0,0,0),(320 - this.previousnumberwidth / 2,0,this.previousnumberwidth,text.get_height()))
        this.screen.blit(text,(320 - text.get_width() / 2,0))
        this.previousnumberwidth = text.get_width()
    def checksubmit(this,pos):
        if this.submit_topleft[0] <= pos[0] <= this.submit_bottomright[0] and this.submit_topleft[1] <= pos[1] <= this.submit_bottomright[1]:
            correct = True
            for i in range(len(this.bitgroup)):
                if this.bitgroup[i].value != this.correctbits[i]:
                    correct = False
                    break
            if correct:
                this.score += 1
                text = Bit.bitfont.render("Score: " + str(this.score),True,(200,200,200))
                draw.rect(this.screen,(0,0,0),(0,0,text.get_width(),text.get_height()))
                this.screen.blit(text,(0,0))
                this.newnumber()
                text = Bit.bitfont.render("Correct",True,(0,0,0))
                draw.rect(this.screen,(0,255,0),(0,300,640,text.get_height()))
            else:
                text = Bit.bitfont.render("Incorrect",True,(255,255,255))
                draw.rect(this.screen,(255,0,0),(0,300,640,text.get_height()))
            this.screen.blit(text,(320 - text.get_width() / 2,300))
            return True
        else:
            return False
class Bit:
    bitfont = font.SysFont("Monospace",40)
    height = 50
    width = 50
    bgcolour = (240,240,240)
    truechar = bitfont.render("1",True,(0,0,0))
    falsechar = bitfont.render("0",True,(0,0,0))
    def __init__(this,screen,centre):
        this.value = False
        this.screen = screen
        this.centre = centre
        this.font = this.falsechar
        this.topleft = [centre[0] - this.width / 2,centre[1] - this.height / 2]
        this.bottomright = [centre[0] + this.width / 2, centre[1] + this.height / 2]
    def draw(this):
        draw.rect(this.screen,this.bgcolour,(*this.topleft,this.width,this.height))
        this.screen.blit(this.font,[this.centre[0] - this.font.get_width() / 2,this.centre[1] - this.font.get_height() / 2])
    def toggle(this):
        this.value = not this.value
        this.font = this.truechar if this.value else this.falsechar
        this.draw()
class BitGroup(list):
    def __init__(this,screen):
        super().__init__()
        this.screen = screen
    def draw(this):
        for bit in this:
            bit.draw()
    def toggleat(this,pos):
        for bit in this:
            if bit.topleft[0] <= pos[0] <= bit.bottomright[0] and bit.topleft[1] <= pos[1] <= bit.bottomright[1]:
                bit.toggle()
                return True
        return False
    def checkanswer(this,correctbits):
        for i in range(len(this)):
            if this[i].value != correctbits[i]:
                return False
        return True
if __name__ == "__main__": main()
