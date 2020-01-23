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

### Attacking
- If space in front of player is empty, move forward
- If not, think of other possibilities:
    - Calculate pressure exercised towards each teammate
    - Calculate distance to teammate (passing difficulty)
    - Calculate possibilities of scoring when shooting (distance to goal)
    - Take decision that maximizes scoring potential
- If pass is unsuccesful, give possession to next closest oponent, start again

### Defending
- If opponent in my same row has moved forward:
    - If he's in my own half, step forward, else wait
- If opponent in a row next to mine has moved forward and there's no 
    teammate on his row:
    - If he's in my own half, step in his row
    - If I'm marking nobody, step in his row
    - Else wait
- Else (opponent has passed or I'm far from the ball's row):
    - If I'm marking nobody and there's someone unmarked in my closest vicinity
        (radio: 2), mark that someone
    - Else step back
