import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

// A class to create battle characters
public class CharacterCreator {

    // Fields (immutable once initialized)
    private final String namesFilePath, titlesFilePath;

    // Constructor
    public CharacterCreator (String namesFilePath, String titlesFilePath) {
        this.namesFilePath = namesFilePath;
        this.titlesFilePath = titlesFilePath;
    }

    // Generates a new Player object using randomized data and a given taunt string
    public Player generatePlayer(String taunt) {
        // Initialize new instance of Random
        Random r = new Random();

        // Generate character data
        String name = generateName();
        int health = r.nextInt(25, 41); // 25-40 HP
        Weapon weapon = generateWeapon();

        // Create and return a Player object using the generated character data
        return new Player(name, health, weapon, taunt);
    }

    // Generates a random character name and title from text files
        /* Note: Can implement a new method for pulling from files in the future */
    private String generateName() {
        // Parse names.txt file, append data to an ArrayList
        ArrayList<String> names = new ArrayList<>();
        try {
            File namesFile = new File(namesFilePath);
            Scanner nameScanner = new Scanner(namesFile);
            names = new ArrayList<>();
            while (nameScanner.hasNextLine()) {
                String name = nameScanner.nextLine();
                names.add(name);
            }
        } catch (FileNotFoundException e) {
            System.out.println("names.txt not found");
        }

        // Parse titles.txt file, append data to an ArrayList
        ArrayList<String> titles = new ArrayList<>();
        try {
            File titlesFile = new File(titlesFilePath);
            Scanner titleScanner = new Scanner(titlesFile);
            while (titleScanner.hasNextLine()) {
                String title = titleScanner.nextLine();
                titles.add(title);
            }
        } catch (FileNotFoundException e) {
            System.out.println("titles.txt not found");
        }

        // Initialize a new instance of Random
        Random r = new Random();

        // Randomly select a name and title from the parsed text files
        String randomName = names.get(r.nextInt(names.size()));
        String randomTitle = titles.get(r.nextInt(titles.size()));

        // Return formatted name + title
        return randomName + " " + randomTitle;
    }

    // Randomly generate weapon data from the Weapon enum
    private Weapon generateWeapon() {
        // Initialize new Random object
        Random r = new Random();
        // Initialize Weapon array to hold the values of the Weapon enum
        Weapon[] weaponsList = Weapon.values();
        // Return a random weapon from the above array
        return weaponsList[r.nextInt(weaponsList.length)];
    }
}