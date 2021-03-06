//此程序用于处理对战过程记录并生成表格
#include <iostream>
#include <fstream>
using namespace std;
#define For(i, j, k) for (int i = j; i < k; i++)
const int x = 3, y = 18, z = 15;
unsigned int table[x][y][z][x][y][z][y - 1];
int a, b, c, d, e, f, a2, b2, c2, d2, e2, f2, count;
int main(){
	ifstream in1("count.txt");
	in1 >> count;
	ifstream in2("table.data");
	For(i, 0, x) For(j, 0, y) For(k, 0, z) For(o, 0, x) For(p, 0, y) For(q, 0, z) For(r, 0, y-1)
	in2>>table[i][j][k][o][p][q][r];
	ifstream in3("data");
	while (in3 >> a >> b >> c >> d >> e >> f) {
		if (a != -1 || b != -1 || c != -1 || d != -1 || e != -1 || f != -1) {
			if (a2 != 0 || b2 != 0 || c2 != 0 || d2 != 0 || e2 != 0 || f2 != 0)
				if (c2 < 15 && f2 < 15)
					table[a - 1][b2][c2][d - 1][e2][f2][b]++;
		}else a = b = c = d = e = f = 0, count++;
		a2 = a, b2 = b, c2 = c, d2 = d, e2 = e, f2 = f;
	}
	ofstream out1("table.data");
	For(i, 0, x) For(j, 0, y) For(k, 0, z) For(o, 0, x) For(p, 0, y) For(q, 0, z){
		For(r, 0, y - 1) out1 << table[i][j][k][o][p][q][r] << " ";
		out1 << endl;
	}
	ofstream out2("count.txt");
	out2 << count;
}
