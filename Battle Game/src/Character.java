public abstract class Character {

    // Fields
    private final String name;

    private final int baseHealth;
    private final Weapon weapon;

    private int health;

    // Constructor
    public Character (String name, int baseHealth, Weapon weapon) {
        this.name = name;
        this.baseHealth = baseHealth;
        this.weapon = weapon;
    }

    // Initialize battleCry() for Player subclass
    public abstract void battleCry();

    // Getters
    public String getName() {return name;}

    public int getHealth() {return health;}

    public int getBaseHealth() {return baseHealth;}

    public Weapon getWeapon() {return weapon;}

    // Health setter
    public void setHealth(int newHealth) {this.health = newHealth;}
}

