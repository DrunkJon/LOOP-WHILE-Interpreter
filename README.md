# How to run
1. Open Terminal in the directory containing these files.
2. run "py Main.py" (I wrote this in Python 3.9 so make sure you have the right version.)
3. you should see "{}" and "$>" printed to comandline now and can start coding.

# Syntax
* Variables start with a lowercase "x" followed by a number e.g. "x12"
* Assignemts look like this: "x1 := x2 + 1"
  * you always need to have a variable before and after the ":="
  * followed by either "+" or "-"
  * and either "1" or "0"!
  * the value of a variable can not go below 0! (it won't throw an error if you try) use multiple variables instead to simulate more complex numbers.
* you can start a comment anywhere by starting them with "#" and ending them with a newline
* For-Loops look like this: "loop x2 begin ... end"
  * commands between "begin" and "end" will repeated "x2" amount of times (or whichever variable you provide)
  * value of the loop-variable does not get updated during loop execution, so the variable can be used without side effects from or to the loop
* While-Loops look like this: "while x10 != 0 begin .. end"
  * value of the loop-variable does get updated during loop execution and loop only ends when loop-variable has value 0
  * you can only use "!= 0" and everything else will give you a Syntax-Error
* Named-Blocks get declared like this: "BLOCK n1 n2 begin ... end" and called like this: "x2 := BLOCK x3 x10 end"
  * the name of the block has to be writen in all caps and will be used to reference the block later on.
  * the "n..." are Placeholders for Input values (note that you can't use n0 as an Input Placeholder)
  * if you execute the example above. The Block will create a new inner context where all variables are reset to 0 and Name-Blocks from the outer context can't be called,
    it will then set the value of "x1" in the inner context to the value of "x3" in the outer context (because "x3" is placed in the position of the first placeholder "n1") same with x2 and the outer value of x10.
    it will then execute all the code between begin and end and finaly set the value of "x2" to the value "x0" has in the inner context at the end of the block.
 
See LW_Files/MainFile.txt for example blocks

# Working with the "Shell"
if you run Main.py, it will automatically run the code in MainFile.txt (wich comes with some pre written blocks for convienience) and will then let you interact with the Interpreter from a basic shell.

the code you write in the shell get's storred in a temporary buffer instead of getting executed imediately. This is usefull for writing lines that would not be valid syntax on their on but are together (expecially writting blocks and loops over multiple lines)
To execute the Code in the buffer you just have to write "run" or "r" (you need to do this in a seperate line or your run will be interpreted as regular code and throw a SyntaxError)
If your buffer code contains SyntaxErrors it will not run and the buffer will be deleted, so run your code regularly

everytime Code gets executed, the shell will print the current variable values in form of a python dict.

Correctly executed Code from the shell will be added to the code on MainFile.txt and other executed shell Code. To update MainFile.txt with the new Code you can type "save" or "s" (same rules as run apply) your current buffer code will then be interpreted and if it can be executed without error it (and all the Code you executed this far) will be saved in MainFile.txt

If you want to protect the current MainFile.txt form being overwritten you can simple rename it and save again. You can then rerun it at a later time by renaming it back to MainFile.txt (or playing around in Main.py)

If you're done just write "quit", "q", "close" or "c" and the shell will close (carefull unsaved progress will be lost)
