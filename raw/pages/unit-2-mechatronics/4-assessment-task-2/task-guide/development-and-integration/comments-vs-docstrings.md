> For the complete documentation index, see [llms.txt](https://gosford-high-school.gitbook.io/9-computing-tech/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://gosford-high-school.gitbook.io/9-computing-tech/unit-2-mechatronics/4-assessment-task-2/task-guide/development-and-integration/comments-vs-docstrings.md).

# Comments vs Docstrings

Comments and docstrings are both ways to add explanatory text to your code, but they serve different purposes and have different formatting conventions. Here's a breakdown of their comparison and contrast:

<details>

<summary>Comments</summary>

* **Structure:** Comments can be single-line (// in C++, # in Python) or multi-line (/\* ... \*/ in C++) depending on the programming language. They are typically placed within the code block they are explaining.
* **Use:** Comments are used to explain specific lines of code, algorithms, or logic choices made by the programmer. They can also be used for temporary notes or reminders to be removed later such as #TODO

</details>

<details>

<summary>Docstrings</summary>

* **Structure:** Docstrings are multi-line strings (usually placed at the beginning of a class, function, or module) that follow specific formatting conventions depending on the language. They use special delimiters like triple quotes (""" ... """) in Python.
* **Use:** Docstrings provide comprehensive explanations for classes, functions, or modules. They typically cover the purpose, usage, parameters, return values, and sometimes even examples. They are meant to be permanent documentation for anyone using the code.

We can also check what a function does, by asking it. This helps maintainability.

```python
def my_function:
"""This is a docstring for MyClass"""
pass

# Print the docstring of MyClass

help(my_function)
print(my_function.__doc__)
```

</details>

| Feature         | Comments                                          | Docstrings                                                               |
| --------------- | ------------------------------------------------- | ------------------------------------------------------------------------ |
| Purpose         | Explain specific code sections                    | Document classes, functions, or modules                                  |
| Placement       | Within the code block being explained             | At the beginning of the definition                                       |
| Formatting      | Language-dependent (usually single or multi-line) | Language-specific formatting conventions (e.g., triple quotes in Python) |
| Permanence      | Can be temporary (for notes/reminders)            | Meant to be permanent documentation                                      |
| Level of Detail | Brief explanations                                | Comprehensive descriptions                                               |

***

## When Should I use a Comment or DocString?

* Use **comments** to explain "**why**" you wrote a specific piece of code.
* Use **docstrings** to document "**what"** a class, function, or module does and "how" to use it.

```python
def create_historic_character(name, era):
    """Create a historical character with a name and era.

    Args:
        name (str): The character's name.
        era (str): The historical era.

    Returns:
        str: A formatted description of the character.
    """
    return f"{name} lived during the {era}."

# Example usage
print(create_historic_character("Leonardo da Vinci", "Renaissance"))
```

The docstring provides an explanation of the function and what it does:

* Function Purpose: To create a historical character with a name and era.
* Arguments: It defines a section titled "Args" that explains each argument taken by the function:
  * name: The name of the historical figure.
  * era: The historical era the figure belongs to.
* Returns: Outlines the that a description of the character is returned from the function.

This docstring improves code readability and maintainability by providing clear explanations for anyone using the **`create_historic_character`** function.
