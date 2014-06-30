Cellular Automata simulation of a forest
==========
This is a simulation of a forest populated by trees, lumberjacks, bears and the occasional forest fire. 

Erik Sjöström

How it works, (1 iteration = 1 month)
---------
### The Grid
  * The grid is an NxN square
  * 50% of the grid will be populated by trees at the start of the simulation.
  * 10% of the grid will be populated by lumberjacks at the start of the simulation.
  * 2% of the grid will be populated by bears at the start of the simulation.

### Trees
There are three types of trees
  * Sapling, the mini tree. A sapling turn into a normal tree after 12 months.
  * Normal tree. Has a 10% chance to spawn a sapling at an adjacent cell.
  * If a normal tree survives for 120 months it turns into an elder tree, which has a 20% chance to spawn a sapling. 

### Lumberjacks
Every month the lumberjack takes a random walk for a maximum of three cells. For every cell it reaches it checks if the cell contains a tree. If the cell does contain a tree the lumberjack cuts it down and stays in that cell for the rest of month. If it does not contain a tree, the lumberjack
tries to move on to the next cell unless it is at the end of its walk (third cell). For every tree a lumberjack cuts down, lumber is collected.
A normal tree is worth 1 lumber and an elder tree is worth 2 lumber. 

#### Hiring and firing
At the end of a year (12 months), all the lumber is counted up and compared to the amount of working lumberjacks according to
`amount = (lumber/(scale_factor) - lumberjacks)`, if amount is positive that many lumberjacks are hired, otherwise that many lumberjacks are fired.

### Bears
Every month each bear takes a random walk for a maximum of five cells. If a bear runs into a lumberjack, it brutally savages the lumberjack and sends it out of
the simulation, and stays in that cell for the rest of the month.

#### Animal control
If there is one or more accidents during a year, one bear is taken around the back of the simulation. If no accidents is encountered during a year, a new bear is spawned. 

### Forest fires
A forest fire happens during one single month, so during a forest fire, only one month elapses.

There are some factors which determine the spread of the fire: Chance of catching fire and duration of fire, these differ between trees.
- Sapling: Has a 1/8 chance to catch fire and burns for 1 iteration
- Tree: Has 1/4 chance to catch fire and burns for 2 iterations
- Elder tree: Has 1/2 chance to catch fire and burns for 4 iterations

After the fire, the ground remains scorched for 5 years, until any saplings can spawn on the ground.


Fun keyboard commands
---------
- F = Starts a fire at random cell containing a tree
- K = Removes 50 lumberjacks from the simulation
- B = Spawns 100 new bears
- L = Spawn 50 lumberjacks

TODO
---------
* The lumberjacks are currently taking over, this should probably be fixed
* It seems like there are some stray dots of color, look into this

Credit
---------
Credit goes to reddit user /u/Coder_d00d for coming up with the idea as a challenge in /r/dailyprogrammer
