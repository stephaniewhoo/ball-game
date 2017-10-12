#!/usr/bin/env python3
# encoding: utf-8

from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        """
        initialize Ball
        :param canvas: Canvas
        :param paddle: Paddle
        :param color: string
        """
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.fraction = 0
        self.canvas_id = self.canvas.create_text(10, 10, anchor="nw")
        text = "Point: 0"
        self.canvas.itemconfig(self.canvas_id, fill="blue", text=text)

    def hit_paddle(self, pos):
        """
        :param pos: list
        :return: bool
        """
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.fraction += 1
                self.canvas.delete(self.canvas_id)
                self.canvas_id = self.canvas.create_text(10, 10, anchor="nw")
                self.canvas.itemconfig(self.canvas_id, fill="blue", text="Point: ")
                self.canvas.insert(self.canvas_id, 12, self.fraction)
                return True
        return False

    def draw(self):
        """

        :return:
        """
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            self.canvas.create_text(100, 300, text=("Game over! Point: %d") % self.fraction, fill="red")
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

class Paddle:
    def __init__(self, canvas, color):
        """
        :param canvas:
        :param color:
        """
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all(sequence='<KeyPress-Left>', func=self.turn_left)
        self.canvas.bind_all(sequence='<KeyPress-Right>', func=self.turn_right)

    def turn_left(self, event):
        """
        :return:
        """
        self.x = -2

    def turn_right(self, event):
        """
        :return:
        """
        self.x = 2

    def draw(self):
        """

        :return:
        """
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

class Lock:
    lock = False

    def __init__(self):
        self.lock = False

    @classmethod
    def getLock(self):
        return self.lock

    @classmethod
    def setLock(self, lock):
        self.lock = lock
        return self

if "__main__" == __name__:
    tk = Tk()
    tk.title("Python Game")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)

    tk.update()
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()

    def start_begin(event):
        if Lock.getLock() == True:
            return
        Lock.setLock(True)
        paddle = Paddle(canvas=canvas, color="blue")
        ball = Ball(canvas=canvas, paddle=paddle, color='red')
        time.sleep(1)
        while True:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.001)

    canvas.bind_all(sequence="<Button-1>", func=start_begin)

    tk.mainloop()
