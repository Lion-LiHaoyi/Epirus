//此程序用于处理对战过程记录并生成表格
#include <cstdio>
#define For(i, j, k) for (int i = j; i < k; i++)
int table[15][17][15][15][17][15], a, b, c, d, e, f, a2, b2, c2, d2, e2, f2, count;
int main(){
	freopen("data.txt", "r", stdin);
	freopen("table.txt", "w", stdout);
	while (scanf("%d%d%d%d%d%d", &a, &b, &c, &d, &e, &f) != EOF) {
		if (a != -1 || b != -1 || c != -1 || d != -1 || e != -1 || f != -1) {
			if (a2 != 0 || b2 != 0 || c2 != 0 || d2 != 0 || e2 != 0 || f2 != 0)
				table[a][b][c2][d][e2][f2]++;
		}else a = b = c = d = e = f = 0, count++;
		a2 = a, b2 = b, c2 = c, d2 = d, e2 = e, f2 = f;
	}
	For(i, 0, 15) For(j, 0, 17) For(k, 0, 15) For(o, 0, 15) For(p, 0, 17) For(q, 0, 15)
	printf("%d ", table[i][j][k][o][p][q]);
	freopen("count.txt", "w", stdout);
	printf("%d", count);
}
