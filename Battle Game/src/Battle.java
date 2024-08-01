import java.util.ArrayList;
import java.util.Random;

/**
 * A class to create and run battles, matches, and tournaments between Player objects.
 */
public class Battle {
    /**
     * Runs a tournament of battles
     *
     * @param players An ArrayList of Player objects
     */
    public void playBracket(ArrayList<Player> players) {
        // Initialize variables
        ArrayList<Player> winners = new ArrayList<>();
        int highestWins = 0;

        // Nested for loops to make every player battle one another exactly once
            // 1 plays vs 2, 3, 4, 5
            // 2 plays vs 3, 4, 5
            // 3 plays vs 4, 5
            // 4 plays vs 5
        for (int i = 0; i < players.size() - 1; i++) {
            for (int j = i + 1; j < players.size(); j++) {
                playMatch(players.get(i), players.get(j));
            }
        }

        // Find the leading win total
        for (Player player : players) {
            if (player.getWins() > highestWins) {
                highestWins = player.getWins();
            }
        }

        // Find each player with that leading win total
        for (Player player : players) {
            if (player.getWins() == highestWins) {
                winners.add(player);
            }
        }

        // Announce the tournament winner(s)
        if (winners.size() == 1) {
            // Announce 1 winner
            System.out.println("Tournament winner, with " + highestWins + " wins: " + winners.getFirst().getName());
        } else {
            // Announce all tied winners
            System.out.println("Tournament winners, with " + highestWins + " wins each:");
            for (Player winner : winners) {
                System.out.println(winner.getName());
            }
        }
    }

    /**
     * Takes the returned winner of a battle between two Player objects, prints the winner to console, and increments
     * their win counter.
     *
     * @param player1 The first Player object participating in the battle.
     * @param player2 The second Player object participating in the battle.
     */
    private void playMatch(Player player1, Player player2) {
        Player winner = runBattle(player1, player2);
        declareBattleWinner(winner);
        winner.addWin();
    }

    /**
     * Runs a battle between two Player objects and returns the winning Player.
     *
     * @param player1 The first Player object participating in the battle.
     * @param player2 The second Player object participating in the battle.
     * @return The winning Player object.
     */
    private Player runBattle(Player player1, Player player2) {
        // Initialize a new instance of Random
        Random r = new Random();

        System.out.println("------- Let the battle begin! ------------\n");

        // Reset characters' healths to their base amounts
        player1.setHealth(player1.getBaseHealth());
        player2.setHealth(player2.getBaseHealth());

        // Pull data into variables for the player1 character
        String player1Name = player1.getName();
        String player1WeaponName = player1.getWeapon().getName();
        int player1WeaponDamage = player1.getWeapon().getDamage();

        // Pull data into variables for the player2 character
        String player2Name = player2.getName();
        String player2WeaponName = player2.getWeapon().getName();
        int player2WeaponDamage = player2.getWeapon().getDamage();

        // Call method to introduce characters
        introduceCharacters(player1, player2);

        // Counter variable to determine who attacks
        int i = 0;

        // While both players are alive, use weapon and health data to carry out turn-based attacks
        // Print the process to the user
        while (player1.getHealth() > 0 && player2.getHealth() > 0) {
            // Player attacks on even turns
            if (i % 2 == 0) {
                int player1Attack = r.nextInt(player1WeaponDamage + 1);
                player2.setHealth(player2.getHealth() - player1Attack);

                System.out.println(player1Name + " attacks " + player2Name + " with their "
                        + player1WeaponName + " for " + player1Attack + " damage");
                System.out.println(player2Name + " HP = " + player2.getHealth());
            } else { // Enemy attacks on odd turns
                int player2Attack = r.nextInt(player2WeaponDamage + 1);
                player1.setHealth(player1.getHealth() - player2Attack);

                System.out.println(player2Name + " attacks " + player1Name + " with their "
                        + player2WeaponName + " for " + player2Attack + " damage");
                System.out.println(player1Name + " HP = " + player1.getHealth());
            }

            i++;
            System.out.println();
        }

        // When a character dies (loop breaks), return the winning Player
        if (player1.getHealth() <= 0) {
            return player2;
        } else {
            return player1;
        }
    }

    /**
     * Prints the end of a battle and declares the winning Player.
     *
     * @param winner The winning Player object.
     */
    private void declareBattleWinner(Player winner) {
        System.out.println(winner.getName() + " wins the battle!");
        System.out.println("\n-------------- Battle End -----------\n");
    }

    /**
     * Introduces each Player at the start of a battle.
     *
     * @param player1 The first Player object in the battle.
     * @param player2 The second Player object in the battle.
     */
    private void introduceCharacters(Player player1, Player player2) {
        player1.battleCry();
        player2.battleCry();
        System.out.println();
    }
}