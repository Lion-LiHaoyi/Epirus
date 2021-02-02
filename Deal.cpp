//此程序用于处理对战过程记录并生成表格
#include <cstdio>
#define For(i, j, k) for (int i = j; i < k; i++)
const int x=5,y=17,z=18;
int table[x][y][z][x][y+1][z][y], a, b, c, d, e, f, a2, b2, c2, d2, e2, f2, count;
int main(){
	freopen("count.txt", "r", stdin);
	scanf("%d", &count);
	freopen("table.txt", "r", stdin);
	For(i, 0, x) For(j, 0, y) For(k, 0, z) For(o, 0, x) For(p, 0, y+1) For(q, 0, z) For(r, 0, y)
	scanf("%d", &table[i][j][k][o][p][q][r]);
	freopen("data", "r", stdin);
	while (scanf("%d%d%d%d%d%d", &a, &b, &c, &d, &e, &f) != EOF) {
		if (a != -1 || b != -1 || c != -1 || d != -1 || e != -1 || f != -1) {
			if (a2 != 0 || b2 != 0 || c2 != 0 || d2 != 0 || e2 != 0 || f2 != 0)
				table[a][b][c2][d][e2][f2][b]++;
		}else a = b = c = d = e = f = 0, count++;
		a2 = a, b2 = b, c2 = c, d2 = d, e2 = e, f2 = f;
	}
	freopen("table.data", "w", stdout);
	For(i, 0, x) For(j, 0, y) For(k, 0, z) For(o, 0, x) For(p, 0, y+1) For(q, 0, z){
		For(r, 0, y) printf("%d ", table[i][j][k][o][p][q][r]);
		printf("\n");
	}
	freopen("count.txt", "w", stdout);
	printf("%d", count);
}
