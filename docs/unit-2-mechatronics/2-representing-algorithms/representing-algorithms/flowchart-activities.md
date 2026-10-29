# Flowchart Activities

!!! warning "Please Read:"

    These activities are not marked as part of your assessment, they are just to get you used to creating algorithms.


Before we start, we need to consider **what software to draw a flowchart in.**

You are welcome to use **Flowgorithm** if you enjoyed that in Year 7, **OR,** you can use Excalidraw:

[:material-link-variant: https://excalidraw.com/](https://excalidraw.com/)

**Note:** For Excalidraw, you will need to go to **Library** in the top right hand corner, then add flowchart shapes to your library to get a **parallelogram** for **input** and **output**.&#x20;

## Activities

1. **Create a flowchart based on the following algorithms (one at a time):**
   1. ```
      BEGIN 
          read (num1)
          read (num2)
          Set total to num1 + num2
          Set average to total / 2
          Display average
      END
      ```
   2. <pre><code><strong>BEGIN
      </strong>    read (score)
          IF score >= 85
              Display "Excellent"
          ELSEIF score >= 70
              Display "Good"
          ELSEIF score >= 50
              Display "Average"
          ELSE
              Display "Fail"
          ENDIF
      END
      </code></pre>
   3. ```
      BEGIN
          read (N)
          Set totalSum to 0
          FOR i = 1 to N
              Add i to totalSum
          NEXT i
          Display totalSum
      END
      ```
2. **Write pseudocode AND produce a flowhcart for each of the following Python programs:**
   1. ```python
      age = int(input("Enter your age: "))


      if age < 13:
          print("You are a Child.")
      elif 13 <= age <= 19:
          print("You are a Teenager.")
      elif 20 <= age <= 64:
          print("You are an Adult.")
      else:
          print("You are a Senior.")
          
          
      ```
   2. <pre class="language-python"><code class="lang-python"><strong>def calculate_factorial(num):
      </strong>    factorial = 1
          for i in range(1, num + 1):
              factorial *= i
          return factorial
          
      number = int(input("Enter a number: "))

      factorial_result = calculate_factorial(number)

      print(f"The factorial of {number} is {factorial_result}.")
      </code></pre>
