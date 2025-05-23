"""This program is designed to generate a random creature type from magic the gathering."""

__author__ = "Avery Cloutier"
__version__ = "0.2.0"

import random
import os

creature_types = []
with open("creature_types.txt", "r", encoding="utf-8") as file:
    for line in file:
        creature_types.append(line.strip())

continue_generating = True

while continue_generating:
    user_input = input("Generate creature type? (yes/no) ").strip().lower()
    if user_input == "yes":
        chosen_creature = random.choice(creature_types)
        print(chosen_creature)  # Print to the console

        with open("generated_creatures.txt", "a", encoding="utf-8") as output_file:
            output_file.write(chosen_creature + "\n")  # Write to file

    elif user_input == "no":
        if os.path.exists("generated_creatures.txt"):
            os.remove("generated_creatures.txt")
        continue_generating = False
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
