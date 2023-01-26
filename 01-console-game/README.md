# Console Game

To familiarise yourself with common control flows, building a command line game is a great start. In general, it should
contain a few major modules with the following game idea:

You are an adventurer who explores a dungeon. The dungeon has any number of rooms, from a few rooms to even hundreds if
you dive deep enough. The overall goal is to survive and climb deeper as you go. The rooms are simple rectangle shaped
with up to 4 pathways leading in and out from them. Within the rooms there could be obstacles, puzzles, or enemies.

The whole layout of the map and the rooms in a 2D grid, where the player can move with the arrow keys. The player has a
leveling system that increases its health and attack damage. When defeating enemies the player gains experience, when
opening chests items could be obtained.

### Feature-set:

* Procedural floor generation
* Console Rendering of 2D grid movement with arrow keys
* Turn-based fight system
* Leveling system

### Procedural floor generation

For each floor the game should generate 3-12 rooms that are connected through their edges. A room must have at least one
edge connected, but up to four should be allowed. The connected edges should have a door that may or may not be closed
and require an item to open. The rooms are determined in type, with the following options:

* Fight room: One to Three enemies spawned at random locations, away from the doors
* Loot room: One to Three chests spawned in the middle of the room, which can contain:
    * Key to open a locked door
    * Health and Defence Potions
* Staircase room: A way to go up or down in the dungeon. There is always one down and one up generated.

For the layout, a path must be provided between the Staircases which should not be blocked by doors.

### Console Rendering

For each turn, the game should clear the console and render the active room and entities with ASCII characters.
This does not need to be very big, a 16:9 grid is plenty. The UI should contain a few elements:

* Top-Left: Health and Level of the player
* Top-Right: The Level of the dungeon
* Bottom-left: Choice options for the tile the player standing on
* Bottom-Right: Experience meter

### Fight System

The enemies will close onto the players, and once meet the player is forced to fight, in a turn-based system with the
following actions:

* Attack: Always available but leaves the player unprotected.
* Defend: Blocks the next attack for the player power level.
* Use Item: Can replenish health or apply further defence.
* Flee: Only available when the enemy us bellow 30% health.
* Skip: Do nothing, skip the turn.

The enemies would choose their action randomly or with a set pattern between:

* Attack: Attacks the player with the floor power level.
* Defend: Blocks an attack from the player for the floor power level.
* Pass: Does nothing, skips it turn.

### Leveling System

The players should be able to level up from 1 to any infinity; where with each level the requirement would exponentially
grow. However, the power level of the enemies would grow linearly. The base statistics are:

* Player: Power 3, scaling: `Power + Power * ( Level * 0.75 )`
* Enemies: Power 3, scaling: `FLOOR( Floor * 1.75 + 3 )`

The power means the health, the attack damage, and the defence block all in one. When a player levels up,
it should fill up their health bar.