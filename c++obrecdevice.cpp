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
 std::vector<float> Ua()
{
	for (int n=0 ; n <12 ; ++n)
	{
		std::vector<float> x;
		float k;
		k = pow(U10[n],1.23)*0.71;
		x.push_back(k);
	return x;	
	}
}

int main()
{
	std::vector<float> z;
	z = Ua();
	cout << z;
	return 0;
}