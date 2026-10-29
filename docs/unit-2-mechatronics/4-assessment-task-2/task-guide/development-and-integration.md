# Development and Integration

!!! info "Learning Intention"

    * Design and implement modular programs (code) with functions for mechatronic and/or automated systems
    * Build a mechatronic system using the preferred design and code in a general-purpose programming language
    * Apply selected algorithms and data structures for mechatronic or automated systems



!!! success "Success Criteria"

    * I can create modular code with functions to control a system's inputs and outputs.
    * I can build and program a system to complete the challenge using my designed code.
    * I can apply suitable algorithms and data structures to effectively control a system.



## Development

Typically when we develop software, we may start by working on the mainline algorithm, then creating the subroutines separately. This allows us to work on our main flow and functions separately.

### Decomposition

**Decomposition** in software design is the process of breaking down a complex system into smaller, more manageable components. Let's take a text-based adventure game for example. Developing our mainline algorithm in `main.py` and our subroutines in a different module such as `actions.py` allows us to narrow our focus on different elements of the project.

`main.py` would include the main user interface and may be developed first. The first rendition may look something like the following:

```python title="main.py"
def main():
    print("Welcome to the Adventure Game!")
    print("A wild creature appears! What do you do?")
    print("1. Fight")
    print("2. Run away")
    
    choice = input("Enter your choice (1, 2, or 3): ")
    
    if choice == "1":
        print('Fight function Here')
    elif choice == "2":
        print('Run away function here')
    else:
        print("Invalid choice. Please restart and pick a valid option.")

if __name__ == "__main__":
    main()
```

The above sets out how the UI will function, but so far only demonstrates that the user interface works.&#x20;

Now, let's look at another module, `actions.py`, where we'll put the functions.

```python title="actions.py"
def fight():
    """
    Function to handle the fight action.
    This could include various logic for fighting a creature.
    """
    print("You chose to fight the creature!")
    # Add more fight logic here as needed
    print("You engage in battle with the creature.")
    # Example of more details
    print("The creature is strong, but you're stronger!")

def run_away():
    """
    Function to handle the run away action.
    This could include logic for successfully running away or failing to escape.
    """
    print("You chose to run away!")
    # Add more run away logic here as needed
    print("You turn and flee from the creature.")
    # Example of a scenario where running away fails
    print("Unfortunately, the creature is too fast! It catches up with you!")
```

The beauty of this is that in the above, we can **test** the run\_away and fight functions in the actions.py  module **prior** to using them in the main user interface, and we can test the user interface thoroughly without needing to run through all the functions.

## Integration

Whilst your program is **unlikely** to require this step, it is an important step in the process of software development.

Once we have developed our mainline routine (`main.py`) and our subroutines (`actions.py`), we need to bring the subroutine into the main routine. We also need to ensure **both files are in the same folder.**&#x20;

So let's see an example of integration into our `main.py` file now:

```python title="main.py"
# We could also just type "import actions" to get all functions
# "from actions import *" to get all functions as well
from actions import fight, run_away 

def main():
    print("A wild creature appears! What do you do?")
    print("1. Fight")
    print("2. Run away")
    
    choice = input("Enter your choice (1, 2, or 3): ")
    
    if choice == "1":
        fight()  # Calls the fight function from actions.py
    elif choice == "2":
        run_away()  # Calls the run_away function from actions.py
    else:
        print("Invalid choice. Please restart and pick a valid option.")

if __name__ == "__main__":
    main()

```

## For Your Task

Again, as you are already importing modules, **development and integration** are kind of the same step, but you are **encouraged** to use subroutines effectively even if they are just stored at the top of your program.&#x20;
