public enum Weapon {
    // Constants
    AXE("Axe", 15),
    BOW("Bow", 8),
    CLUB("Club", 11),
    CROSSBOW("Crossbow", 13),
    DAGGER("Dagger", 6),
    FLAIL("Flail", 13),
    HALBERD("Halberd", 14),
    KATANA("Katana", 11),
    LONGSWORD("Longsword", 12),
    MACE("Mace", 14),
    SPEAR("Spear", 12),
    STAFF("Staff", 9),
    SWORD("Sword", 11),
    WARHAMMER("Warhammer", 15);

    // Fields
    private final String name;
    private final int damage;

    // Constructor
    Weapon(String name, int damage) {
        this.name = name;
        this.damage = damage;
    }

    // Name getter
    public String getName() {
        return name;
    }

    // Damage getter
    public int getDamage() {
        return damage;
    }
}
