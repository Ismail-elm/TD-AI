#include "magic_kingdom.h"

int N, M;
int A, B;
int head[MAXN], to[MAXM*2], nxt[MAXM*2], ec = 0;
int visited[MAXN];
int dista[MAXN];

// Compare deux fichiers
int compare_files(const char *file1, const char *file2) {
    FILE *f1 = fopen(file1, "r");
    FILE *f2 = fopen(file2, "r");
    if (!f1 || !f2) return 0;

    int c1, c2;
    do {
        c1 = fgetc(f1);
        c2 = fgetc(f2);
        if (c1 != c2) {
            fclose(f1);
            fclose(f2);
            return 0;
        }
    } while (c1 != EOF && c2 != EOF);

    fclose(f1);
    fclose(f2);
    return 1;
}

void addEdge(int u, int v) {
    to[ec] = v;
    nxt[ec] = head[u];
    head[u] = ec++;
}

// DFS itératif
void dfs_iterative(int start) {
    int stack[MAXM*2];
    int top = 0;
    stack[top++] = start;

    while (top > 0) {
        int u = stack[--top];
        if (visited[u]) continue;
        visited[u] = 1;

        for (int e = head[u]; e != -1; e = nxt[e]) {
            int v = to[e];
            if (!visited[v]) stack[top++] = v;
        }
    }
}

// BFS pour le plus court chemin
int bfs(int start, int target) {
    for (int i = 1; i <= N; i++) dista[i] = -1;

    int *q = malloc((N+5)*sizeof(int));
    int front = 0, back = 0;
    q[back++] = start;
    dista[start] = 0;

    while (front < back) {
        int u = q[front++];
        if (u == target) break;
        for (int e = head[u]; e != -1; e = nxt[e]) {
            int v = to[e];
            if (dista[v] == -1) {
                dista[v] = dista[u] + 1;
                q[back++] = v;
            }
        }
    }

    int ans = dista[target];
    free(q);
    return ans;
}

