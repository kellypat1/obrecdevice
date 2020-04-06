import math
import numpy as np
import operator
bf = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
U10= [0.1, 0.9, 2.45, 4.4, 6.7, 9.3, 12.3, 15.5, 19, 22.7, 26.5]
Feff = [84215.245553961, 24639684.4725712, 187516.243575778]
hs = 0.4
Beaufort = [0,0,0,0.0348,0.0187,0.00847,0.0033,0.00033,0,0,0,0,0,0,0.01848,0.0099,0.00363,0.00066,0.00011,0,0,0,0,0,0,0.11761,0.09154,0.03829,0.00847,0.00077,0,0,0]

'''''
Feff1 = float(input("type feef x: "))
Feff2 = float(input("type feff y: "))
Feff3 = float(input("type feff z: "))
Feef = [Feff1,Feff2,Feff3]
hs = float(input("a value for Hs in metre: "))
'''''



#Calculation of Ua for every wind speed
def Ua():
    x = []
    for num in U10:
        k = float((np.power(num, 1.23)) * 0.71)
        x.append(k)
    return x

print("Ua values(m/s)-----------",Ua())

#Calculation of the development,HS and TP of every wave
def dev():
    dev = []
    HS = []
    TP = []
    for i in Feff:
        for num in Ua():
            k1 = float(9.81 * i / (num ** 2))
            k2 = float(0.243 * np.power(num, 2) / 9.81) if k1 > 22800 else float((k1 ** 0.5) * 0.0016 * (num ** 2) / 9.81)
            k3 = float((8.13 * num) / 9.81) if k1 > 22800 else float((np.power(k1, 0.33) * 0.286 * num / 9.81))
            dev.append(k1)
            HS.append(k2)
            TP.append(k3)
    return dev, HS, TP

print("dev--------------------------", dev()[0])
print("HS------------------------------",dev()[1])
print("TP-----------------------------", dev()[2])

# Calculation of q,where q defines s the mean wave overtopping inflow (m3/s/m)
def qo():
    listqo = []
    for num in dev()[1]:
        for i in np.arange(0.5, 3.5, 0.1):
            k4 = float(math.exp(-2.6 * i / num) * 0.2 * (9.81 * np.power(num, 3)) ** 0.5)
            listqo.append(k4)
    return listqo

print("Mean wave overtopping inflow(m3/s/m)-------",qo())

#Calculation of Phydro, where Phydro defines the power of collected waves
def Phydro():
    listPhydro = []
    for i in np.arange(0.5, 3.5, 0.1):
        k6 = 1000 * 9.81 * i
        listPhydro.append(k6)
    return listPhydro

print("Power of collected waves---------",Phydro())

#Calculation of Pwave,where Pwave defines the initial wave power that runs in the breakwater
def Pwave():
    listPwave=[]
    for num1, num2 in zip(dev()[1], dev()[2]):
        k7 = float(478.88 * (num1 ** 2) * (num2))
        listPwave.append(k7)
    return listPwave

print("Initial wave power that runs in the breakwater---------",Pwave())

#Calculation of nhydro, where nhydro  is defined as the proportion of the hydraulic power and the wave power
def nhydro():
    listnhydro=[]
    for x1 in Pwave():
        for x2 in Phydro():
            k8 = float(x2 / x1)
            listnhydro.append(k8)
    return listnhydro

print("The proportion of the hydraulic power and the wave power---",nhydro())

#Defination of the different scenarios for the hydraulic height of water above water turbine (m)

def Hk():
    scenarios = []
    for i in np.arange(0, 3.5, 0.05):
        hk = []
        for k in np.arange(0.5, 3.5, 0.1):
            k11 = float((k - i) / 2 + hs)
            if k11 <k and k11 >0:
                hk.append(k11)
            else:
                break
        scenarios.append(hk)
    return scenarios

print("Hydraulic height of water above water turbine (m)--------",Hk())

#Calculation of the power of the water turbine, Pk,el,for every nhydro and qo
def pkel():
    listpkel=[]
    for i, k in zip(nhydro(), qo()):
        k9 = float(1000 * 9.81 * i * k)
        listpkel.append(k9)
    return listpkel

print("The power of water turbine(W/m)--------",pkel())

# Multiply the power of the water turbine with every beaufort in the certain harbor
listaddbf = []
def addbf():
    k = 0
    while k < 961:
        for i in range(0, len(Beaufort)):
            for k in range(k, 30 + k):
                k15 = pkel()[k] * Beaufort[i]
                listaddbf.append(k15)
        k += 30
    return listaddbf

print("Multiply the power of the water turbine with every beaufort-----",addbf())

# Every list includes the values of addbf for a certain Rc each time
def Rc_values():
    listRc_value = []
    for i in np.arange(0, 30):
        RC = []
        #print("Rc---------------------------------", (i*0.1)+0.5)
        for j in np.arange(i, len(listaddbf), 31):
            k20 = listaddbf[j]
            RC.append(k20)
        #print("Rc_Value-----------------", RC)
        listRc_value.append(RC)
    return listRc_value

Rc_values()

#Summarize the values of every Rc in order to find one value for each Rc
def sum_rc():
    sum_rc_values = []
    for i in range(0, len(Rc_values())):
        sum = 0
        for j in Rc_values()[i]:
            sum += j
        sum_rc_values.append(sum)
    return sum_rc_values
print("Summarize the values of every Rc-----------",sum_rc())
print(len(sum_rc()))

#Calculation of all the different scenarios for the Hk values in order to find the power of the water turbine(pkel) and the crest freeboard (RC) each time.
#Calculation of the best scenario that maximize the power of the water turbine and calculation of Hk and Rc for this value of pkel.
max_of_all = []
listh1 = []
listrc = []
def maximum_of_scenario():
    max_of_scenario = []
    k11 = 0
    scenario = []
    for i in np.arange(0, 70):
        if Hk()[i] != []:
            k11 = np.array(Hk()[i]) * sum_rc()
            scenario.append(k11)
            k16 = [np.amax(k11)]
            max_of_scenario.append(k16)
            k17 = np.argmax(k11)
            k18=k17*0.1+0.5
            max_of_all.append(max_of_scenario)
            print("h1--------------", i * 0.05, "----------", k11,"\nmax_value------------" ,k16,"\nRC--------",k18)
            if max_of_all == max(max_of_all):
                k19 = (i * 0.05)+hs
                listh1.append(k19)
                listrc.append(k18)
                k21=max_of_all
                print("hydraulic height of water above water turbine,Hk (m)-------", listh1 ,"\nCrest freeboard,Rc(m)------", listrc, "\nMaximum power of the water turbine,Pkel (W/m)-----------", k21)
            else:
                pass
        else:
            pass
    return k21,listh1,listrc
maximum_of_scenario()

print("----------------------")
print("FINAL RESULTS")
print("hydraulic height of water above water turbine,Hk (m)-------", listh1,
"\nCrest freeboard,Rc(m)------", listrc, "\nMaximum power of the water turbine,Pkel (W/m)-----------",max(max(max_of_all))) 
