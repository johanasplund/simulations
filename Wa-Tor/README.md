#Wa-Tor

##The introduction to Wa-Tor by Alexander K. Dewdney
>Somewhere, in a dimension that can only be called recreational at a distance limited only by one's programming prowess, the planet Wa-Tor swims among the stars. It is shaped like a torus, or dougnut, and is entirely covered with water.
>The two dominant denizens of Wa-Tor are sharks and fish, so called because these are the terrestrial creatures they mist closely resemble. The sharks of Wa-Tor eat the fish and the fish of Wa-Tor seem always to be in plentiful supply.[1](http://home.cc.gatech.edu/biocs1/uploads/2/wator_dewdney.pdf)

##Initial parameters
* Initial amount of fish in the ocean
* Initial amount of sharks in the ocean
* Age at which fish breed
* Age at which sharks breed
* Time after which a shark that hasn't found food, dies of starvation

##Rules
* The fish and the sharks are randomly distributed across the grid at the start of the simulation
* The initial age of each fish and shark is randomly chosen between 0 and breeding age
* There can only one animal in an individual cell after each tick, because the shark eats the fish
* Both fish and shark can both move in all available directions, (Up-down, left-right, and diagonally)
* Fish swim in a random direction after each tick
* Sharks hunt, if there is a fish in a bordering cell the shark will eat that fish. If there are no fish surrounding the shark, the shark will move like a fish in a random direction
* If an animal reached breeding age the animal will first move according to the movement rules, then a new animal of the same type is spawned in the cell from which the old animal moved, and the age of both, the parent and the offspring is reset to zero
* If the shark does not find any food before it reaches starvation age, it dies and disappears from the grid. If it fins food the starvation timer is reset to zero

##Possible results
* A perfect balance between fish and sharks, which increase and decrease but never become extinct
* Disappearance of sharks
* Extinction of both species

##Output
The grid is represented graphically using PyGame

##ToDo
* Make fish more intelligent: 
	* Let them sense sharks (with a configurable probability) in a configurable distance (up to 3 cells) and if the sense sharks, let them take evasive action
* Let sharks detect fish in a configurable range (up to 3 cells)
* More tasteful colors 


[1] <http://home.cc.gatech.edu/biocs1/uploads/2/wator_dewdney.pdf>