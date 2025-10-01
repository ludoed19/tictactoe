from tkinter import *
import random

size_btn = 150
window = Tk()

list_btn = []
btn_click = []
btn_comp = []

window.geometry(f"{size_btn*3}x{size_btn*3+100}")
window.title("TicTacToe")

class Btn():
    global size_btn,list_btn,btn_click,btn_comp

    def __init__(self,x0,y0,index_btn):
        self.index_btn = index_btn
        self.x0 = x0
        self.y0 = y0
        self.btn = Button(font=('Arial 100 bold'))
        self.btn.place(x=x0, y=y0, width=size_btn, height=size_btn)
        self.start_btn = Button(text = 'Start', height = 3, width = 9,command=self.click_start, bg = 'gray')
        self.start_btn.place(rely=0.9,relx=0.6)
        self.lbl = Label(text = 'Для начала игры нажмите Start', height = 2, width = 30)
        self.lbl.place(relx=0.05, rely=0.91)
        self.wins = [[0,1,2],[3,4,5],[6,7,8],[1,4,7],[0,3,6],[2,5,8],[0,4,8],[2,4,6]]

    def unbind1(self,event):
        self.btn.unbind('<Button-1>')
    def bind1(self,event):
        self.btn.bind('<Button-1>',self.click)

    def cfg_green(self):
        self.btn.config(bg='green')
    def cfg_white(self):
        self.btn.config(bg='white')

    def check_best_turn(self):
        def evaluate(board):
            score = 0
            for combo in self.wins:
                o_count = sum(1 for c in combo if c in board["O"])
                x_count = sum(1 for c in combo if c in board["X"])
                if o_count > 0 and x_count == 0:
                    score += 10 ** o_count
                elif x_count > 0 and o_count == 0:
                    score -= 10 ** x_count
            return score

        def minimax(board, depth, alpha, beta, is_maximizing):
            for combo in self.wins:
                if all(c in board["O"] for c in combo):
                    return 1000 - depth
                if all(c in board["X"] for c in combo):
                    return -1000 + depth
            if len(board["O"]) + len(board["X"]) == 9:
                return 0

            if depth >= 6:
                return evaluate(board)

            if is_maximizing:
                max_eval = -9999
                for i in range(9):
                    if i not in board["O"] and i not in board["X"]:
                        board["O"].append(i)
                        eval_score = minimax(board, depth+1, alpha, beta, False)
                        board["O"].remove(i)
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
                return max_eval
            else:
                min_eval = 9999
                for i in range(9):
                    if i not in board["O"] and i not in board["X"]:
                        board["X"].append(i)
                        eval_score = minimax(board, depth+1, alpha, beta, True)
                        board["X"].remove(i)
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
                return min_eval

        best_score = -9999
        move = None
        board = {"O": btn_comp.copy(), "X": btn_click.copy()}

        for i in range(9):
            if i not in board["O"] and i not in board["X"]:
                board["O"].append(i)
                score = minimax(board, 0, -9999, 9999, False)
                board["O"].remove(i)
                if score > best_score:
                    best_score = score
                    move = i

        return move

    def win_check(self,lst1):
        self.win = False
        btn_choice = sorted(lst1)
        k = 0
        for i in range(8):
            for j in range(3):
                if self.wins[i][j] in btn_choice:
                    k+=1
            if k == 3:
                self.win = True
                break
            else:
                k=0
        if self.win:
            for q in list_btn:
                q.unbind1('<Button-1>')
            for w in range(3):
                list_btn[self.wins[i][w]].cfg_green()

    def cfg_o(self,str1):
        self.btn.config(text=str1)

    def game(self):
        if len(btn_comp) == 0 and len(btn_click) == 0:
            x = random.randint(0,8)
        else:
            x = self.check_best_turn()

        if x is None:
            return

        btn_comp.append(x)
        list_btn[x].cfg_o('O')
        list_btn[x].unbind1('<Button-1>')

        self.win_check(btn_comp)

    def click_start(self):
        global btn_click, btn_comp
        btn_click = []
        btn_comp = []
        for b in list_btn:
            b.btn.config(text='')
            b.bind1('<Button-1>')
            b.cfg_white()

    def click(self,event):
        self.btn.config(text='X')
        btn_click.append(self.index_btn)
        self.win_check(btn_comp)
        self.win_check(btn_click)
        self.btn.unbind('<Button-1>')
        self.game()

def draw():
    index = 0
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            list_btn.append(Btn(x,y,index))
            index+=1
            x+=size_btn
        x=0
        y+=size_btn

window.resizable(width=False, height=False)
draw()
window.mainloop()