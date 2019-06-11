# -*- coding: utf-8 -*-
"""
Created on Tue May 29 13:36:57 2018

@author: azm
"""
import random
import matplotlib.pyplot as plt
import math
import numpy as np

class person():
    def __init__(self,number,x,y):
        self.number = number
        self.x = x#現在の場所
        self.y = y
        self.next_x = None#次行きたい場所
        self.next_y = None
    
    def ikitai_basyo(self,L,xr,xl):#行きたい場所を決める
        rnd = random.random()
        R=0.3
        a=3
        xT = L/2#(L+1)/2
        if (self.y < a*(self.x-xr) or self.y < -a*(self.x-xl)):
            yT = -L/10 +2*L/5*(-self.y/math.sqrt((self.y-L/2+5)**2+self.y**2)+math.sin(math.atan(a)))
        else:
            yT = -L/10
        #yT = -L/10
        
        syahen = math.sqrt(abs(self.x-xT)**2+abs(self.y-yT)**2)
        tate = -xT+self.x
        yoko = -yT+self.y
        cos  = yoko/syahen
        sin  = tate/syahen
        Z = abs(cos) + abs(sin)
        
        Ru = 1/4*R + (1-R)*(-cos*(1-np.sign(cos)))/(2*Z)
        Rd = 1/4*R + (1-R)*(cos*(1+np.sign(cos)))/(2*Z)
        Rr = 1/4*R + (1-R)*(-sin*(1-np.sign(sin)))/(2*Z)
        Rl = 1/4*R + (1-R)*(sin*(1+np.sign(sin)))/(2*Z)
        
        #Ru,Rd,Rr,Rl = 0/4,2/4,1/4,1/4
        #print(Rd)
        #print(math.degrees(alpha),math.degrees(math.asin(tate/syahen)))
        
        if 0 < rnd <= Ru:#up
            self.next_x = self.x 
            self.next_y = self.y+1
        elif Ru<rnd<=Ru+Rd:#down
            self.next_x = self.x 
            self.next_y = self.y-1
        elif Ru+Rd<rnd<=Ru+Rd+Rr:#right
            self.next_x = self.x+1
            self.next_y = self.y
        elif Ru+Rd+Rr<rnd<=Ru+Rd+Rr+Rl:#left
            self.next_x = self.x-1
            self.next_y = self.y
    
    def ikitai_basyo_iku(self):
        self.x = self.next_x#現在の場所に次の場所にする
        self.y = self.next_y
        
        self.ikitai_basyo_kesu()#行きたい場所を消す
    
    def ikitai_basyo_kesu(self):
        self.next_x = None#行きたい場所を消す
        self.next_y = None
        
    def show_property(self):#プレイや１人の情報を表示
        print(self.number,'('+str(self.x)+','+str(self.y)+')','('+str(self.next_x)+','+str(self.next_y)+')')
        
class room():
    def __init__(self,L,W,rho):
        self.W = W#yの長さ
        self.L = L#xの長さ
        self.rho = rho
        self.Ld = self.L/5
        self.xl= self.L/2 - self.Ld/2
        self.xr =self.L/2 + self.Ld/2
        self.M = int((self.L-2)*(self.W-2)*self.rho)#人数
        self.person = []#プレイや一人一人を格納
        self.hitogairu_basyo = None#プレイヤーがいる場所
        xy_list = []#プレイヤーの座標の候補を格納
        
        for i in range(1,L):#1<= x <= L-1
            for j in range(1,W):#1 <= x <= W-1
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
    
    def idou(self,nn):
        #print('移動'+str(nn+1)+'回目')
        for i in range(self.M):
            self.person[i].ikitai_basyo(self.L,self.xr,self.xl)#行きたい場所を決める
        #print('行きたい場所を選んだ後')
        #self.show_property()
        
        self.hitogairu_basyo_kazoeru()#人がいる場所を確認
        
        for i in range(self.M):#行きたい場所がダメなところの場合
            for x,y in zip(self.hitogairu_basyo[0],self.hitogairu_basyo[1]):
                if self.person[i].next_x == x and self.person[i].next_y == y:#行きたい場所に人がいるとき
                    self.person[i].ikitai_basyo_kesu()
            
            if self.person[i].next_x is None or self.person[i].next_y is None:#Noneとばす
                pass
            elif self.xl <= self.person[i].next_x <= self.xr and self.person[i].next_y <= 0:#
                pass
            elif not((0 < self.person[i].next_x < self.L) and (0 < self.person[i].next_y < self.W)):#境界条件,壁にはいけない
                self.person[i].ikitai_basyo_kesu()

        #print('いけない場所を除く')
        #self.show_property()
        
        for i in range(self.M):#移動
            kabuttahito = [self.person[i].number]
            if self.person[i].next_x == None:
                continue
            for j in range(self.M):
                if self.person[j].next_x == None or i == j:
                    pass
                elif self.person[i].next_x == self.person[j].next_x and self.person[i].next_y == self.person[j].next_y:
                    kabuttahito.append(self.person[j].number)
            #print(kabuttahito)
            
            if len(kabuttahito) == 1:
                self.person[i].ikitai_basyo_iku()
            
            elif len(kabuttahito) == 2:
                player1 = kabuttahito[0]
                player2 = kabuttahito[1]
                if 0 <= random.random() < 1/2:#CC
                    self.person[player1].ikitai_basyo_iku()
                    self.person[player2].ikitai_basyo_kesu()
                    #print('win player',player1)
                else:
                    self.person[player2].ikitai_basyo_iku()
                    self.person[player1].ikitai_basyo_kesu()
                    #print('win player',player2)
            
            elif len(kabuttahito) >= 3:
                winner = kabuttahito[int(random.random()*len(kabuttahito))]
                #print('winner player',winner)
                self.person[winner].ikitai_basyo_iku()
                for k in kabuttahito:
                    self.person[k].ikitai_basyo_kesu()
        #print('対戦終了')
        #self.show_property()
        for i in range(self.M):#逃げる(出口)
            if self.xl <= self.person[i].x <= self.xr and self.person[i].y <= 0:#take out of the system
                self.person[i].x = -100
                self.person[i].y = -100
        
        nokori = self.nokori_ninzu()
        self.plot(nn,nokori)
        return nokori
        #print('------')
    def nokori_ninzu(self):
        n=0
        for i in range(self.M):
            if 0 <= self.person[i].x <= self.L and 0 <= self.person[i].y <= self.W:
                n += 1
        print(n)
        return n
        
    def plot(self,nn,nokori):#図を作成
        x,y = [],[]#青点
        xg,yg =[],[]#次逃げれそうな人（オレンジ）
        linex = [self.xr+0.2,self.W,self.W,0,0,self.xl-0.2]#wall
        liney = [0,0,self.L,self.L,0,0]#wall
        
        for i in range(self.M):
            if self.xl <= self.person[i].x <= self.xr and self.person[i].y == 1:#逃げれそうな人に色を付ける
                xg.append(self.person[i].x)
                yg.append(self.person[i].y)
            elif self.person[i].x >=1 and self.person[i].y >=0:
                x.append(self.person[i].x)
                y.append(self.person[i].y)

        plt.figure(figsize=(self.L/8,self.W/8))
        plt.ylim([-0.5,self.L+0.5])
        plt.xlim([-0.5,self.W+0.5])
        plt.plot(linex,liney,'r-')
        plt.scatter(x, y)
        plt.scatter(xg, yg)
        plt.text(1,1, r't='+str(nn))
        plt.text(1,3, r'n='+str(nokori))
        plt.savefig(r'./figure2/'+str(nn)+'.png')
        plt.close()
    
    def show_property(self):
        for i in range(self.M):
            self.person[i].show_property()
        print('------')
 
# 散布図を描画
#plt.scatter(x, y)
def main():
    L,W = 50,50
    rho = 0.4
    
    r = room(L,W,rho)
    
    #print('最初の状態')
    #r.show_property()
    
    for i in range(501):
        n = r.idou(i)
        if n <= 0:
            break
    
    #print('最後の状態')
    #r.show_property()
    
if __name__ == "__main__":
    main()