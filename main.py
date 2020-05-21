from graphics import *
from math import *


class Stare:
    def __init__(self, name):
        self.nume = name

    def Punct(self):
        return Point(self.x, self.y)


def same(nod1, nod2):
    if nod1.name == nod2.name:
        return 1
    else:
        return 0

def search(lista, nume):
    for i in range(len(lista)):
        if lista[i].nume == nume:
            return i
    else:
        return "eroare"


def selftranzitie(nod, nume, win, init = "not", poz = 0):
    x = nod.x
    y = nod.y
    if x < 250 or init == "initial":
        #print("leeeeeeft")
        directie = "left"
    elif x > 550:
        directie = "right"
    elif y <= 250:
        directie = "up"
    else:
        directie = "down"
    if directie == "left":
        x -= 70
        c = Circle(Point(x + 20, y), 2)

    if directie == "right":
        x += 70
        c = Circle(Point(x - 20, y), 2)

    if directie == "up":
        y -= 70
        c = Circle(Point(x, y + 20), 2)

    if directie == "down":
        y += 70
        c = Circle(Point(x, y - 20), 2)
    c.setFill('pink')
    c.setOutline('pink')
    cir = Circle(Point(x, y), 20)
    cir.setOutline('pink')
    cir.setWidth(2)
    cir.draw(win)
    c.draw(win)
    text = Text(Point(x, y - poz * 15), nume)
    text.setSize(10)
    text.setFace("helvetica")
    text.setTextColor('cyan3')
    text.draw(win)


def tranzitie(nod1, nod2, nume, win, poz = 0):
    x1 = nod1.x
    y1 = nod1.y
    x2 = nod2.x
    y2 = nod2.y
    xvar = (x1 - x2) / 10
    yvar = (y1 - y2) / 10
    x1 -= xvar
    x2 += xvar
    y1 -= yvar
    y2 += yvar
    if (x1 - x2) ** 2 > (y1 - y2) ** 2:
        xtextvar = 10
        ytextvar = 0
    else:
        ytextvar = 10
        xtextvar = 0
    ln = Line(Point(x1, y1), Point(x2, y2))
    ln.setArrow("last")
    ln.setWidth(3)
    x = (3 * x1 + x2) // 4
    y = (3 * y1 + y2) // 4
    pt = Point(x + xtextvar, y + ytextvar + poz * 22)
    if x1 > x2 or y1 < y2:
        ln.setFill('aqua')
    else:
        ln.setFill('yellow')
    tx = Text(pt, nume)
    tx.setTextColor('red')
    tx.setFace("helvetica")
    tx.setSize(20)
    ln.draw(win)
    tx.draw(win)


def stare(nod, final, win):
    x = nod.x
    y = nod.y
    text = nod.nume
    cir = Circle(Point(x, y), 50)
    cir.setOutline('white')
    cir.setWidth(2)
    cir.draw(win)

    if final == 1:
        cir2 = Circle(Point(x, y), 40)
        cir2.setOutline('white')
        cir2.setWidth(2)
        cir2.draw(win)
    elif final == -1:
        ln = Line(Point(x, y + 100), Point(x, y + 50))
        ln.setArrow("last")
        ln.setWidth(3)
        ln.setOutline('green')
        ln.draw(win)

    tx = Text(Point(x, y), text)
    tx.setSize(20)
    tx.setTextColor('red')
    tx.draw(win)


class Automat:

    def citire(self):
        with open("automat.in", 'r') as f:
            f.readline()
            s = f.readline().split()  #
            self.stari = []
            for i in s:
                self.stari.append(Stare(i))
            t = f.readline().replace("\n", "")  #
            self.sin = self.stari[search(self.stari, t)]
            s = f.readline().split()
            self.sfin = []
            for i in s:
                print(search(self.stari, i))
                (self.sfin).append(self.stari[search(self.stari, i)])
            self.simbolstart = f.readline().replace('\n',"")
            self.tranzitii = {}
            #de forma stare:{(litera,simpbol_pop):((simboluri_push), stare2)}
            for i in self.stari:
                self.tranzitii[i] = {}

            x = f.readline()

            while x:
                x = x.split()
                x[3] = x[3].split("+")
                x[3].reverse()
                self.tranzitii[self.stari[search(self.stari, x[0])]][(x[1],x[2])] = (tuple(x[3]), self.stari[search(self.stari, x[4])])
                x = f.readline()
            #print(self.tranzitii)

    def verificare(self, cuvant):
        s = self.sin
        #print(s.nume)
        ok = 1
        stack = [self.simbolstart]
        for i in cuvant:
            if len(stack):
                if (i,stack[-1]) in self.tranzitii[s].keys():
                    x = self.tranzitii[s][(i,stack[-1])]
                    #print("dadadada",x)
                    s = x[1]
                    #print(s.nume)
                    stack = stack[:-1] # pop din stiva
                    for k in x[0]:
                        if k != 'E': # E = epsilon
                            stack.append(k)
                    #print(stack)
                else:
                    ##print(stack)
                    #("???")
                    #print()
                    #print(i, cuvant)
                    #print(self.tranzitii[s].keys())
                    return 0
            else:
                #print('stack')
                return 0
        else:
            if len(stack) == 0:
                return 1  # vidarea stivei
            else:
                if s in self.sfin:
                    return 1  # stare finala
                else:
                    return 0
            if len(cuvant):
                #print('stop',s.nume)
                if(('E',stack[-1]) in self.tranzitii[s].keys()) and (self.tranzitii[s][('E',stack[-1])][1] in self.sfin):
                    return 1
            else:
                if s in self.sfin:
                    return 1
                return 0

    def afisare_grafica(self):
        win = GraphWin("Automat", 1600, 800)
        win.setBackground('black')

        ##############################
        # determinare coordonate noduri
        ##############################

        n = len(self.stari)
        alpha = 2 * pi / n
        # print(alpha)
        r = 300  # raza

        for i in range(n):
            x = r * sin(i * alpha)
            y = r * cos(i * alpha)
            self.stari[i].x = x + 400
            self.stari[i].y = y + 400
            # print(x,y)

        #(stare(self.sin, -1, win))
        afisate = []
        #starile afisate
        for s1 in self.stari:
            if s1 in self.sfin:
                stare(s1, 1, win)
            elif s1 == self.sin:
                stare(s1, -1, win)
            else:
                stare(s1, 0, win)
            for j in self.tranzitii[s1].values():
                s2 = j[1]
                if s1.nume < s2.nume:
                    pair = (s1.nume,s2.nume)
                else:
                    pair = (s2.nume,s1.nume)
                if pair not in afisate:
                    afisate.append(pair)
                    tranzlist = []
                    for t in self.tranzitii[s1].keys():
                        if self.tranzitii[s1][t][1] == s2:
                            tranz = t[0] + ", " + t[1] + "/" + "+".join(self.tranzitii[s1][t][0][::-1])
                            tranzlist.append(tranz)
                    print(s1.nume,tranzlist,s2.nume)
                    dev = len(tranzlist) // 2
                    for i in range(len(tranzlist)):
                        if s1 == s2:
                            if s1 == self.sin:
                                selftranzitie(s1, tranzlist[i], win, 'initial', poz=i - dev)
                            else:
                                selftranzitie(s1,tranzlist[i],win,poz = i - dev)
                        else:
                            tranzitie(s1,s2,tranzlist[i],win,poz = i - dev)

        # de forma stare:{(litera,simpbol_pop):((simboluri_push), stare2)}

        #####################################
        #####################################

        input_box = Entry(Point(1200, 400), 30)
        input_box.setFace("helvetica")
        input_box.setStyle('bold')
        input_box.draw(win)
        output = Text(Point(1200, 350), "da")
        output.setSize(25)
        ln = Line(Point(800, 0), Point(800, 800))
        ln.setWidth(3)
        ln.setFill('white')
        ln.setOutline('white')
        ln.draw(win)

        if aut.verificare("") == 1:
            output.setTextColor('lime')
        else:
            output.setTextColor('red')
        output.draw(win)

        while True:
            cuv = input_box.getText()
            if aut.verificare(cuv) >= 1:
                input_box.setTextColor('lime')
                output.setText("Cuvant acceptat")
                output.setTextColor('lime')
            else:
                input_box.setTextColor('red')
                output.setText("Cuvant respins")
                output.setTextColor('red')
        win.getMouse()  # Pause to view result
        win.close()  # Close window when done

        #####################################
        #####################################



aut = Automat()
aut.citire()
if(aut.verificare('0010101c1010100')):
    print("cuvant acceptat")
else:
    print("cuvant respins")
######################
aut.afisare_grafica()#
######################