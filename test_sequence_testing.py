'''
ToDo:
  1) polish abort functionality
  2) implement function/action definiton
            * complete the "read_opd_2()" like functions
  3) implement test sequence functions into gui
            * complete the "parse_uart_data()" like functions
'''


import time

def start_count():
    print("Executing Start_Count")

def read_opd_02():
    print("Executing Read_OPD_02")

def read_fpd_02():
    print("Executing Read_FPD_02")
    '''
    data = tel.get_data()
    return data[opd]
    '''

def read_epd_01():
    print("Executing Read_EPD_01")

def fv_02():
    print("Executing FV_02")
    '''
    tel.open_valve(fv_o2)
    tel.send_data()
    '''

def nv_02():
    print("Executing NV_02")

def fv_03():
    print("Executing FV_03")

def blp_abort():
    print("Executing BLP_Abort")

# Function mapping
task_map = {
    "Start_Count": start_count,
    "Read_OPD_02": read_opd_02,
    "Read_FPD_02": read_fpd_02,
    "Read_EPD_01": read_epd_01,
    "FV_02": fv_02,
    "NV_02": nv_02,
    "FV_03": fv_03,
    "BLP_Abort": blp_abort
}

def parse_uart_data(data):
    time_list = []
    function_list = []
    action_list = []
    limit_list = []
    condition_list = []
    unit_list = []
    oob_list = []
    
    # Find max absolute time value to adjust countdown timing
    max_time = max(abs(entry[0]) for entry in data if entry[0] is not None)
    
    for entry in data:
        if len(entry) < 7:
            continue  # Skip incomplete entries
        
        # Adjust time values so that max_time corresponds to 0
        time_value = max_time - abs(entry[0])
        time_list.append(time_value)
        
        function_list.append(entry[1])
        action_list.append(entry[2])
        limit_list.append(entry[3])
        condition_list.append(entry[4])
        unit_list.append(entry[5])
        oob_list.append(entry[6])

    
    
    return time_list, function_list, action_list, limit_list, condition_list, unit_list, oob_list

def countdown_execution(time_list, function_list, limit_list, condition_list, oob_list):
    start_time = time.time()
    executed = set()
    
    while len(executed) < len(time_list):
        current_time = int(time.time() - start_time)
        
        for i, target_time in enumerate(time_list):
            if target_time == current_time and i not in executed:
                print(f"{30-target_time} seconds remaining: Executing {function_list[i]}")
                
                # Check conditions before executing
                if limit_list[i] != "N/A" and condition_list[i] != "N/A":
                    try:
                        value = 13  # Example input value for testing
                        condition_value = float(condition_list[i])
                        if limit_list[i].startswith("<") and value > condition_value:
                            print(f"Condition met: {value} {limit_list[i]} {condition_value}")
                        elif limit_list[i].startswith(">") and value < condition_value:
                            print(f"Condition met: {value} {limit_list[i]} {condition_value}")
                        else:
                            print(f"Condition not met for {function_list[i]}, triggering OOB: {oob_list[i]}")
                            if oob_list[i] in task_map:
                                task_map[oob_list[i]]()
                            break    
                            #continue  # Skip execution if condition is not met
                    except ValueError:
                        print("Invalid limit or condition value, skipping condition check.")
                
                # Execute function if in map
                if function_list[i] in task_map:
                    task_map[function_list[i]]()
                executed.add(i)
        
        time.sleep(0.1)  # Non-blocking slight delay for efficiency

# Example test data
data = [
    [-30, 'Start_Count', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    [-20, 'Read_OPD_02', 'READ', '<', '15', 'psi', 'BLP_Abort'],
    [-20, 'Read_FPD_02', 'READ', '<', '15', 'psi', 'BLP_Abort'],
    [-20, 'Read_EPD_01', 'READ', '<', '15', 'psi', 'BLP_Abort'],
    [-15, 'FV_02', 'CLOSE', 'N/A', '0', 'N/A', 'BLP_Abort'],
    [-15, 'NV_02', 'OPEN', 'N/A', '0', 'N/A', 'N/A'],
    [0, 'FV_03', 'OPEN', 'N/A', 'N/A', 'N/A', 'N/A']
]

# Extract lists
time_list, function_list, action_list, limit_list, condition_list, unit_list, oob_list = parse_uart_data(data)

# Execute countdown-based function execution
countdown_execution(time_list, function_list, limit_list, condition_list, oob_list)

'''
#does this call the function
for i in range(len(task_map)):
    task_map[function_list[i]]()
'''



