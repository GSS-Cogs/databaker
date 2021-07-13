import logging

def override_looked_up_cell(found_cell, cellvalueoverride, apply_functions):
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

    for a_func in apply_functions:
        if str_override_applied or cell_override_applied:
            logging.warning(f'''You are applying (via apply=) a function to the dimension 
                header {found_cell} that has already had a cell value override applied to it.
                The cell.value at time this function was applied was {value}.''')
        value = a_func(value)

    return found_cell, value

def unpack_callables(callable_thing_or_tuple_of):
    """
    Where we are passing callables to the HDim apply= keyword, if not none sanity check
    what we've got and make sure we return a tuple of them.
    """
    if not callable_thing_or_tuple_of:
        return ()

    msg = '{} is being passed in via apply= but does not appear to be callable or tuple of callables'

    # If it's a single callable, return it in a tuple
    if not isinstance(callable_thing_or_tuple_of, tuple):
        assert hasattr(callable_thing_or_tuple_of, "__call__"), msg.format(callable_thing_or_tuple_of)
        return tuple([callable_thing_or_tuple_of])

    # If it's already a tuple, make sure everything in it is callable
    elif isinstance(callable_thing_or_tuple_of, tuple):
        for a_hopefully_callable_thing in callable_thing_or_tuple_of:
            assert hasattr(a_hopefully_callable_thing, "__call__"), msg.format(a_hopefully_callable_thing)
        return callable_thing_or_tuple_of

    else:
        raise ValueError('''The argument to HDim(apply=) should either be single callable (eg a function,
            lambda, or a class with a .__call__ method or a tuple of these things.''')
