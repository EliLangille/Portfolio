import java.util.ArrayList;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        // Initialize instances of the CharacterCreator and Battle classes
        CharacterCreator characterCreator = new CharacterCreator(args[0], args[1]);
        Battle battle = new Battle();

        // Array of taunts
        String[] taunts = {
                "You smell like a sewer.",
                "I'll turn you into a pile of bones",
                "Your weapon is pitiful.",
                "Is that all you've got?",
                "I could win this with one hand behind my back.",
                "You should surrender now.",
                "My grandmother could fight better than you.",
                "You don't scare me."
        };

        // Generate an ArrayList of 5 random characters with random taunts
        Random r = new Random();
        ArrayList<Player> players = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            players.add(characterCreator.generatePlayer(taunts[r.nextInt(taunts.length)]));
        }

        // Play a tournament with the 5 Players
        battle.playBracket(players);
    }
}