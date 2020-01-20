# Agent based simulation - football

I've recently grown interested in agent based simulation. After doing some 
basic exercises (found in g0_test) I want to fully test my recently acquired
knowledge. 

I will try to generate a football game. For that, each agent will represent a 
player. By coding up some basic rules I will try to replicate a player's 
decision making during a football game. My goal is to make the rules more
and more complex everytime so we can get closer (while still probably staying
light years away) to a real game. Let's see how it goes.

Some examples that I have thought of as to now:

- If space in front of player is empty, move forward
- If not, think of other possibilities:
    - Calculate pressure exercised towards each teammate
    - Calculate distance to teammate (passing difficulty)
    - Calculate possibilities of scoring when shooting (distance to goal)
    - Take decision that maximizes scoring potential
- If pass is unsuccesful, give possession to next closest oponent, start again
