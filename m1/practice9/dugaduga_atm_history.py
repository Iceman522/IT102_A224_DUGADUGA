# TODO 1:
# Create view_history().
 
def view_history():
    # TODO 2:
    # Try to open transactions.txt
    # in read mode.
    try:
        with open("transactions.txt", "r") as file:
 
    # TODO 3:
    # Read all lines from the file.
            lines = file.readlines()
 
    # TODO 4:
    # Return the lines to the caller.
        return lines
 
    # TODO 5:
    # Handle FileNotFoundError.
    #
    # If the file does not exist,
    # return an empty list.
    except FileNotFoundError:
        return[]

""" 
######### Learning Signature ######### 
Programmed by: Adrian Paolo V. Dugaduga
Date Submitted: September 4, 2026
 
Program Description: This program defines a function that reads and returns transaction log history from a text file while handling missing file errors gracefully.
Reflection: I learned how to safely read data from external files and use try-except blocks to prevent program crashes when a file does not exist.
AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
    