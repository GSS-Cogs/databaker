import logging

def override_looked_up_cell(found_cell, cellvalueoverride):
    str_override_applied = False 
    cell_override_applied = False

    # Apply str level cell value override if applicable 
    if found_cell.value in cellvalueoverride: 
        str_override_applied = True
        value = cellvalueoverride[found_cell.value] 
    
    # Apply cell level cell value override if applicable 
    elif found_cell._cell in cellvalueoverride:
        cell_override_applied = True 
        value = cellvalueoverride[found_cell._cell] 
        
    # No overrides applied 
    else: 
        value = found_cell.value

    if str_override_applied and cell_override_applied: 
        logging.warning(f'''Both a str (cellvalueoverride) and cell level (AddCellValueOverride) 
        override is being applied to cell {found_cell}. This should rarely or never be necessary 
        and can lead to confusing and difficult to debug behaviour.''')
        
    return found_cell, value