#include <string>
#include <sstream>
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

int bf[11] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
float U10[11] = {0.1, 0.9, 2.45, 4.4, 6.7, 9.3, 12.3, 15.5, 19, 22.7, 26.5};
long double Feff[3] = {846396.84, 24639684.4725712, 187516.243575778};
float hs = 0.4;
float Beaufort[33] = {0, 0, 0, 0.0348, 0.0187, 0.00847, 0.0033, 0.00033, 0, 0, 0, 0, 0, 0, 0.01848, 0.0099, 0.00363, 0.00066,
			0.00011, 0, 0, 0, 0, 0, 0, 0.11761, 0.09154, 0.03829, 0.00847, 0.00077, 0, 0, 0};

/*
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
vector<float> wave_conditions()
{
	vector< float> x;
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
	x.insert(x.begin(),development.begin(),development.end());
	x.insert(x.begin()+33,HS.begin(),HS.end());
	x.insert(x.begin()+66,TP.begin(),TP.end());
	return x;
}

// Calculation of q,where q defines s the mean wave overtopping inflow (m3/s/m)
vector<float> qo()
{
	vector <float> z;
	z = wave_conditions();
	vector <float> qo_elements;
	for (int n=33 ; n<66; n++){
		for(float i=0.5 ; i<3.5 ; i += 0.1){
			float k1;
			k1 = exp(-2.6 * i / z[n]) * 0.2 * pow((9.81 *pow(z[n], 3)),0.5);
			qo_elements.push_back(k1);
		}
	}
	return qo_elements;
}
*/
// Calculation of Phydro, where Phydro defines the power of collected waves
// Calculation of Pwave,where Pwave defines the initial wave power that runs in the breakwater
// Calculation of nhydro, where nhydro  is defined as the proportion of the hydraulic power and the wave power
vector <float> Phydro()
{
	vector<float> Phydro;
	for (int i= 0.5 ; i<3.5;i +=0.1){
		int k1;
		k1 = 1000*9.81 *i;
		Phydro.push_back(k1);
	}
	return Phydro;
}
/*
vector <float> Pwave()
{
	vector <float> Pwave;
	for(int n=33,m=66 ; n<66 && m<99 ; ++n,++m){
		float k2;
		vector<float> z;
		z = wave_conditions();
		k2 =478.88 * pow(z[n] ,2) * (z[m]);
		Pwave.push_back(k2);
	}
	return Pwave;
}
vector<float> nhydro()
{
	vector <float> nhydro;
	vector <float> z,n;
	z = Pwave();
	n = Phydro();
	for (int k=0 ; k<33 ;++k){
		for(int l=0 ; l<30 ; ++l){
			float k3;
			k3 = n[l]/z[k];
			nhydro.push_back(k3);
		}
	}
	return nhydro;
}
*/



int main()
{
	/*
	vector<float> z;
	z = Ua();
	for (vector<float>::const_iterator i = z.begin(); i != z.end(); ++i){
		cout << *i<<' ';
	}
	vector<float> k;
	k =wave_conditions();
	for( vector<float>::const_iterator m = k.begin(); m != k.end(); ++m){
		cout<< *m<<' '	;
	}

	vector <float> y;
	y = qo();
	for( vector<float>::const_iterator n = y.begin(); n != y.end(); ++n){
		cout<< *n<<' '	;
	}
	*/
	vector <float> t;
	t=Phydro();
	for( vector<float>::const_iterator n = t.begin(); n != t.end(); ++n){
		cout<< *n<<' '	;
	}
	return 0;
}