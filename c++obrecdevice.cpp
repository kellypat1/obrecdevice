#include <string>
#include <sstream>
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

int bf[11] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
float U10[11] = {0.1, 0.9, 2.45, 4.4, 6.7, 9.3, 12.3, 15.5, 19, 22.7, 26.5};
double Feff[3] = {846396.84, 24639684.4725712, 187516.243575778};
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
vector<double> wave_conditions()
{
	vector< double> x;
	vector <float> z;
	z =Ua();
	vector<double> development,HS,TP;
	for (int n=0; n<3 ; n++)
	{
		for(int i=0; i<11 ; i++){
			double k1,k2,k3;
			k1 = (9.81*Feff[n])/pow(z.at(i),2);
			if (k1 >22800){
				k2 = 0.243* pow(z.at(i),2)/9.81;
				k3 = 8.13 * z.at(i)/9.81;
				HS.push_back(k2);
				TP.push_back(k3);
			}
			else{
				k2=pow(k1,0.5) * 0.0016 * pow(z.at(i),2) / 9.81;
				k3=pow(k1, 0.33) * 0.286 * z.at(i) / 9.81;
				HS.push_back(k2);
				TP.push_back(k3);
			}
			development.push_back(k1);
			
		}
	}
	x.insert(x.begin(),development.begin(),development.end());
	x.insert(development.end(),HS.begin(),HS.end());
	x.insert(HS.end(),TP.begin(),TP.end());
	return x;
}


int main()
{
	vector<float> z;
	z = Ua();
	for (vector<float>::const_iterator i = z.begin(); i != z.end(); ++i)
    cout << *i << ' ';
	vector<double> k;
	k =wave_conditions();
	for( vector<double>::const_iterator i = k.begin(); i != k.end(); ++i)
	cout<< *i<<' '	;

	return 0;
}