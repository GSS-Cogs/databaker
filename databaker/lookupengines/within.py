
from databaker.constants import ABOVE, BELOW, UP, DOWN, LEFT, RIGHT, DIRECTION_DICT
from databaker.lookupengines.generic import override_looked_up_cell

# Essentially a factory function for the actual WithinEngine
# I don't particularly like breaking the python convention of UPPERCLASS == a constant
# but it's probably the lesser evil compared to an inconsistant api
class WITHIN(object):
    
    def __init__(self, **kwargs):
        """
        Factory class to take the intial keywords provided to the WITHIN class/argument (fair bit of indirection here) 
        and provide the arguments as required by the actual WithinEngine (see below) that'll do the lookups.

        We're aiming to get the variables:
        -----------------------------------
        direction_of_travel - are we scanning the cells going LEFT, RIGHT, UP or DOWN?
        starting_offset - how many x or y offsets away (relative to an observation) do we start looking?
        ending_offset  - how many x or y offsets away (relative to an observation) do we finish looking?

        And provide them on demand via the unpack() method
        """

        assert len(kwargs) == 2, 'WITHIN requires exactly 2 keyword argument. Either above & below or left & right (order can be switched)'

        # Unpack the kwargs
        above = kwargs.get("above", None)
        left = kwargs.get("left", None)
        right = kwargs.get("right", None)
        below = kwargs.get("below", None)

        # Check we've been passed sane combinations of keywords
        msg1 = "You can't pass keywords of {} if you're also passing {}"
        msg2 = "You can't use a {} keyword without a corresponding {} keyword"
        if above is not None:
            assert all(x is None for x in [left, right]), msg1.format("left and right", "above")
            assert below is not None, msg2.format("above", "below")

        if below is not None:
            assert all(x is None for x in [left, right]), msg1.format("left and right", "below")
            assert above is not None, msg2.format("below", "above")

        if right is not None:
            assert all(x is None for x in [above, below]), msg1.format("above and below", "right")
            assert left is not None, msg2.format("right", "left")

        if left is not None:
            assert all(x is None for x in [above, below]), msg1.format("above and below", "left")
            assert right is not None, msg2.format("left", "right")

        # Get the direction of travel, this is dependant on the order in which the keyword args are passed
        # e.g (left=1, right=2) is traveling RIGHT, while (right=1, left=1) is travelling LEFT
        if left is not None:
            # Consider the kwargs in the order they were recieved
            for k, v in kwargs.items():
                self.starting_offset = kwargs["left"]
                self.ending_offset = kwargs["right"]
                if k == "left":
                    self.direction_of_travel = RIGHT
                    break
                if k == "right":
                    self.direction_of_travel = LEFT
                    break
        elif above is not None:
            self.starting_offset = kwargs["above"]
            self.ending_offset = kwargs["below"]
            for k, v in kwargs.items():
                if k == "above":
                    self.direction_of_travel = DOWN
                    break
                if k == "below":
                    self.direction_of_travel = UP
                    break
        else:
            raise ValueError('Invalid keywords passed to WITHIN engine.You must have either the "left"'
                    + ' and "right", or "above" and "below" keywords.')

        # In case someone does something silly
        assert isinstance(self.starting_offset, int), f'The parameters passed to the {",".join(kwargs)} keywords must be integers'
        assert isinstance(self.ending_offset, int), f'The parameters passed to the {",".join(kwargs)} keywords must be integers'

    def unpack(self):
        """
        Get the relevant args on demand
        """
        return self.starting_offset, self.ending_offset, self.direction_of_travel


class WithinEngine(object):
    
    def __init__(self, cell_bag, direction, label, starting_offset, ending_offset, direction_of_travel, cellvalueoverride):
        self.cellvalueoverride = cellvalueoverride
        """
        Creates a lookup engine to resolve a WITHIN(<a given range of offsets>) lookup.

        Imagine the following example:

        |  A   |  B   |  C   |  D   |  E   |  F   |  G   |
        |      |      |      |      |      |      |      |
        |      | age1 |      |      |      | age2 |      |
        | ob1  | ob2  | ob3  |      | ob4  | ob5  | ob6  |

        The relationships between the age dimension (age1 and age2 in the example)
        is both LEFT and RIGHT, realtive to a given observation.

        Consider the following code:
        HDim(cells, "Dimensions 1, WITHIN(left=1, right=1), ABOVE)

        This is specifying age is above the observation, but only within the range of
        one to the left through 1 to the right.

        So in that example, we're searching (from the observation) for an age dimension
        cell via the following pattern.

        |   A  |  B   |  C   |  D   |
        |------|------|------|------|
        |   7  |  8   |  9   |      |
        |   4  |  5   |  6   |      |
        |   1  |  2   |  3   |      |
        |      |  ob  |      |      |

        With the header cell we're "looking up" being the first of the cells we've labelled
        1-9 (in that order) that is a cell we've also selected as being part of the "Age" dimension.
        """

        # Store all the things
        self.label = label
        self.direction = direction
        self.starting_offset = starting_offset
        self.ending_offset = ending_offset
        self.direction_of_travel = direction_of_travel
        self.cellvalueoverride = cellvalueoverride
        self.cell_bag = cell_bag

        self.sequence = self._sequencer(cell_bag)  # see docstring

    # scenario 1
    def _xy_traveling_up_and_left(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling right to left from the bottom row to the top row
        """
        for y_offset in range(self.table_height, -1, -1):
            for x_offset in range(self.table_width, -1, -1):
                yield x_offset, y_offset

    # Scenario 2
    def _xy_traveling_up_and_right(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling left to right from the bottom row to the top row
        """
        for y_offset in range(self.table_height, -1, -1):
            for x_offset in range(0, self.table_width+1, 1):
                yield x_offset, y_offset

    # scenario 3
    def _xy_traveling_down_and_left(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling right to left from the top row to the bottom row
        """
        for y_offset in range(0, self.table_height+1, 1):
            for x_offset in range(self.table_width, -1, -1):
                yield x_offset, y_offset

    # scenario 4
    def _xy_traveling_down_and_right(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling left to right from the top row to the bottom row
        """
        for y_offset in range(0, self.table_height+1, 1):
            for x_offset in range(0, self.table_width+1, 1):
                yield x_offset, y_offset

    # scenario 5
    def _xy_traveling_up_cols_and_left(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling from the right most column left and from the bottom 
        row upwards
        """
        for x_offset in range(self.table_width, -1, -1):
            for y_offset in range(self.table_height, -1, -1):
                yield x_offset, y_offset

    # scenario 6
    def _xy_traveling_down_cols_and_right(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling from the left most column right and from the top 
        row downwards
        """
        for x_offset in range(0, self.table_width+1, 1):
            for y_offset in range(0, self.table_height+1, 1):
                yield x_offset, y_offset

    # scenario 7
    def _xy_traveling_up_cols_and_right(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling from the left most column right and from the bottom 
        row upwards
        """
        for x_offset in range(0, self.table_width+1, 1):
            for y_offset in range(self.table_height, -1, -1):
                yield x_offset, y_offset

    # scenario 8
    def _xy_traveling_down_cols_and_left(self):
        """
        Helper, given we know the length and height of the table, yield tuples of all
        xy co-ordinates travelling from the right most column left and from the top 
        row downwards
        """
        for x_offset in range(self.table_width, -1, -1):
            for y_offset in range(-1, self.table_height, 1):
                yield x_offset, y_offset

    def _sequencer(self, cell_bag):
        """
        The sequencer sorts all cells (or pointers to cells) into a linear set based on
        the stated order of consumption.

        eg, for an ABOVE lookup, with a direction of travel of LEFT->RIGHT the following table:

        |   A     |    B    |    C     |
        |   foo   |  bar    |    baz   |
        |   ray   |  egon   |    peter |
        |  larry  |  curly  |    mo    |
 
        Gets sequenced as:
        [larry, curly, mo, ray, egon, peter, foo, bar, baz]

        Whereas with a lookup of BELOW and direction of travel RIGHT->LEFT it would be
        [baz, bar, foo, peter, egon, ray, mo, curly, larry]
        """

        # Get the cell bag into an iterable form
        pristine_table = []
        for pristine_cell in cell_bag.table.unordered_cells:
            pristine_table.append(pristine_cell)

        # Pristine table bags are always exactly square
        self.table_height = max([cell.y for cell in pristine_table])
        self.table_width = max([cell.x for cell in pristine_table])

        # TODO - we need to take a hard look at refactoring this for performance when its all working!
        # I doubt this is even remotely efficient (so lets get the tests working, then we're free to rip the following to bits and make it faster)
        

        def build_sequence(sequence_generator_method):
            sequence = []
            for (x_offset, y_offset) in sequence_generator_method:
                potential_cell = [x for x in cell_bag if x.x == x_offset and x.y == y_offset]
                if len(potential_cell) == 1: 
                    sequence.append(potential_cell[0])

            return sequence
        
        #Scenario 1
        if self.direction == ABOVE and self.direction_of_travel == LEFT:
            sequence = build_sequence(self._xy_traveling_up_and_left())

        #Scenario 2
        elif self.direction == ABOVE and self.direction_of_travel == RIGHT:
            sequence = build_sequence(self._xy_traveling_up_and_right())

        #Scenario 3
        elif self.direction == BELOW and self.direction_of_travel == LEFT:
            sequence = build_sequence(self._xy_traveling_down_and_left())

        #Scenario 4
        elif self.direction == BELOW and self.direction_of_travel == RIGHT:
            sequence = build_sequence(self._xy_traveling_down_and_right())

        #Scenario 5
        elif self.direction == LEFT and self.direction_of_travel == UP:
            sequence = build_sequence(self._xy_traveling_up_cols_and_left())

        #Scenario 6
        elif self.direction == RIGHT and self.direction_of_travel == DOWN:
            sequence = build_sequence(self._xy_traveling_up_cols_and_right())

        #Scenario 7
        elif self.direction == RIGHT and self.direction_of_travel == UP:
            sequence = build_sequence(self._xy_traveling_up_cols_and_right())

        #Scenario 8
        elif self.direction == LEFT and self.direction_of_travel == DOWN:
            sequence = build_sequence(self._xy_traveling_down_cols_and_left())

        else:
            raise ValueError(f'A direction of travel of {self.direction_of_travel} is incomptible with an {self.direction} directed lookup')
        
        return tuple(sequence) # render the sequence immutable because we're not massocists

    def lookup(self, cell):
        """
        Given a cell, lookup the first correct dimension header cell within the specified range of offsets.
        """

        # TODO - think!
        # We've got things into the right sequence so this will work, but given we know the absolute width and height of the
        # table can we shortcut this? Feels like there might be some logic hack to be found here to start us off a better informed /
        # close to the mark point in the sequence.  
        found_cell = None
        for sequenced_cell in self.sequence:
            if self.direction == ABOVE:
                if sequenced_cell.x >= cell.x-self.starting_offset and sequenced_cell.x <= cell.x+self.ending_offset:
                    if sequenced_cell.y < cell.y: # We're looking above, the dimenion option needs to above the cell
                        found_cell = sequenced_cell
                    found_cell = sequenced_cell
                    break

            elif self.direction == BELOW:
                if sequenced_cell.x >= cell.x-self.starting_offset and sequenced_cell.x <= cell.x+self.ending_offset:
                    if sequenced_cell.y > cell.y: # We're looking below, the dimenion option needs to below the cell
                        found_cell = sequenced_cell
                        break

            elif self.direction == LEFT:
                if sequenced_cell.y >= cell.y-self.starting_offset and sequenced_cell.y <= cell.y+self.ending_offset:
                    if sequenced_cell.x < cell.x: # We're looking left, the dimenion option needs to left of the cell
                        found_cell = sequenced_cell
                        break
                    
            elif self.direction == RIGHT:
                if sequenced_cell.y <= cell.y-self.starting_offset and sequenced_cell.y >= cell.x+self.ending_offset:
                    if sequenced_cell.x > cell.x: # We're looking right, the dimenion option needs to be right of cell
                        found_cell = sequenced_cell
                        break

        if found_cell is None:
            raise ValueError(f'Unsuccessful within lookup for cell {cell} in dimension "{self.label}". Direction was {DIRECTION_DICT[self.direction]}'
                        f' and we were scanning {DIRECTION_DICT[self.direction_of_travel]} but no header cell was found in the specified range.')

        cell, cell_value = override_looked_up_cell(found_cell, self.cellvalueoverride) 
        return cell, cell_value