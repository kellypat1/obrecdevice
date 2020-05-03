#include <string>
#include <sstream>
#include <iostream>
#include <math.h>
#include <vector>
#include <boost/range/algorithm.hpp>
#include <boost/range/irange.hpp>

using namespace std;

int bf[11] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
float U10[11] = {0.1, 0.9, 2.45, 4.4, 6.7, 9.3, 12.3, 15.5, 19, 22.7, 26.5};
long double Feff[3] = {846396.84, 24639684.4725712, 187516.243575778};
float hs = 0.4;
float Beaufort[33] = {0, 0, 0, 0.0348, 0.0187, 0.00847, 0.0033, 0.00033, 0, 0, 0, 0, 0, 0, 0.01848, 0.0099, 0.00363, 0.00066,
			0.00011, 0, 0, 0, 0, 0, 0, 0.11761, 0.09154, 0.03829, 0.00847, 0.00077, 0, 0, 0};


//Calculation of Ua for every wind speed
vector<float> Ua()
{
	vector<float> x;
	for (int n=0 ; n <11 ; n++)
	{
		float k;
		k = pow(U10[n],1.23)*0.71;
		x.push_back(k);
	}
	return x;	
}

// Calculation of the development,HS and TP of every wave
vector<vector<float>> wave_conditions()
{
	vector<vector< float>> x;
	vector <float> z;
	z =Ua();
	vector<float> development,HS,TP;
	for (int n=0; n<3 ; n++)
	{
		for(int i=0; i<11 ; i++){
			float k1,k2,k3;
			k1 = (9.81*Feff[n])/pow(z.at(i),2);
			if (k1 >22800){
				k2 = 0.243* pow(z.at(i),2)/9.81;
				k3 = 8.13 * z.at(i)/9.81;
			}
			else{
				k2=pow(k1,0.5) * 0.0016 * pow(z.at(i),2) / 9.81;
				k3=pow(k1, 0.33) * 0.286 * (z.at(i) / 9.81);
			}
			development.push_back(k1);
			HS.push_back(k2);
			TP.push_back(k3);
		}
	}
	x.push_back(development);
	x.push_back(HS);
	x.push_back(TP);
	return x;
}

// Calculation of q,where q defines s the mean wave overtopping inflow (m3/s/m)
vector<float> qo()
{
	vector<vector <float>> z;
	z = wave_conditions();
	vector <float> qo_elements;
	for (int n=0 ; n<33; n++){
		for(float i=0.5 ; i<3.4 ; i += 0.1){
			float k1;
			k1 = exp(-2.6 * i / z[1][n]) * 0.2 * pow((9.81 *pow(z[1][n], 3)),0.5);
			qo_elements.push_back(k1);
		}
	}
	return qo_elements;
}

// Calculation of Phydro, where Phydro defines the power of collected waves
// Calculation of Pwave,where Pwave defines the initial wave power that runs in the breakwater
// Calculation of nhydro, where nhydro  is defined as the proportion of the hydraulic power and the wave power
vector <float> nhydro()
{
	vector<int> Phydro_elements;
	vector <float> Pwave_elements,nhydro_elements;
	for (float i= 0.5 ; i<3.4;i +=0.1){
		int k1;
		k1 = 1000*9.81 *i;
		Phydro_elements.push_back(k1);
	}
	for(int n=0 ; n< 33 ; ++n){
		float k2;
		vector<vector<float>> z;
		z = wave_conditions();
		k2 =478.88 * pow(z[1][n] ,2) * (z[2][n]);
		Pwave_elements.push_back(k2);
	}
	vector <float> nhydro;
	for (int k=0 ; k<Pwave_elements.size() ;++k){
		for(int l=0 ; l<Phydro_elements.size() ; ++l){
			float k3;
			k3 = Phydro_elements[l]/Pwave_elements[k];
			nhydro.push_back(k3);
		}
	}
	return nhydro;
}
// Calculation of the power of the water turbine, Pk,el,for every nhydro and qo
vector<float> pkel()
{
	vector<float> pkel_elements, z,t;
	z= nhydro();
	t=qo();
	for(int i=0; i<z.size();++i){
		float k1;
		k1=1000*9.81*z[i]*t[i];
		pkel_elements.push_back(k1);
	}
	return pkel_elements;
}

// Multiply the power of the water turbine with every beaufort in the certain harbor
// Every list includes the values of addbf for a certain Rc each time
vector<float> sum_rc()
{
	vector <float>listaddbf,l;
	int k=0;
	l=pkel();
	while(k<l.size()-29){
		for(int i=0; i<(sizeof(Beaufort)/sizeof(Beaufort[0]));i++){
			for(int k: boost::irange(k,30+k)){
				float k1;
				k1= l[k] * Beaufort[i];
				listaddbf.push_back(k1);		
			}
		k+=30;
		}
	}
	vector<vector <float>> Rc_value;
	for (int i =0;i<30;++i){
		vector<float> rc1;
		for(int j=i; j<listaddbf.size();j+=30){
			float k2;
			k2=listaddbf[j];
			rc1.push_back(k2);
		}
		Rc_value.push_back(rc1);
	}
	vector <float> sum_rc_values;
	for (int i =0 ;i<Rc_value.size();++i){
		float sum = 0;
		for(int j=i;j<Rc_value[i].size();++j){
			sum +=Rc_value[i][j] ;
		}
		sum_rc_values.push_back(sum);
	}
	cout<<Rc_value.size()<<"------------------------------------------------------"<<endl;
	cout<<listaddbf.size()<<endl;
	return sum_rc_values;
}

// Defination of the different scenarios for the hydraulic height of water above water turbine (m)
vector<vector<float>> Hk()
{
	vector<vector<float>>  scenarios;
	vector <float> hk;
	for(float i=0.0 ;i < 3.45; i+=0.05){
		for(float k = 0.5; k<3.4; k+=0.1){
			float k1;
			k1 = (k-i)/2 +hs;
			if ((k1<k) && (k1>0)){
				hk.push_back(k1);
			}
			else{
				break;
			}
		}
	}
	scenarios.push_back(hk);
	return scenarios;
}

// Calculation of all the different scenarios for the Hk values in order to find the power of the water turbine(pkel) and the crest freeboard (RC) each time.
// Calculation of the best scenario that maximize the power of the water turbine and calculation of Hk and Rc for this value of pkel.

vector<vector<float>> maximum_of_scenario()
{
	vector <float> list,listrc,max_value,n,scenario;
	vector<float >k1,k2;
	vector<vector<float> z;
	z=Hk();
	n=sum_rc();
	for (int i =0;i<z.size();++i){
		k1= z[i]*n;
		scenario.push_back(k1);
		k2 = max_value(scenario.begin(),scenario.end());
		max_of_scenario.push_back(k2);

	}


}
def maximum_of_scenario():
	listh1 = []
	listrc = []
	max_of_all = []
	max_of_scenario = []
	k11 = 0
	scenario = []
	listsum = sum_rc()
	for i in np.arange(0, 70):
		if Hk()[i] != []:
			k11 = np.array(Hk()[i]) * listsum
			scenario.append(k11)
			k16 = [np.amax(k11)]
			max_of_scenario.append(k16)
			k17 = np.argmax(k11)
			k18 = k17 * 0.1 + 0.5
			max_of_all.append(max_of_scenario)
			#k20= (i *0.05) + hs
			#listh1.append(k20)
			print("h1--------------", i * 0.05, "----------", k11, "\nmax_value------------", k16, "\nRC--------", k18)
			if max_of_all == max(max_of_all):
				k19 = (i * 0.05) + hs
				listh1.append(k19)
				listrc.append(k18)
				k21 = max_of_all
				# print("hydraulic height of water above water turbine,Hk (m)-------", listh1 ,"\nCrest freeboard,Rc(m)------", listrc, "\nMaximum power of the water turbine,Pkel (W/m)-----------", k21)
			else:
				pass
		else:
			pass
	return scenario,k21, listh1, listrc

*/


int main()
{
	vector<vector<float>> z;
	z =wave_conditions();
	for( int k=0; k<z.size();++k){
		for (int j = 0; j < z[k].size(); j++){
            cout << z[k][j] << " "; 
		}
        cout << endl; 
	}
	vector<float>n;
	n=qo();
	for( int k=0; k<n.size();++k){
		cout << n[k];
	cout<<"qo end------------------"<<endl;
	}
	vector<float> p;
	p=nhydro();
	for( int k=0; k<p.size();++k){
		cout << p[k] <<" ";
	cout<<"nhydro end-------------------------------"<<endl;
	}
	vector <float> p1;
	p1 = pkel();
	for (int k=0 ;k <p1.size();++k){
		cout<<p1[k]<<endl;
	}

	vector<float> s;
	s = sum_rc();
	for( int k=0; k<s.size();++k){
		//for (int j=0; j<s[k].size();++j){
		cout << s[k] <<endl;
	}

	vector<vector<float>> p2;
	p2= Hk();
	for( int k=0; k<p2.size();++k){
		for (int j=0; j<p2[k].size();++j){
		cout << p2[k][j] <<" ";
		}
		cout<<endl;
	}
	return 0;
}