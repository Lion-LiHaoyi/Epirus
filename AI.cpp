//本程序用于执行训练程序
#include <windows.h>
#include <iostream>
#include <fstream>
using namespace std;
int main(){
	int t, tt;
	cout <<
	        "Enter the number of training sessions and the number of cycles per cycle\n\
    The more training times, the more accurate the program, but the slower the speed\n";
	cin >> t >> tt;
	ofstream out("time");
	out << tt << endl;
	cout << "Done";
	for (int i = 0; i < t; i++) {
		cout << i << endl;
		system("EpirusN.py");
		system("Deal.exe");
	}
}
