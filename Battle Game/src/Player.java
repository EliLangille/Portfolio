// A Player extension of the Character class which adds a taunt for the Character
public class Player extends Character {
    // Fields
    private final String taunt;
    private int wins;

    // Constructor
    public Player(String name, int baseHealth, Weapon weapon, String taunt) {
        super(name, baseHealth, weapon);
        this.taunt = taunt;
        this.wins = 0;
    }

    // Wins getter
    public int getWins() {return wins;}

    // Wins incrementer
    public void addWin() {this.wins++;}

    // Overrides the battle cry to use the Player's taunt
    @Override
    public void battleCry() {
        System.out.println(this.getName() + ": \"" + this.taunt + "\"");
    }
}
