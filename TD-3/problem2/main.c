#include <stdio.h>
#include <stdlib.h>
#include "magic_kingdom.h"

int main() {
    FILE *in = fopen("Aladdin-Magic-Kingdom/test10.txt","r");
    if (!in) { perror("Erreur ouverture input"); return 1; }

    fscanf(in,"%d %d",&N,&M);

    for (int i = 0; i <= N; i++) {
        head[i] = -1;
        visited[i] = 0;
    }

    for (int i=0;i<M;i++){
        int u,v;
        fscanf(in,"%d %d",&u,&v);
        addEdge(u,v);
        addEdge(v,u);
    }

    fscanf(in,"%d %d",&A,&B);
    fclose(in);

    // compter les royaumes
    int kingdoms = 0;
    for(int i=1;i<=N;i++){
        if(!visited[i]){
            dfs_iterative(i);
            kingdoms++;
        }
    }

    int shortest = bfs(A,B);

    // écrire résultat
    FILE *out = fopen("output_generated.txt","w");
    fprintf(out,"%d\n%d\n", kingdoms, shortest);
    fclose(out);

    // comparer avec fichier attendu
    if (compare_files("output_generated.txt", "Aladdin-Magic-Kingdom/test10-output.txt"))
        printf("Fichiers identiques.\n");
    else
        printf("Fichiers différents.\n");

    return 0;
}
