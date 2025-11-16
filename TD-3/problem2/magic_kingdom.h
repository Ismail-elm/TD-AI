#ifndef MAGIC_KINGDOM_H
#define MAGIC_KINGDOM_H

#include <stdio.h>
#include <stdlib.h>

#define MAXN 100005
#define MAXM 200005


extern int N, M;
extern int A, B;
extern int head[MAXN], to[MAXM*2], nxt[MAXM*2], ec;
extern int visited[MAXN];
extern int dista[MAXN];


int compare_files(const char *file1, const char *file2);
void addEdge(int u, int v);
void dfs_iterative(int start);
int bfs(int start, int target);

#endif
