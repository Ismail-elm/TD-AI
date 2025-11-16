#ifndef AVL_H
#define AVL_H

#include <stdio.h>

struct AVLNode {
    int data;
    struct AVLNode *left, *right;
    int height;
};

// --- Fonctions utilitaires ---
int max(int a, int b);
int height(struct AVLNode* node);
int getBalance(struct AVLNode* node);

// --- Rotations ---
struct AVLNode* rightRotate(struct AVLNode* y);
struct AVLNode* leftRotate(struct AVLNode* x);

// --- Insertion et recherche ---
struct AVLNode* insertAVL(struct AVLNode* node, int key);
int searchAVL(struct AVLNode* root, int target);

// --- Comparaison de fichiers ---
int compare_files(const char *file1, const char *file2);

#endif
