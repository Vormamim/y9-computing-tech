# Activities

### Question 1

A school canteen system allows students to place food orders.

Students provide their **student details** and **order details** to the system. The system checks the student's details using the **Student Data** data store and processes the order.

The system sends an **order confirmation** to the student. The order is stored in the **Orders** data store.

<mark style="background-color:#fde68a;">**Construct a Level 1 Data Flow Diagram (DFD) for the school canteen system.**</mark>

### **Question 2**

An online gaming tournament system allows players to register for tournaments and compete in matches.

A **Player** provides **registration details** to the **Manage Registration** process. The process stores the player's information in the **Player Data** data store.

Players can request a list of available tournaments. **Manage Tournaments** retrieves **Tournament Information** from the **Tournament Data** data store and sends the available tournaments to the Player.

When a player joins a tournament, **Tournament Selection** is sent to Manage Tournaments. The player's registration is then added to the tournament.

During a match, the Player sends **Game Results** to the **Manage Results** process. Manage Results stores the results in the **Tournament Results** data store.

The system can retrieve tournament results and send **Leaderboard Information** to the Player.

<mark style="background-color:#fde68a;">**Construct a Level 1 Data Flow Diagram (DFD) for the online tournament system.**</mark>
