import tkinter as tk
from tkinter import * 
from tkinter.ttk import * 

window = tk.Tk()
rows = 8

class Shape:
    def __init__(self, master = None):
        self.master = master
         
        # Calls create method of class Shape
        self.create()
     
    def create(self):
         
        # Creates a object of class canvas
        # with the help of this we can create different shapes
        self.canvas = Canvas(self.master)

        # Creates the background for the game board
        self.canvas.create_rectangle(50, 700, 750, 60,
                                outline = "black", fill = ('#964b00'),
                                width = 2)

        for j in range(rows):
            for i in range(4):

                # Creates the holes for the pegs
                self.canvas.create_oval(75+(i*125), 65+(j*75), 145+(i*125), 135+(j*75),
                                    outline = "black", fill = "white",
                                    width = 2)
                
                if i < 2:
                    # Creates the holes for the pegs
                    self.canvas.create_oval(625+(i*40), 70+(j*75), 650+(i*40), 95+(j*75),
                                        outline = "black", fill = "black",
                                        width = 2)
                if i >=2:
                    # Creates the holes for the pegs
                    self.canvas.create_oval(625+((i-2)*40), 105+(j*75), 650+((i-2)*40), 130+(j*75),
                                        outline = "black", fill = "black",
                                        width = 2)

        # Pack the canvas to the main window and make it expandable
        self.canvas.pack(fill = BOTH, expand = 1, side=TOP)
 
guess = []

def enter_guess():
    guess.append(entry.get())
    entry.delete(0, END)

if __name__ == "__main__":

    COLOURS = ["R = red", "G = green", "B = blue", "P = purple", "Y = yellow", "W = white"]
    color_labels = tk.Label(text="Enter the colour you would like to guess, \n"+ str(COLOURS))
    color_labels.config(font=('Helvetica bold', 12))
    color_labels.pack(side=tk.TOP)

    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    shape = Shape(window)
 
    # Sets the title to Shapes
    window.title("Shapes")
 
    # Sets the geometry and position
    # of window on the screen
    window.geometry("800x800")

         
    entry = tk.Entry(fg="black", bg="white", width=50)
    entry.pack()

    button = tk.Button(
        text="Submit guess",
        width=25,
        height=5,
        bg="white",
        fg="black",
        command=enter_guess
    )
    button.pack()
 
window.mainloop()