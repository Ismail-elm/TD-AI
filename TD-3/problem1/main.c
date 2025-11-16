#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "functions.h"


int main() {
    FILE *fin = fopen("Infinite-Library/test10.txt", "r");
    if (!fin) { printf("Erreur : impossible d’ouvrir Infinite-Library/test10.txt\n"); return 1; }

    FILE *fout = fopen("output_generated.txt", "w");
    if (!fout) { printf("Erreur : impossible de créer output_generated.txt\n"); fclose(fin); return 1; }

    int n;
    fscanf(fin, "%d", &n);

    struct AVLNode* root = NULL;
    for (int i = 0; i < n; i++) {
        int val;
        fscanf(fin, "%d", &val);
        root = insertAVL(root, val);
    }

    int q;
    fscanf(fin, "%d", &q);
    for (int i = 0; i < q; i++) {
        int target;
        fscanf(fin, "%d", &target);
        fprintf(fout, searchAVL(root, target) ? "YES\n" : "NO\n");
    }

    fclose(fin);
    fclose(fout);

    if (compare_files("output_generated.txt", "Infinite-Library/test10-output.txt"))
        printf("Fichiers identiques.\n");
    else
        printf("Fichiers différents.\n");

    return 0;
}
