# IPO Charts

!!! info "Learning Intention"

    Use program-development support tools, including Input Process Output (IPO) charts/diagrams, decision trees, flowcharts and structured English/pseudocode, in the development of a game or simulation

    Develop appropriate supporting documentation in a program to ensure it is easy to read, understand and maintain

    Create a record of project development demonstrating iterative design and evaluation


!!! success "Success Criteria"

    I can develop IPO charts to plan a particular process in a game design scenario.

    I can correctly identify inputs, processes and outputs in a game design scenario.


An IPO chart describes a process using three stages: **Input**, **Process** and **Output**. It is useful for identifying what information a particular part of a program receives, what the program does with that information, and what result it produces. IPO charts are commonly used during system design because they provide a simple way of planning a process before writing code.

## Input

An input is information provided to the process. In a game, an input could be a player's button press, a selected option, a value retrieved from a data store, or information about an object in the game world.

The important point is that the input is information being provided to the process, rather than simply the physical device that produced it. For example, when a player presses a controller button, the relevant input to the software is the button press or command.

## Process

The process describes what the system does with the input. This might involve calculations, comparisons, searches, updates or decisions.

For example, a game could receive a player's selected character and then check that character's available abilities. The processing is the work the software performs to turn the input into a result.

## Output

The output is the information or result produced by the process. An output could be an updated score, a message, a new position, a changed game state or information displayed to the player.

An output does not have to be something displayed on the screen. It could also be information sent to another part of the program or saved for later use.

## Example: Purchasing an Item in a Game

Consider a game that allows a player to purchase an item:

| Input                            | Process                                                                | Output                                                             |
| -------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Item selected                    | Check the item's price against the player's available coins            | Updated inventory                                                  |
| Player's current number of coins | If the purchase is valid, update the player's inventory and coin total | <p>New coin total</p><p></p><p>Message confirming the purchase</p> |

## Using IPO Charts

IPO charts are useful because they encourage developers to think about the boundaries of a process. You should be able to distinguish between an input and the device used to provide it, and between an output and the device used to display or produce it.

For example:

* A keyboard is an input device, but **"player presses the W key"** is an input to a movement process.
* A monitor is an output device, but **"updated player position displayed"** is an output.

IPO charts also connect closely to programming. Once the inputs, processing and outputs have been identified, the processing can be translated into pseudocode or program code. This makes the IPO chart a useful planning tool rather than simply a diagram to complete after the program has already been designed.
