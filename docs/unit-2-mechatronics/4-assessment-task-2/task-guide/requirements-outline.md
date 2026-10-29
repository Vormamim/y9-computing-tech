# Requirements Outline

!!! info "Learning Intention"

    * Specify the functional requirements of a mechatronic or automated system, including stating the purpose of a system, describing use cases and developing test cases of inputs and expected outputs
    * Specify the non-functional requirements of a mechatronic or automated system



!!! success "Success Criteria"

    * I can clearly state the purpose of my mechatronic device design and how the Raspberry Pi PICO can be used to solve the problem.
    * I can develop test cases by identifying inputs (e.g. sensor readings, button presses) and expected outputs (e.g. LED signals, buzzer sounds).
    * I can identify and explain non-functional requirements, such as efficiency, accuracy and response time that impact my microcontroller's performance.



## Writing your Requirements Outline

Work through all of the following to complete your requirements outline:

??? note "Defining the Purpose"

    Write 1-2 sentences on the need / problem you are trying to solve, and 1-2 sentences on your proposed solution.

    !!! info "Example"

        #### The Need

        My family has recently had a baby and needs to keep the nursery between 18 and 22°C. Due to the hot weather over summer and it being a small bedroom, the room can heat up quite quickly  through the middle of the day, and my parents are very tired due to the baby waking them up frequently, and often fall asleep in the living room whilst the baby is sleeping.

        #### Proposed Solution

        I will design an alarm system to put in the living room which will ring a highly annoying song on a buzzer continuously until a button is pressed if the temperature goes below 18°C or above 22°C. Additionally, I will develop an LED system which will show how close the temperature is to being optimal (around 20-21°C).&#x20;


??? note "Identify Key Actions"

    List at least **3-5 specific actions** which your microcontroller needs to perform to complete the task. These should be clear, simple actions like detection, input, output or triggering an event (e.g. sound or lights).

    !!! info "Examples"

        * Buzzer rings quickly if boundary values are exceeded.
        * Green LED lights up if optimal temperature,  red if boundary values exceeded.


??? note "Functional Requirements"

    A functional requirement is the action or behavior the robot needs to perform.

    For each key action, write a **functional requirement** that clearly states **what the robot must do**. These should be written in a clear and concise manner.

    !!! info "Example"

        **Temperature Sensor Input:** If temperature exceeds boundary values (<18°C OR >22°C), buzzer rings continuously.

        **LED Output:** Green LED must light up if temperature is optimal (20-21°C). Yellow LED must light up if temperature is within 1°C of boundary values. Red LED must light up if boundary values exceeded.


??? note "Test Cases"

    For each **functional requirement**, develop **tese cases** for it. A test case is simply an outline of expected function, input and outputs, so that we can test against it later on when developing prototypes.

    * Identify the **inputs** (e.g. sensor data, button presses).
    * Identify the **expected outputs** (e.g. motor movement, sound, display messages).

    !!! info "Example"

        Look at the following table for an example of what a test case looks like.


    <table><thead><tr><th width="217.33343505859375">Test Case</th><th>Input</th><th>Expected Output</th></tr></thead><tbody><tr><td>Temperature too hot</td><td>Temperature sensor reads  > 22°C.</td><td>Red LED lights up, buzzer rings continuously.</td></tr><tr><td>Temperature in high range</td><td>Temperature sensor reads 21-22°C </td><td>Yellow LED lights up, buzzer makes beeps slowly.</td></tr></tbody></table>

    !!! warning "Markdown Formatting a Table"

        I've given you this one for free - copy the following into your Markdown file to create your table. Each empty section is a row.&#x20;


    ```markdown
    | Test Case | Input     | Expected Output   |
    |---------- |---------- |----------------   |
    |           |           |                   |
    |           |           |                   |
    |           |           |                   |
    ```


??? note "Non-Functional Requirements"

    These are requirements that focus on how well the robot will perform in completing the task, rather than the completing of the task itself. Consider the following:&#x20;

    * **Efficiency**
    * **Response Time**
    * **Accuracy**

    !!! info "Example"

        **Response Time** – The robot should react to sensor input within 1 second.
