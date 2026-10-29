> For the complete documentation index, see [llms.txt](https://gosford-high-school.gitbook.io/9-computing-tech/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://gosford-high-school.gitbook.io/9-computing-tech/unit-3-games-and-simulations/2-modelling-systems/decision-trees/activities.md).

# Activities

### Question 1

In a game, a player can perform a **special move**.

* If the player has **50 or more energy**, the special move is performed.
* If the player has less than 50 energy, the game displays **"Not enough energy"**.

<mark style="background-color:$warning;">**Construct a decision tree**</mark> <mark style="background-color:$warning;"></mark><mark style="background-color:$warning;">that represents the logic used to determine whether the player can perform the special move.</mark>

### Question 2

A player encounters a locked door.

* If the player has a **key**, the door opens.
* If the player does not have a key, the game checks whether the player has **100 or more coins**.
* If they have 100 or more coins, they can **purchase a key and open the door**.
* Otherwise, the door remains locked.
*

<mark style="background-color:$warning;">**Construct a decision tree that represents the possible outcomes when the player interacts with the locked door.**</mark>

<mark style="background-color:$warning;">Your decision tree should show</mark> <mark style="background-color:$warning;"></mark><mark style="background-color:$warning;">**both decisions**</mark> <mark style="background-color:$warning;"></mark><mark style="background-color:$warning;">and all possible outcomes.</mark><br>

### Question 3

A player encounters an enemy in a game.

The game first checks whether the player's **health is greater than 0**.

* If the player's health is 0 or less, the player **loses the game**.
* If the player is still alive, the game checks whether the enemy's health is **greater than 0**.
  * If the enemy's health is 0 or less, the player **wins the encounter**.
  * Otherwise, the game checks whether the player's health is **greater than the enemy's health**.
    * If it is, the game displays **"You have the advantage"**.
    * Otherwise, the game displays **"Enemy has the advantage"**.

<mark style="background-color:$warning;">**Construct a decision tree that represents the logic used by the game when the player encounters an enemy.**</mark>

<mark style="background-color:$warning;">**Your decision tree should:**</mark>

* <mark style="background-color:$warning;">Begin with the first condition</mark>
* <mark style="background-color:$warning;">Show each subsequent decision in the correct order</mark>
* <mark style="background-color:$warning;">Include every possible branch</mark>
* <mark style="background-color:$warning;">Include a clear outcome at the end of every branch</mark>
