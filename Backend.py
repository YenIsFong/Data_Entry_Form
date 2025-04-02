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
    start_row = getCurrentRow(ErrorString)
    if start_row is None:
        print("Issue not found")
        return

    print(f"Start row: {start_row}")
    lastrow = len(df)  # Default to the last row if no 'nan' is found
    
    df = pd.read_csv(file_path)

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