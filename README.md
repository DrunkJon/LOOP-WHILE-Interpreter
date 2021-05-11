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
* For-Loops look like this: "loop x2 begin ... end"
  * commands between "begin" and "end" will repeated "x2" amount of times (or whichever variable you provide)
  * value of the loop-variable does not get updated during loop execution, so the variable can be used without side effects from or to the loop
* While-Loops look like this: "while x10 != 0 begin .. end"
  * value of the loop-variable does get updated during loop execution and loop only ends when loop-variable has value 0
  * you can only use "!= 0" and everything else will give you a Syntax-Error
* Named-Blocks get declared like this: "BLOCK n1 n2 begin ... end" and called like this: "x2 := BLOCK x3 x10 end"
  * the name of the block has to be writen in all caps and will be used to reference the block later on.
  * the "n..." are Placeholders for Input values (note that you can't use n0 as an Input Placeholder)
  * if you execute the example above. The Block will create a new inner context where all variables are reset to 0 and Name-Blocks from the outer context cant't be called,
    it will then set the value of "x1" in the inner context to the value of "x3" in the outer context (because "x3" is placed in the position of the first placeholder "n1")
    it will then execute all the code between begin and end and finaly set the value of "x2" to the value "x0" has in the inner context at the end of the block.
 
See LW_Files/MainFile.py for example blocks
