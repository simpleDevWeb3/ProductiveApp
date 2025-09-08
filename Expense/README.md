<h1 align="center">Expenses Tracker and GPA Calculator Application</h1>

## Table of Contents 
- [Install the required dependencies](#install-the-required-dependencies)
- [How to run the application](#how-to-run-the-application)
- [Application menu](#application-menu)
- [Expenses tracker application](#expenses-tracker-application)
- [GPA Calculator application](#gpa-calculator-application)

## Install the required dependencies
- type the command below in command prompt:
    ```
    pip install matplotlib
    ```
    
## Run the application

A. Visual Studio Code:
   ```
    - open visual studio code make sure have install python extension then only debug the python file.
   ```

B. Command Prompt:
   ```
    - open the assignment.py file folder
    - right click the folder, choose command prompt
    - enter command "python main.py"
   ```

C. Anaconda Prompt:
```
     - please make sure downloaded Anaconda Distribution from https://docs.anaconda.com/anaconda/getting-started
     - open anaconda prompt 
     - enter the right path (foward): cd "folder name"
     - enter the right path (backward): cd..
     - enter command "python main.py" to execute the python file
```

## Expenses tracker application

- First of all, need to make sure all the file is downloaded.

1. Add Expense:
   ```
    - click the add budget, it will show the add expenses page 
    - then, fill in all the relevant information needed 
    - after that press the save button and it will save it 
    - back button can let you back to expenses tracker menu page
   ```
   
2. Show Expenses:
   ```
    - click the view expenses button it will show the expenses that you have enter just now
    - it will show all the expenses detail. For example, Date, Category, Amount, Description
    - you can delete selected expense if selected the expenses wanted to delete
    - for delete all button, all the record will be deleted
    - back button can let you back to expenses tracker menu page
   ```

3. Set Budget:
   ```
   - click the set budget, it will show the set budget page 
   - then, enter the budget you want to save or use the dropdown list to choose amount faster
   - after press save, it will save the amount
   - back button can let you back to expenses tracker menu page
   ```

4. Check Budget:
   ```
    - click the check budget button it will show all the budget detail inside
    - it show the budget set just now
    - it also show the total spend in the expense record
    - based on this two, it will prompt a message to let user know if the total spent is within the budget
    - back button can let you back to expenses tracker menu page
   ```

5. Analysis:
    ```
    - click the analysis button it will show the summary expense and budget page 
    - then, it will show your total expenses amount, budget amount and a expenses pie chart based on the category
    - back button can let you back to expenses tracker menu page
    ```

