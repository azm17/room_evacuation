import random
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

L,W =100,100
rho = 0.1
rhoD = 0
N = L*W*rho
P = 2
r = 0.2
exit_width = 10

class person():
    def __init__(self,number,x,y):
        global L,W,rho,rhoD
        self.number = number
        self.personal = 0
        self.x = x#現在の場所
        self.y = y
        
        self.next_x = None#次行きたい場所
        self.next_y = None
        
        if number < L*W*rho*rhoD:
            self.personal = 0
        else:
            self.personal = 1
        
           
    def ikitai_basyo(self):#行きたい場所を決める
        global W
        global r
        DX,DY = float(W)/2,0
        
        #if DX <= self.x:
        alh = np.arctan2((self.x - DX), (self.y - DY))
        #else:
            #alh =2*np.pi - abs(np.arctan2(self.x - DX, self.y - DY))
        z = abs(np.cos(alh))+abs(np.sin(alh))
        
        Pu = r/4 + ((1-r)*(-np.cos(alh))*(1-np.sign(np.cos(alh))))/(2*z)
        Pd = r/4 + ((1-r)*(np.cos(alh))*(1+np.sign(np.cos(alh))))/(2*z)
        Pr = r/4 + ((1-r)*(-np.sin(alh))*(1-np.sign(np.sin(alh))))/(2*z)
        Pl = r/4 + ((1-r)*(np.sin(alh))*(1+np.sign(np.sin(alh))))/(2*z)
        
        rnd = random.random()
        
        if 0 < rnd <= Pu:#up
            self.next_x = self.x 
            self.next_y = self.y+1
        elif Pu<rnd<=Pu+Pd:#down
            self.next_x = self.x 
            self.next_y = self.y-1
        elif Pu+Pd<rnd<=Pu+Pd+Pr:#right
            self.next_x = self.x+1
            self.next_y = self.y
        elif Pu+Pd+Pr<rnd<=Pu+Pd+Pr+Pl:#left
            self.next_x = self.x-1
            self.next_y = self.y
        
        
class room():
    def __init__(self,L,W,rho):
        self.W = W#WIDE
        self.L = L#LENGTH
        self.M = int(L*W*rho)#人数
        self.person = []#プレイや一人一人を格納
        xy_list = []#プレイヤーの座標の候補を格納
        self.hitogairu_basyo = None#プレイヤーがいる場所
        
        for i in range(W):
            for j in range(L):
                xy_list.append([i,j])#プレイヤーの座標の候補を格納
        
        for i in range(self.M):
            tmp = xy_list.pop(int(random.random()*len(xy_list)))
            x,y = tmp[0],tmp[1]
            self.person.append(person(i,x,y))#M人分の人を作る
    
    
    def hitogairu_basyo_kazoeru(self):
        x_list,y_list=[],[]
        for i in range(self.M):
            x_list.append(self.person[i].x)
            y_list.append(self.person[i].y)
        self.hitogairu_basyo = x_list,y_list
        
        
    def no_winner(self,a):
        for i in range(len(a)):
            self.person[a[i]].next_x = None
            self.person[a[i]].next_y = None
         
            
    def hanbetsu(self,i):
        for x,y in zip(self.hitogairu_basyo[0],self.hitogairu_basyo[1]):
            if self.person[i].next_x == x and self.person[i].next_y == y:#人がいるとこと行きたい
                self.person[i].next_x = None
                self.person[i].next_y = None
            elif self.person[i].next_x is None or self.person[i].next_y is None:
                pass
            elif self.person[i].next_x < 0 or self.person[i].next_y < 0:#x,y<0の場合
                self.person[i].next_x = None
                self.person[i].next_y = None
            elif self.person[i].next_x > self.W or self.person[i].next_y > self.L:#x,y>w,lの場合
                self.person[i].next_x = None
                self.person[i].next_y = None
    
    
    def idou(self,k):
        global N
        global P
        for i in range(self.M):
            self.person[i].ikitai_basyo()#行きたい場所を決める
        
        self.hitogairu_basyo_kazoeru()#人がいる場所を確認
        
        for i in range(self.M):#行きたい場所がダメなところの場合
            self.hanbetsu(i)
            if self.person[i].next_x == None or self.person[i].next_y == None:
                self.person[i].ikitai_basyo()
                self.hanbetsu(i)
       
        for i in range(self.M):#移動
            competitor = [i]
            if self.person[i].next_x == None:
                continue
            for j in range(self.M):
                if self.person[j].next_x == None or i == j:
                    pass
                elif self.person[i].next_x == self.person[j].next_x and self.person[i].next_y == self.person[j].next_y:
                    competitor.append(j)
 
            if len(competitor) == 1:
                self.person[i].x = self.person[i].next_x
                self.person[i].y = self.person[i].next_y
                
                self.person[i].next_x = None
                self.person[i].next_y = None
                
            elif len(competitor) == 2:
                player1 = competitor[0]
                player2 = competitor[1]
                if self.person[player1].personal == 0 and self.person[player2].personal == 0:
                    if 0 <= random.random() < 1/2:
                        if 0 <= random.random() < 1/P:
                            self.person[player1].x = self.person[player1].next_x
                            self.person[player1].y = self.person[player1].next_y
                            self.person[player2].next_x = None
                            self.person[player2].next_y = None
                        else:
                            self.no_winner(competitor)
                    else:
                        if 0 <= random.random() < 1/P:
                            self.person[player1].next_x = None
                            self.person[player1].next_y = None
                            self.person[player2].x = self.person[player1].next_x
                            self.person[player2].y = self.person[player1].next_y
                        else:
                            self.no_winner(competitor)
                elif self.person[player1].personal == 1 and self.person[player2].personal == 0:                         
                    if 0 <= random.random() < 1/P:
                        self.person[player1].next_x = None
                        self.person[player1].next_y = None
                        self.person[player2].x = self.person[player1].next_x
                        self.person[player2].y = self.person[player1].next_y
                    else:
                        self.no_winner(competitor)
                elif self.person[player1].personal == 0 and self.person[player2].personal == 1:                         
                    if 0 <= random.random() < 1/P:
                        self.person[player2].next_x = None
                        self.person[player2].next_y = None
                        self.person[player1].x = self.person[player1].next_x
                        self.person[player1].y = self.person[player1].next_y
                    else:
                        self.no_winner(competitor)
                elif self.person[player1].personal == 1 and self.person[player2].personal == 1:
                    winner = competitor[int(random.random()*len(competitor))]
                    self.person[winner].x = self.person[winner].next_x
                    self.person[winner].y = self.person[winner].next_y
                    for i in competitor:
                         self.person[i].next_x = None
                         self.person[i].next_y = None
                
            elif len(competitor) >= 3:
                detector = []
                for i in range(len(competitor)):
                    if self.person[competitor[i]].personal == 0:
                        detector.append(competitor[i])
                
                if len(detector) == 0:
                    winner = competitor[int(random.random()*len(competitor))]
                    self.person[winner].x = self.person[winner].next_x
                    self.person[winner].y = self.person[winner].next_y
                    for i in competitor:
                        self.person[i].next_x = None
                        self.person[i].next_y = None
                
                else:
                    winner = detector[int(random.random()*len(detector))]
                    if len(detector) == 1:
                        self.person[winner].x = self.person[winner].next_x
                        self.person[winner].y = self.person[winner].next_y
                        
                    elif 0 <= random.random() <1/(len(detector)-1):    
                        if 0 <= random.random() < 1/P:
                            self.person[winner].x = self.person[winner].next_x
                            self.person[winner].y = self.person[winner].next_y
                            for i in competitor:
                                self.person[i].next_x = None
                                self.person[i].next_y = None
                        else:
                            self.no_winner(competitor) 
                    else:
                        self.no_winner(competitor)
        
        exit_person = []
        for i in range(self.M):
            if np.floor(self.W/2-(exit_width/2)) <= self.person[i].x <= np.floor(self.W/2+(exit_width/2)) and self.person[i].y <= 0:
                exit_person.append(i)
                
        for i in reversed(exit_person):
            del self.person[i]
            self.M = self.M-1
            N = N-1
             
        '''          
        self.plot()
        
    def plot(self):
        #global ims
        x,y = [],[]
        xd,yd =[],[]
                
        for i in range(self.M):
            if self.person[i].personal == 0:
                xd.append(self.person[i].x)
                yd.append(self.person[i].y)
            elif self.person[i].personal ==1:
                x.append(self.person[i].x)  
                y.append(self.person[i].y)
        
        plt.figure(figsize=(10,10))
        plt.ylim([-0.5,self.L+0.5])
        plt.xlim([-0.5,self.W+0.5])
        linex = [self.W*3/5+0.2,self.W+0.2,self.W+0.2,-0.2,-0.2,self.W*2/5-0.2]
        liney = [-0.2,-0.2,self.L+0.2,self.L+0.2,-0.2,-0.2]
        plt.plot(linex,liney,'r-')
        plt.scatter(x, y,c='blue')
        plt.scatter(xd, yd,c='red')
        plt.savefig('./figure2/'+'.png')'''

def main():
    global L,W,rho,exit_time
    r = room(L,W,rho)
    for i in range(50000):
        r.idou(i)
        if N == 0:
            break
    exit_time = i+1
        
    
if __name__ == "__main__":
    k = 10
    for i in range(11):
        rhoD = i/10
        print('rhoD=',rhoD)
        for j in range(1,10,1):
        	exit_ave = 0
        	rho = j/10
        	for i in range(k):
        		N = L*W*rho
        		main()
        		exit_ave = exit_ave + exit_time
        	print('rho=',rho,'EXIT TIME AVERAGE',int(exit_ave/k))
        
    