def cell_val_override(found_cell, cellvalueoverride):
#    # Apply str level cell value override if applicable
    if found_cell.value in cellvalueoverride:
        value = cellvalueoverride[found_cell.value]
    # Apply cell level cell value override if applicable
    elif found_cell._cell in cellvalueoverride:
        value = cellvalueoverride[found_cell._cell]
    else:
        value = found_cell.value

    return found_cell, value