
import csv
import pandas as pd
file_path = r"C:\Users\768604\Desktop\maint_app\merged_output\COLLATED EVERYTHING.csv"             
df = pd.read_csv(file_path)

def getErrorDict():
    df = pd.read_csv(file_path)
    ErrorDict={}
    for index, row in enumerate(df.values):
        if str(row[0]) != "nan":
            ErrorDict[row[0]]=index
    # print(ErrorDict)
    return ErrorDict

def getErrorList():
    ErrorDict=getErrorDict()
    return list(ErrorDict.keys())

# Get the row index of Error
def getCurrentRow(ErrorString):
    ErrorDict = getErrorDict()
    try:
        return ErrorDict[ErrorString]
    except KeyError:
        print("No Such Issue Found!")
        return None  # or raise a custom exception

def getActionList(ErrorString):
    ActionList=[]
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return

    lastrow = len(df)  # Default to the last row if no 'nan' is found

    for index, row in enumerate(df.values[start_row:], start=start_row):
        # print(index)
        # print(str(row[1]))
        if str(row[1]) == "nan":
            # Add your action here
            lastrow = index
            print(f"Found nan at row: {lastrow}")
            break
        else:
            ActionList.append(str(row[1]))
        
    # print(ActionList)    
    return ActionList

def getLastRowIndex():
    df = pd.read_csv(file_path)
    last_row = df.iloc[-1]  # get the last row
    return last_row.name

def getActionFrequency(ErrorString, ActionString):
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return
    
    print(f"Start row: {start_row}")
    df = pd.read_csv(file_path)
    # Identify the last row using pandas
    RowToChange=None
    for index, row in enumerate(df.values[start_row:], start=start_row):
        # print(f"Index: {index}, Value of row[1]: {row[1]}")
        if str(row[1]) == ActionString:
            RowToChange=index
            print(f'"{ActionString}" found at index: {RowToChange}')
            # row[2]=row[2]+1
            print(row[2])
            # print(row[2]) 
            return row[2]

        elif str(row[1]) == "nan": #idk need to test later
            print("No Action Found!")
            return

def addError(ErrorString, ActionTaken, Frequency):
    try:
        if ErrorString in getErrorList():
            return False
        
        df = pd.read_csv(file_path)
        lastrow = getLastRowIndex()
        print(lastrow)

        emptyrow=["","",""]
        new_row = [ErrorString, ActionTaken, Frequency]  # create a new row
        
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
        rows.insert(lastrow+2, emptyrow)
        rows.insert(lastrow+3, new_row)
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("New action added successfully.")
        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def addNewAction(ErrorString, newActionString,Frequency):
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return

    lastrow = len(df)  # Default to the last row if no 'nan' is found

    for index, row in enumerate(df.values[start_row:], start=start_row):
        print(index)
        print(str(row[1]))
        if str(row[1]) == "nan":
            # Add your action here
            lastrow = index
            print(f"Found nan at row: {lastrow}")
            break
    else:
        print("No nan value found!")
        
    # print("hello")
    new_row = [None, newActionString, Frequency]  # create a new row
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    rows.insert(lastrow+1, new_row)
    
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print("New action added successfully.")
    return True

# addNewAction("Load Head Issue","HELLLOOOOOO",12)

def IncrementActionCount(ErrorString,ActionString):
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return
    
    print(f"Start row: {start_row}")
    df = pd.read_csv(file_path)
    # Identify the last row using pandas
    RowToChange=None
    for index, row in enumerate(df.values[start_row:], start=start_row):
        # print(f"Index: {index}, Value of row[1]: {row[1]}")
        if str(row[1]) == ActionString:
            RowToChange=index
            print(f'"{ActionString}" found at index: {RowToChange}')
            # row[2]=row[2]+1
            df.at[RowToChange, df.columns[2]] += 1     
            # print(row[2]) 
            break

        elif str(row[1]) == "nan": #idk need to test later
            return
        
    df.to_csv(file_path, index=False)

def DecrementActionCount(ErrorString, ActionString):
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return
    
    print(f"Start row: {start_row}")
    df = pd.read_csv(file_path)
    # Identify the last row using pandas
    RowToChange=None
    for index, row in enumerate(df.values[start_row:], start=start_row):
        # print(f"Index: {index}, Value of row[1]: {row[1]}")
        if str(row[1]) == ActionString:
            RowToChange=index
            print(f'"{ActionString}" found at index: {RowToChange}')
            # Decrement the count, but not below 0
            df.at[RowToChange, df.columns[2]] = max(0, df.at[RowToChange, df.columns[2]] - 1)     
            break

        elif str(row[1]) == "nan": 
            return
        
    df.to_csv(file_path, index=False)

def deleteError(ErrorString):
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return

    print(f"Start row: {start_row}")
    lastrow = len(df)  # Default to the last row if no 'nan' is found
    
    # Identify the last row using pandas
    for index, row in enumerate(df.values[start_row:], start=start_row):
        print(f"Index: {index}, Value of row[1]: {row[1]}")
        if str(row[1]) == "nan":
            lastrow = index
            print(f"Last row found at index: {lastrow}")
            break

    if lastrow is None:
        print("No valid last row found. Exiting.")
        return

    # Read the CSV using csv.reader
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Adjust for header if applicable
    header_offset = 1 if reader and isinstance(reader, list) and reader[0] else 0
    start_row += header_offset
    lastrow += header_offset

    # Delete rows from start_row to lastrow (inclusive)
    print(f"Deleting rows from {start_row} to {lastrow}")
    del rows[start_row:lastrow + 1]

    # Write updated data
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("Error deleted successfully.")

def deleteAction(ErrorString, ActionToDel):
    
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return

    print(f"Start row: {start_row}")
    df = pd.read_csv(file_path)
    # Identify the last row using pandas
    RowToDel=None
    for index, row in enumerate(df.values[start_row:], start=start_row):
        # print(f"Index: {index}, Value of row[1]: {row[1]}")
        if str(row[1]) == ActionToDel:
            RowToDel=index
            print(f'"{ActionToDel}" found at index: {RowToDel}')
            break

        elif str(row[1]) == "nan": #idk need to test later
            return
    # print("HELLOE WORLD")
    if RowToDel==None:
        print(f'"{ActionToDel}" Not Found in "{ErrorString}"!')
        return        
    # Read the CSV using csv.reader
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Adjust for header if applicable
    header_offset = 1 if reader and isinstance(reader, list) and reader[0] else 0
    start_row += header_offset
    
    print(f"Deleting rows from {RowToDel}")
    if RowToDel==start_row:
        print("Please delete Entire Error Record instead!")
        return
    else:
        del rows[RowToDel+1]
        
    # Write updated data
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("Error deleted successfully.")

def getlastColumn(ErrorString):
    
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)
    
    for i in range(3, len(df.columns)):
        if pd.isna(df.iloc[start_row, i]):
            # If the cell is NA, return current column
            return i
    return len(df.columns)

def addOrder(ErrorString, OrderList, AdminName):
    """Updates the first available order column starting from column index 3."""
    
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)

    if start_row is None:
        print("Issue not found")
        return

    print(f"Updating row: {start_row}")
    
    columntoupdate=getlastColumn(ErrorString)
    print(f"Updating column: {columntoupdate}")
    
    # Ensure the DataFrame has enough rows
    while len(df) <= start_row + len(OrderList):
        df.loc[len(df)] = [None] * len(df.columns)
    
    # Ensure the DataFrame has enough columns
    while len(df.columns) <= columntoupdate:
        df[columntoupdate] = None
        
        
    column_names = list(df.columns)
    column_names[columntoupdate] = 'Order'
    df.columns = column_names
    for index, item in enumerate(OrderList):
        df.iloc[index + start_row, columntoupdate] = item
    df.iloc[start_row-1,columntoupdate]=AdminName

    # Save the updated DataFrame
    df.to_csv(file_path, index=False)
    print("Order list updated successfully.")
    
def findUserColumn(ErrorString,User):
    
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)
    
    for i in range(3, len(df.columns)):
        if df.iloc[start_row-1, i] == User:
            return i
    return None

# getActionOrderdict(ErrorString): return Dictionary {Action:order}
def getActionOrderdict(ErrorString,User):
    """
    Returns a dictionary of actions and their corresponding orders for a given error and user.
    
    Args:
        error_string (str): The error string to retrieve actions for.
        user (str): The user to retrieve actions for.
    
    Returns:
        dict: A dictionary where keys are actions and values are their corresponding orders.
    """
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)

    if start_row is None:
        print("Issue not found")
        return
    
    lastrow = len(df)  # Default to the last row if no 'nan' is found

    for index, row in enumerate(df.values[start_row:], start=start_row):
        print(index)
        print(str(row[1]))
        if str(row[1]) == "nan":
            # Add your action here
            lastrow = index
            print(f"Found nan at row: {lastrow}")
            break
    else:
        print("No nan value found!")

    # columntoextract starts from 3, if 
    OrderColumn = findUserColumn(ErrorString,User)
    
    Order = df.iloc[start_row:lastrow, OrderColumn].tolist()
    print(Order)
    
    Action=getActionList(ErrorString)
    print(Action)
    
    # Combine the two lists into a dictionary
    ActionOrderDict = dict(zip(Action, Order))
    
    # Sort the dictionary in descending order
    sorted_ActionOrderDict = dict(sorted(ActionOrderDict.items(), key=lambda item: int(item[1])))
    print(sorted_ActionOrderDict)
    
    return sorted_ActionOrderDict
    # extract startrow to lastrow, the User ==  df.iloc[start_row-1,OrderRow]

def getUser(ErrorString):
    df = pd.read_csv(file_path)
    start_row = getCurrentRow(ErrorString)
    
    UserList = df.iloc[start_row-1, 3:getlastColumn(ErrorString)].tolist()
    print(UserList)
    return UserList