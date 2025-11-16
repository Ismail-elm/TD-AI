#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "functions.h"

// --- Structure d'un nœud AVL ---
struct AVLNode {
    int data;
    struct AVLNode *left, *right;
    int height;
};

// --- Fonctions utilitaires ---
int max(int a, int b) { return (a > b) ? a : b; }
int height(struct AVLNode* node) { return node ? node->height : 0; }

// --- Rotations ---
struct AVLNode* rightRotate(struct AVLNode* y) {
    struct AVLNode* x = y->left;
    struct AVLNode* T2 = x->right;
    x->right = y;
    y->left = T2;
    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;
    return x;
}

struct AVLNode* leftRotate(struct AVLNode* x) {
    struct AVLNode* y = x->right;
    struct AVLNode* T2 = y->left;
    y->left = x;
    x->right = T2;
    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;
    return y;
}

// --- Balance factor ---
int getBalance(struct AVLNode* node) {
    return node ? height(node->left) - height(node->right) : 0;
}

// --- Insertion AVL (O(log n)) ---
struct AVLNode* insertAVL(struct AVLNode* node, int key) {
    if (!node) {
        struct AVLNode* new_node = (struct AVLNode*)malloc(sizeof(struct AVLNode));
        new_node->data = key;
        new_node->left = NULL;
        new_node->right = NULL;
        new_node->height = 1;
        return new_node;
    }

    if (key < node->data) node->left = insertAVL(node->left, key);
    else if (key > node->data) node->right = insertAVL(node->right, key);
    else return node; // pas de doublons

    node->height = 1 + max(height(node->left), height(node->right));
    int balance = getBalance(node);

    // Cas rotation
    if (balance > 1 && key < node->left->data) return rightRotate(node);
    if (balance < -1 && key > node->right->data) return leftRotate(node);
    if (balance > 1 && key > node->left->data) {
        node->left = leftRotate(node->left);
        return rightRotate(node);
    }
    if (balance < -1 && key < node->right->data) {
        node->right = rightRotate(node->right);
        return leftRotate(node);
    }

    return node;
}


// --- Recherche AVL (O(log n)) ---
int searchAVL(struct AVLNode* root, int target) {
    while (root) {
        if (root->data == target) return 1;
        root = (target < root->data) ? root->left : root->right;
    }
    return 0;
}

// --- Comparaison fichiers ---
int compare_files(const char *file1, const char *file2) {
    FILE *f1 = fopen(file1, "r");
    FILE *f2 = fopen(file2, "r");
    if (!f1 || !f2) {
        printf("Erreur ouverture fichier pour comparaison.\n");
        return 0;
    }

    char line1[100], line2[100];
    int identical = 1, line = 1;

    while (fgets(line1, sizeof(line1), f1) && fgets(line2, sizeof(line2), f2)) {
        if (strcmp(line1, line2) != 0) {
            printf("Différence ligne %d:\n  %s  %s\n", line, line1, line2);
            identical = 0;
        }
        line++;
    }

    if ((fgets(line1, sizeof(line1), f1) != NULL) ||
        (fgets(line2, sizeof(line2), f2) != NULL))
        identical = 0;

    fclose(f1);
    fclose(f2);
    return identical;
}
