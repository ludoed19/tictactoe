from tkinter import *
from tkinter import messagebox

size_btn = 150
window = Tk()
window.geometry(f"{size_btn*3}x{size_btn*3+100}")
window.title("TicTacToe")
window.config(bg="#d0eaff")

list_btn, btn_click, btn_comp = [], [], []
game_active = False

class Btn:
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def __init__(self, x0, y0, index):
        self.index = index
        self.btn = Button(font=('Arial', 100, 'bold'), bg='white', state=DISABLED)
        self.btn.place(x=x0, y=y0, width=size_btn, height=size_btn)
        self.btn.bind('<Button-1>', self.click)

        if index == 0:
            Button(
                text='Start', height=3, width=9, bg="#d5f5e3",
                font=('Arial', 13, 'bold'), activebackground='#add8e6',
                command=self.start
            ).place(rely=0.86, relx=0.7)
            Label(
                text='Для начала игры нажмите Start', bg="#d0eaff",
                font=('Arial', 13, 'bold'), height=2, width=30
            ).place(relx=0.01, rely=0.89)

    def start(self):
        global game_active
        game_active = True
        btn_click.clear(); btn_comp.clear()
        for b in list_btn: b.btn.config(text='', bg='white', state=NORMAL)

    def evaluate(self, board):
        s = 0
        for c in self.wins:
            o = sum(i in board['O'] for i in c); x = sum(i in board['X'] for i in c)
            if o and not x: s += 10 ** o
            elif x and not o: s -= 10 ** x
        return s

    def minimax(self, b, d, a, bta, maxim):
        for c in self.wins:
            if all(i in b["O"] for i in c): return 1000 - d
            if all(i in b["X"] for i in c): return -1000 + d
        if len(b["O"])+len(b["X"])==9 or d>=6: return self.evaluate(b)
        best = -9999 if maxim else 9999
        for i in range(9):
            if i not in b['O']+b['X']:
                (b['O'] if maxim else b['X']).append(i)
                val = self.minimax(b, d+1, a, bta, not maxim)
                (b['O'] if maxim else b['X']).remove(i)
                if maxim: best,a=max(best,val),max(a,val)
                else: best,bta=min(best,val),min(bta,val)
                if bta<=a: break
        return best

    def check_win(self, moves):
        for combo in self.wins:
            if all(i in moves for i in combo):
                for i in combo: list_btn[i].btn.config(bg='red')
                for q in list_btn: q.btn.config(state=DISABLED)
                messagebox.showinfo("Игра окончена", "Компьютер выиграл!"); return True
        return False

    def check_draw(self):
        if len(btn_click)+len(btn_comp)==9:
            for q in list_btn: q.btn.config(state=DISABLED, bg='#ddd')
            messagebox.showinfo("Игра окончена", "Ничья!"); return True
        return False

    def comp_turn(self):
        board = {'O': btn_comp.copy(), 'X': btn_click.copy()}
        move,best=None,-9999
        for i in range(9):
            if i not in board['O']+board['X']:
                board['O'].append(i)
                score=self.minimax(board,0,-9999,9999,False)
                board['O'].remove(i)
                if score>best: best,move=score,i
        if move is not None:
            btn_comp.append(move); list_btn[move].btn.config(text='O', state=DISABLED)
            if not self.check_win(btn_comp): self.check_draw()

    def click(self, _):
        if not game_active:
            messagebox.showinfo("Внимание","Сначала нажмите Start!"); return
        if self.index in btn_click+btn_comp: return
        self.btn.config(text='X', state=DISABLED); btn_click.append(self.index)
        if not self.check_draw(): self.comp_turn()


def draw():
    index,x,y=0,0,0
    for _ in range(3):
        for _ in range(3):
            list_btn.append(Btn(x,y,index)); index+=1; x+=size_btn
        x=0; y+=size_btn

window.resizable(False, False)
draw()
window.mainloop()
