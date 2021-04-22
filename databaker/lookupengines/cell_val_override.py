def cell_val_override(x, y, z):
    # Apply str level cell value override if applicable
    if x in y:
        value = y[x]
    # Apply cell level cell value override if applicable
    elif z in y:
        value = y[z]
    else:
        value = x

    return found_cell, value