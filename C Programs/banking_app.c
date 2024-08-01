#include <stdio.h>

int main() {
	// Initialize variables
	char name[51];
	int menu_choice;
	float balance = 1000.00;
	float deposit;
	float withdrawal;			

	// Greet user
	printf("Welcome to the Banking App!\n");

	// Loop to get user's name and greet them
	while (1) {
		// Prompt for input
		printf("\nEnter your name: ");
		
		// Grab name input and restart name grabber loop if fgets fails
		if (fgets(name, sizeof(name), stdin) == NULL) {
			printf("Invalid input, please try again.\n");
			continue;		
		}

		// Check for and remove the \n character in name if present
		for (int i = 0; i < sizeof(name); i++) {
			if (name[i] == '\n') {
				name[i] = '\0';
				break;
			}
		}
			
		// Greet user once the name string is fixed and break the while loop
		printf("Hello, %s!\n", name);
		break;
	}

	// Program menu and actions
	while (menu_choice != 4) {
		// Display menu options
		printf("\nMenu:\n1. Show Balance\n2. Deposit\n3. Withdraw\n4. Exit\nSelect an option: ");
		
		// Uses an if/else rather than if-continue so the buffer clearer at the end is not skipped
		// Get user's menu choice and restart menu loop if invalid 
		if (!scanf("%d", &menu_choice) || menu_choice > 4 || menu_choice < 1) {
			printf("\nInvalid choice, please try again.\n");
		} else { // If input is valid, execute chosen action
			// Execute menu choice
			switch (menu_choice) {
				// Show user's balance
				case 1: 
					printf("\nYour current account balance is $%.2f\n", balance);
					break;
				// Deposit money
				case 2:		
					while (1) {
						// Clear the buffer of any leftover characters from the menu or from previous iterations of deposit prompt
						int c;
	       	 				while ((c = getchar()) != '\n' && c != EOF); 

						// Deposit prompt
						printf("\nEnter the amount to deposit, between $1 and $100: ");
					 	
						// If scanf fails or deposit is invalid, try again
						if (!scanf("%f", &deposit) || deposit < 1 || deposit > 100) {
							printf("Invalid amount, please try again.\n");
							continue;
						}
						
						// Update balance
						balance += deposit;
						
						// Print deposit statement to user
						printf("Depositing $%.2f, updated balance is $%.2f.\n", deposit, balance);
						
						break;
					}

					break;
				// Withdraw money
				case 3:
					// Run until user chooses a valid withdrawal amount
					while (1) {
						// Clear the buffer of any leftover characters from the menu or from previous iterations of withdrawal prompt
						int c;
       		 				while ((c = getchar()) != '\n' && c != EOF); 

						// Withdrawal prompt
						printf("\nEnter the amount to withdraw: ");
					 
						// If scanf fails or withdrawal amount is invalid, try again
							// Note: This allows for withdrawing into the negative
						if (!scanf("%f", &withdrawal) || withdrawal <= 0) {
							printf("Invalid amount, please try again.\n");
							continue;
						}
						
						// Update balance
						balance -= withdrawal;
						
						// Print withdrawal statement to user
						printf("Withdrawing $%.2f, updated balance is $%.2f.\n", withdrawal, balance);

						break;
					}

					break;
				// Exit program (4 breaks the menu while loop)
				case 4:
					printf("\nGoodbye!\n");
					break;
				// Handle any other errors
				default:
					printf("\nInvalid choice, please try again.\n");
					break;	
			}
		}

		// Clear the buffer of any leftover characters after each loop of the menu
		int c;
       		while ((c = getchar()) != '\n' && c != EOF); 
	}				
	return 0;
}
