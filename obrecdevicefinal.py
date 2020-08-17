import math
import numpy as np
import operator
import matplotlib.pyplot as plt
import sympy

bf = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
U10 = [0.1, 0.9, 2.45, 4.4, 6.7, 9.3, 12.3, 15.5, 19, 22.7, 26.5]
Feff = [846396.84, 24639684.4725712, 187516.243575778]
hs = 0.4
Beaufort = [0, 0, 0, 0.0348, 0.0187, 0.00847, 0.0033, 0.00033, 0, 0, 0, 0, 0, 0, 0.01848, 0.0099, 0.00363, 0.00066,
			0.00011, 0, 0, 0, 0, 0, 0, 0.11761, 0.09154, 0.03829, 0.00847, 0.00077, 0, 0, 0]
degree1= sympy.cot(26.58)

# Calculation of Ua for every wind speed
def Ua():
	x = []
	for num in U10:
		k = float((np.power(num, 1.23)) * 0.71)
		x.append(k)
	return x

# Calculation of the development,HS and TP of every wave
def wave_conditions():
	dev = []
	HS = []
	TP = []
	listUa = Ua()
	for i in Feff:
		for num in listUa:
			k1 = float(9.81 * i / (num ** 2))
			k2 = float(0.243 * np.power(num, 2) / 9.81) if k1 > 22800 else float((k1 ** 0.5) * 0.0016 * (num ** 2) / 9.81)
			k3 = float((8.13 * num) / 9.81) if k1 > 22800 else float((np.power(k1, 0.33) * 0.286 * num / 9.81))
			dev.append(k1)
			HS.append(k2)
			TP.append(k3)
	return dev, HS, TP

# Calculation of q,where q defines s the mean wave overtopping inflow (m3/s/m)
def qo():
	kofoed = []
	vandermeerjansen=[]
	owenmodel=[]
	hedgesandres=[]
	listdev = wave_conditions()
	p1list=[]
	p2list=[]
	c=[]
	degree1=sympy.cot(26.35)
	for num in listdev[1]:
		for i in np.arange(0.5, 3.5, 0.1):
			if i <= 0.75:
				k4 = float(0.4*sympy.sin(2*3.14/(3*i)) +0.6)
				k5=float((0.2*(sympy.cos(np.radians(26.35-30))**3)*k4*(9.81*(num**3))**0.5)*math.exp(-2.6*(i/num)))
				kofoed.append(k5)
			if i > 0.75:
				k4=1.00
				k5=float((0.2*(sympy.cos(np.radians(26.35-30))**3)*k4*(9.81*(num**3))**0.5)*math.exp(-2.6*(i/num)))
				kofoed.append(k5)
	for num1,num2 in zip(listdev[1],listdev[2]):
		k4=float(0.5/(num1*2*3.14/(9.81*(num2**2)))**0.5)
		p2list.append(k4)
	for num in listdev[1]:
		for i in np.arange(0.5,3.5,0.1):
			if k4>2:
				k5=float(0.2*(9.81*(num**3))**0.5)*math.exp(-2.6*(i/num))
				vandermeerjansen.append(k5)
			elif k4<2:
				k5=float(0.06*(9.81*(num**3))**0.5)*k4*math.exp(-5.2*(i/(num*k4)))*(0.5**0.5)
				vandermeerjansen.append(k5)
	for num in listdev[1]:
		for i in np.arange(0.5,3.5,0.1):
			if k4>2:
				k7=float(1.52*(3-(0.15*i)))
				c.append(k7)
			elif k4<2:
				k7=float(1.52*(1.35*i))
				c.append(k7)
	for num,num1 in zip(c,listdev[1]):
		for i in np.arange(0.5,3.5,0.1):
			k8=float(i/(num*num1))
			if k8>=1:
				k9=0
				hedgesandres.append(k9)
			elif k8<1:
				k9=float(0.00753*((9.81*((num*num1)**3))**0.5)*(1-k8)**4.17)
				hedgesandres.append(k9)
	for num,num1 in zip(listdev[1],listdev[2]):
		for i in np.arange(0.5, 3.5, 0.1):
			k4 = float(0.0117*num*num1*9.81*(math.exp((-21.71*i)/(num1*(num*9.81)**0.5))))
			owenmodel.append(k4)
		
	return kofoed,vandermeerjansen,owenmodel,hedgesandres

# Calculation of Phydro, where Phydro defines the power of collected waves
# Calculation of Pwave,where Pwave defines the initial wave power that runs in the breakwater
# Calculation of nhydro, where nhydro  is defined as the proportion of the hydraulic power and the wave power
def nhydro():
	listPhydro = []
	for i in np.arange(0.5, 3.5, 0.1):
		k6 = 1000 * 9.81 * i
		listPhydro.append(k6)
	listPwave = []
	listdev2 = wave_conditions()
	for num1, num2 in zip(listdev2[1], listdev2[2]):
		k7 = float(478.88 * (num1 ** 2) * (num2))
		listPwave.append(k7)
	listnhydro = []
	for x1 in listPwave:
		for x2 in listPhydro:
			k8 = float(x2 / x1)
			listnhydro.append(k8)
	return listnhydro

# Defination of the different scenarios for the hydraulic height of water above water turbine (m)
def Hk():
	scenarios = []
	for i in np.arange(0, 3.5, 0.05):
		hk = []
		for k in np.arange(0.5, 3.5, 0.1):
			k11 = float((k - i) / 2 + hs)
			round(k11,2)
			if k11 < k and k11 > 0:
				hk.append(k11)
			else:
				break
		scenarios.append(hk)
	return scenarios

# Calculation of the power of the water turbine, Pk,el,for every nhydro and qo
def pkel():
	listnhydro1 = nhydro()
	listqo1 = qo()
	k9=[]
	allscenarios=[]
	for m in range(0,len(listqo1),1):
		listpkel=[]
		for i, k in zip(listnhydro1,listqo1[m]):
			k9 = (1000 * 9.81 * i * k)
			listpkel.append(k9)
		allscenarios.append(listpkel)
	return allscenarios

# Multiply the power of the water turbine with every beaufort in the certain harbor
# Every list includes the values of addbf for a certain Rc each time
def sum_rc():
	
	sum_all=[]
	listaddbf_all=[]
	listpkel1=pkel()
	for n in range(0,len(listpkel1),1):	
		k=0
		listaddbf = []
		while k < (len(listpkel1[n])-29):
			for i in range(0, len(Beaufort)):
				for k in range(k, 30 + k):
					k15 = listpkel1[n][k] * Beaufort[i]
					listaddbf.append(k15)
			k += 30
		listaddbf_all.append(listaddbf)
	dividelistrc=[]
	for k in range(0,len(listaddbf_all),1):
		listRc_value = []
		for i in np.arange(0, 30):
			RC = []
			# print("Rc---------------------------------", (i*0.1)+0.5)
			for j in np.arange(i, len(listaddbf_all[k]), 31):
				k20 = listaddbf_all[k][j]
				RC.append(k20)
			# print("Rc_Value-----------------", RC)
			listRc_value.append(RC)
		dividelistrc.append(listRc_value)
	divide_all=[]
	for k in range(0,len(dividelistrc),1):
		sum_rc_values=[]
		for i in range(0, len(dividelistrc[k]),1):
			sum=0
			for j in dividelistrc[k][i]:
				sum+=j
			sum_rc_values.append(sum)
		divide_all.append(sum_rc_values)
	return divide_all

# Calculation of all the different scenarios for the Hk values in order to find the power of the water turbine(pkel) and the crest freeboard (RC) each time.
# Calculation of the best scenario that maximize the power of the water turbine and calculation of Hk and Rc for this value of pkel.
def maximum_of_scenario():
	listh1_divide=[]
	listrc_divide=[]
	k21_divide=[]
	listsum = sum_rc()
	for k in range(0,len(listsum),1):
		listh1 = []
		listrc = []
		max_of_all = []
		scenario = []
		k11=0
		max_of_scenario = []
		for i in np.arange(0, 70):
			if Hk()[i] != []:
				k11 = np.array(Hk()[i]) * listsum[k]
				scenario.append(k11)
				k16 = [np.amax(k11)]
				max_of_scenario.append(k16)
				k17 = np.argmax(k11)
				k18 = k17 * 0.1 + 0.5
				max_of_all.append(max_of_scenario)
				k20= (i *0.05) + hs
				#print("h1--------------", i * 0.05, "----------", k11, "\nmax_value------------", k16, "\nRC--------", k18)
				if max_of_all == max(max_of_all):
					k19 = (i * 0.05) + hs
					listh1.append(k19)
					listrc.append(k18)
					k21 = max_of_all
				else:
					pass
			else:
				pass
		listh1_divide.append(listh1)
		listrc_divide.append(listrc)
		k21_divide.append(k21)
	return k21_divide, listh1_divide, listrc_divide

def Poutput0():
	max2= maximum_of_scenario()
	hs_to=wave_conditions()
	vandermeerjansen1=[]
	listh=nhydro()
	listpkel2=[]	
	p2list=[]
	listPhydro = []
	listPwave = []
	listnhydro = []
	pout=[]
	total=0
	for i,z in zip(max2[2][1],max2[1][1]):
		k6 = 1000 * 9.81 * i
		listPhydro.append(k6)
		for num1, num2 in zip(hs_to[1], hs_to[2]):
			k7 = float(478.88 * (num1 ** 2) * (num2))
			listPwave.append(k7)
		for x1 in listPwave:
			for x2 in listPhydro:
				k8 = float(x2 / x1)
				listnhydro.append(k8)	
		for num1,num2 in zip(hs_to[1],hs_to[2]):
			k4=float(0.5/(num1*2*3.14/(9.81*(num2**2)))**0.5)
			p2list.append(k4)
		for num,k in zip(hs_to[1],listnhydro):
			if k4>2:
				k5=float(0.2*(9.81*(num**3))**0.5)*math.exp(-2.6*(i/num))
				vandermeerjansen1.append(k5)	
				k9= 1000*9.81*k*k5*z
				listpkel2.append(k9)
			elif k4<2:
				k5=float(0.06*(9.81*(num**3))**0.5)*k4*math.exp(-5.2*(i/(num*k4)))*(0.5**0.5)
				vandermeerjansen1.append(k5)
				k9= 1000*9.81*k*k5*z
				listpkel2.append(k9)
	for i,k in zip(Beaufort,listpkel2):
		pout.append(i*k*0.64*24*365/10000) 
	for ele in range(0,len(pout)):
		total =total+pout[ele]
	return total
print("Van der Meer model output energy ", Poutput0())

def Poutput1():
	max2= maximum_of_scenario()
	hs_to=wave_conditions()
	kofoed=[]
	listh=nhydro()
	listpkel2=[]	
	p2list=[]
	listPhydro = []
	listPwave = []
	listnhydro = []
	pout=[]
	total=0
	for i,z in zip(max2[2][0],max2[1][0]):
		k6 = 1000 * 9.81 * i
		listPhydro.append(k6)
		for num1, num2 in zip(hs_to[1], hs_to[2]):
			k7 = float(478.88 * (num1 ** 2) * (num2))
			listPwave.append(k7)
		for x1 in listPwave:
			for x2 in listPhydro:
				k8 = float(x2 / x1)
				listnhydro.append(k8)	
		for num,k in zip(hs_to[1],listnhydro):
			if i<=0.75:
				k4 = float(0.4*sympy.sin(2*3.14/(3*i)) +0.6)
				k5=float((0.2*(sympy.cos(np.radians(26.35-30))**3)*k4*(9.81*(num**3))**0.5)*math.exp(-2.6*(i/num)))
				kofoed.append(k5)	
				k9= 1000*9.81*k*k5*z
				listpkel2.append(k9)
			if i > 0.75:
				k4=1.00
				k5=float((0.2*(sympy.cos(np.radians(26.35-30))**3)*k4*(9.81*(num**3))**0.5)*math.exp(-2.6*(i/num)))
				kofoed.append(k5)
				k9= 1000*9.81*k*k5*z
				listpkel2.append(k9)
	for i,k in zip(Beaufort,listpkel2):
		pout.append(i*k*0.64*24*365/10000) 
	for ele in range(0,len(pout)):
		total =total+pout[ele]
	return total
print("Kofoed's model output energy ", Poutput1())


def Poutput2():
	max2= maximum_of_scenario()
	hs_to=wave_conditions()
	owen=[]
	listh=nhydro()
	listpkel2=[]	
	p2list=[]
	listPhydro = []
	listPwave = []
	listnhydro = []
	pout=[]
	total=0
	for i,z in zip(max2[2][2],max2[1][2]):
		k6 = 1000 * 9.81 * i
		listPhydro.append(k6)
		for num1, num2 in zip(hs_to[1], hs_to[2]):
			k7 = float(478.88 * (num1 ** 2) * (num2))
			listPwave.append(k7)
		for x1 in listPwave:
			for x2 in listPhydro:
				k8 = float(x2 / x1)
				listnhydro.append(k8)	
		for num,k,num1 in zip(hs_to[1],listnhydro,hs_to[2]):
			k4 = float(0.0117*num*num1*9.81*(math.exp((-21.71*i)/(num1*(num*9.81)**0.5))))
			owen.append(k4)
			k9= 1000*9.81*k*k4*z
			listpkel2.append(k9)
	for i,k in zip(Beaufort,listpkel2):
		pout.append(i*k*0.64*24*365/10000) 
	for ele in range(0,len(pout)):
		total =total+pout[ele]
	return total
print("Owen's model output energy ",Poutput2())

def Poutput3():
	max2= maximum_of_scenario()
	hs_to=wave_conditions()
	hedges=[]
	listh=nhydro()
	listpkel2=[]	
	p2list=[]
	listPhydro = []
	listPwave = []
	listnhydro = []
	pout=[]
	k6=[]
	total=0
	c=[]
	listparametre=[]
	for i,z in zip(max2[2][3],max2[1][3]):
		k6 = 1000 * 9.81 * i
		listPhydro.append(k6)
		for num1, num2 in zip(hs_to[1], hs_to[2]):
			k7 = float(478.88 * (num1 ** 2) * (num2))
			listPwave.append(k7)
		for x1 in listPwave:
			for x2 in listPhydro:
				k8 = float(x2 / x1)
				listnhydro.append(k8)	
		for num1,num2 in zip(hs_to[1],hs_to[2]):
			k4=float(0.5/(num1*2*3.14/(9.81*(num2**2)))**0.5)
			listparametre.append(k4)
		for t in listparametre:
			if t>2:
				k5=float(1.52*(3-(0.15*t)))
				c.append(k5)
			elif t<2:
				k7=float(1.52*(1.35*t))
				c.append(k7)
		for num,num1,k in zip(c,hs_to[1],listnhydro):
			k6=float(i/(num*num1))
			if k6>=1:
				k8=0
				hedges.append(k8)
				k9= 1000*9.81*k*k8*z
				listpkel2.append(k9)
			elif k6<1:
				k8=float(0.00753*((9.81*((num*num1)**3))**0.5)*(1-k6)**4.17)
				hedges.append(k8)
				k9= 1000*9.81*k*k8*z
				listpkel2.append(k9)
	for i,k in zip(Beaufort,listpkel2):
		pout.append(i*k*0.64*24*365/10000) 
	for ele in range(0,len(pout)):
		total =total+pout[ele]
	return total
print("Hedges and Reis model output energy ",Poutput3())

if __name__ == '__main__':
	#print("Ua values(m/s)-----------", Ua())
	#print("dev--------------------------", wave_conditions()[0])
	#print("HS------------------------------", wave_conditions()[1])
	#print("TP-----------------------------", wave_conditions()[2])
	#print("Mean wave overtopping inflow(m3/s/m)-------", qo())
	#print("The proportion of the hydraulic power and the wave power---", nhydro())
	#print("Hydraulic height of water above water turbine (m)--------", Hk())
	#print("The power of water turbine(W/m)--------", pkel())
	maximum1 = maximum_of_scenario()
	print("------------------------KOFOED'S MODEL--------------------------------------------------")
	print("FINAL RESULTS")
	print("hydraulic height of water above water turbine,Hk (m)-------", maximum1[1][0],
		  "\nCrest freeboard,Rc(m)------", maximum1[2][0], "\nMaximum power of the water turbine,Pkel (W/m)-----------",
		  max(max(maximum1[0][0])))
	print("------------------------VAN DER MER MODEL--------------------------------------------------")
	print("FINAL RESULTS")
	print("hydraulic height of water above water turbine,Hk (m)-------", maximum1[1][1],
		  "\nCrest freeboard,Rc(m)------", maximum1[2][1], "\nMaximum power of the water turbine,Pkel (W/m)-----------",
		  max(max(maximum1[0][1])))
	print("------------------------OWENS MODEL--------------------------------------------------")
	print("FINAL RESULTS")
	print("hydraulic height of water above water turbine,Hk (m)-------", maximum1[1][2],
		  "\nCrest freeboard,Rc(m)------", maximum1[2][2], "\nMaximum power of the water turbine,Pkel (W/m)-----------",
		  max(max(maximum1[0][2])))
	print("------------------------HEDGES and REIS MODEL--------------------------------------------------")
	print("FINAL RESULTS")
	print("hydraulic height of water above water turbine,Hk (m)-------", maximum1[1][3],
		  "\nCrest freeboard,Rc(m)------", maximum1[2][3], "\nMaximum power of the water turbine,Pkel (W/m)-----------",
		  max(max(maximum1[0][3])))
