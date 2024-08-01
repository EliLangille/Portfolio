#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "FoodItems.h"

// Function to create a FoodItem struct and return a pointer to it
struct FoodItem *createFoodItem() {
    // Buffer clearer variable
    int c;

	// Allocate memory for a FoodItem construct, return NULL if malloc fails
    struct FoodItem *item = malloc(sizeof(struct FoodItem));
    if (item == NULL) {
        return NULL;
    }
    
    // Get and assign the name of the FoodItem
    printf("\nEnter the food's name: ");
    if (fgets(item->name, sizeof(item->name), stdin) == NULL) {
        // If fgets error occurs, handle memory and buffer, return NULL
        free(item);
        size_t len = strlen(item->name);
        if (item->name[len - 1] != '\n') {
            while ((c = getchar()) != '\n' && c != EOF);
        }
        return NULL;
    }
    
    // Remove trailing \n if present in item name, clear buffer if not (fgets overflowed)
    size_t len = strlen(item->name);
    if (len > 0 && item->name[len - 1] == '\n') {
        item->name[len - 1] = '\0';
    } else {
    	while ((c = getchar()) != '\n' && c != EOF);
    }

    // Get and assign the calories of the FoodItem
    printf("Enter the food's calories: ");
    if (scanf("%lu", &item->calories) != 1) {
        // If scanf fails, handle memory and buffer, return NULL
        free(item);
        while ((c = getchar()) != '\n' && c != EOF);
        return NULL;
    }

    // Remove leftover chars in the buffer from scanf()
    while ((c = getchar()) != '\n' && c != EOF);
    return item;
}

// Function to print the info of a FoodItem struct, returns nothing
void displayFoodItem(const struct FoodItem *item) {
    printf("Name: %s, Calories: %lu\n", item->name, item->calories);
}