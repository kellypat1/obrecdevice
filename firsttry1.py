import math
import numpy as np


bf = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
U = [0.1, 0.9, 2.45, 4.4, 6.7, 9.3, 12.3, 15.5, 19, 22.7, 26.5]
#Feff1 = float(input("type feef x: "))
#Feff2 = int(input("type feff y: "))
#Feff3 = int(input("type feff z: "))
#Feef = [Feff1,Feff2,Feff3]
#hs = float(input("a value for Hs in metre: "))



Feff1 = float(246396.84)
hs = float(0.4)



x = []
def Ua(x):
    for num in U:
        k = float((np.power(num,1.23)) * 0.71)
        x.append(k)
    return x
print(Ua(x))
p =[]
HS=[]
TP=[]

def dev(p):
    for num in x:
        k1 =float(9.81 * Feff1/(num**2))
        k2 = float(0.243 * np.power(num, 2) / 9.81) if k1 > 22800 else float((k1**0.5) * 0.0016 * (num**2) / 9.81)
        k3 = float((8.13 * num) / 9.81) if k1 > 22800 else float((np.power(k1, 0.33) * 0.286 * num/ 9.81))
        p.append(k1)
        HS.append(k2)
        TP.append(k3)

    return p,HS,TP
print(dev(p))
print(len(HS))


qo=[]
def calc(qo):
    for num in HS:
        for i in np.arange(0.5, 3.5, 0.1):
            k4 = float(math.exp(-2.6 * i / num) * 0.2 * (9.81 * np.power(num,3)) ** 0.5)
            qo.append(k4)
    return qo
print(calc(qo))
print(len(calc(qo)))
phy=[]
def calc(phy):
    for i in np.arange(0.5,3.5,0.1):
        k6 = 1000*9.81*i
        phy.append(k6)
    return phy
print(calc(phy))
pwa = []
def calc(pwa):
    for num1,num2 in zip(HS,TP):
        k7 =[float(478.88*(num1**2)*(num2))]
        pwa.append(k7)
    return pwa

print(calc(pwa))
print(len(pwa))
no = []
def calc(no):
    for x1 in pwa:
        for x2 in phy:
            k8 = float(x2/x1)
            no.append(k8)
    return no
print (calc(no))
print(len(calc(no)))

def calc():
    i_list=[]
    for i in np.arange(0,3.5,0.05):
        hk=[]
        for k in np.arange(0.5,3.5,0.1):
            k11=float((k-i)/2+hs)
            hk.append(k11)
        i_list.append(hk)    
    return i_list
print(calc()[0][0])
#print(len(calc(hk)))
pkel=[]


def calc(pkel):
    for x1, x2 in zip(no,qo):
        k9 = float(1000*9.81*x1*x2)
        pkel.append(k9)
    return pkel
print(calc(pkel))
print(len(pkel))

def zouzouni():
    list=[]
    for i in np.arange(0,30):
        sum=[]
        #print("i---------------------------------",i)
        for j in np.arange(i,len(pkel),30):
            sum.append(pkel[j])
        #print("sum-----------------",sum)
        list.append(sum)
    return list

def kelly():
	kaltsa = zouzouni()
	results = []
	for i in range(0,len(kaltsa)):
		sum=0
		for j in kaltsa[i]:
			sum+=j
		results.append(sum)
	return results
print("-----------------------")
#k = zouzouni()
#print(len(k))
print(kelly())
print("----------------------------------------")


