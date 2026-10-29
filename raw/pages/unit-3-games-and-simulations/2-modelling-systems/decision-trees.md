> For the complete documentation index, see [llms.txt](https://gosford-high-school.gitbook.io/9-computing-tech/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://gosford-high-school.gitbook.io/9-computing-tech/unit-3-games-and-simulations/2-modelling-systems/decision-trees.md).

# Decision Trees

{% hint style="info" %}

## Learning Intention

Use program-development support tools, including Input Process Output (IPO) charts/diagrams, decision trees, flowcharts and structured English/pseudocode, in the development of a game or simulation

Create and modify algorithms and code that use branching and iteration, and represent them diagrammatically and in English

Develop appropriate supporting documentation in a program to ensure it is easy to read, understand and maintain

Create a record of project development demonstrating iterative design and evaluation
{% endhint %}

{% hint style="success" %}

## Success Criteria

I can plan and represent decisions in a game system using a decision tree

I can represent decision making in a range of game design scenarios.
{% endhint %}

A decision tree is a representation of decisions made by a system. It begins with a question or condition and branches into different possible paths depending on the result. Each path eventually leads to an outcome. Decision trees are useful in games because many gameplay systems need to respond differently depending on the current situation.

A decision in a game is normally based on a condition that can be evaluated. For example, a game might need to determine whether a player has completed a mission, whether an item is available, whether a character has enough energy to perform an action, or whether an enemy is within a particular distance. The condition produces different possible outcomes, which are represented as branches.

Consider a game in which a player approaches a locked research facility. The game might first check whether the player has the access card. If they do, the game could then check whether the facility's security system is active. Depending on the answers, the player might be allowed inside, required to disable the security system, or prevented from entering. A decision tree makes these different paths visible and allows the developer to check whether every possible situation has been considered.

The branches of a decision tree represent the possible results of a decision. For a simple condition, these might be "Yes" and "No", although more than two outcomes are possible. The final result of following a series of branches is an outcome. An outcome might be an action performed by the game, a message displayed to the player, a change to the game state or another decision that needs to be evaluated.

Decision trees are particularly useful for planning game logic because they make complex choices easier to see. Without a clear representation, developers can accidentally forget an outcome or create contradictory conditions. By following each branch from the beginning to an outcome, the developer can test whether the logic accounts for all relevant situations.

Decision trees can also be translated into pseudocode. A branch asking whether a player has enough energy could become an `IF` statement. If the condition is true, the program performs one action; otherwise, it performs another. For example, if a player has enough energy, the game could allow a special move; otherwise, it could display a message explaining that the move cannot currently be performed.

When creating a decision tree, you should make sure that:

* Each decision is actually a question or condition.
* The branches represent possible answers.
* The outcomes clearly describe what the system does next.
* The decision tree represents the logic of the system rather than simply listing a series of unrelated actions.

### Temperature and Car Purchase Examples

<figure><img src="https://1678667815-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FfhjLkhyTe1IYhZcpt4nX%2Fuploads%2FhJ3u0saETKTwv49ACzav%2Fimage.png?alt=media&amp;token=f80743fb-25be-4e9b-9091-7cc52b1bc9c8" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}

## Note about the Car Purchase

The car purchase is straight out of the course notes, however, could be simplified quite easily (having type = SUV twice seems a bit silly, for instance).&#x20;
{% endhint %}

### Video Game Example

> A player encounters a locked treasure room.
>
> * If the player has a **key**, they can enter.
> * If they don't have a key but have **50 or more coins**, they can purchase access.
> * Otherwise, they cannot enter the room.

```
                Does player have a key?
                   /              \
                YES                NO
                 |                  |
            Enter room        Does player have
                              50+ coins?
                              /           \
                            YES            NO
                             |              |
                      Purchase access     Cannot
                      and enter room      enter
```
