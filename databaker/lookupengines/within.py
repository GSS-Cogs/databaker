
from typing import NamedTuple

from databaker.constants import ABOVE

class NoneCell(NamedTuple):
    x: int
    y: int

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
        direction_of_travel - are we scanning the cells going left, right, up or down?
        starting_offset - how many x or y offsets away (relative to an observation) do we start looking?
        ending_offset  - how many x or y offsets away (relative to an observation) do we finish looking?

        And provide them on demand via the unpack() method
        """

        assert len(kwargs) == 2, 'WITHIN requires exactly 2 keyword argument. Either ABOVE & BELOW or LEFT & RIGHT (order can be switched)'

        # Unpack the kwargs
        ABOVE = kwargs.get("ABOVE", None)
        LEFT = kwargs.get("LEFT", None)
        RIGHT = kwargs.get("RIGHT", None)
        BELOW = kwargs.get("BELOW", None)

        # Check we've been passed sane combinations of keywords
        msg1 = "You can't pass keywords of {} if you're also passing {}"
        msg2 = "You can't use a {} keyword without a corresponding {} keyword"
        if ABOVE is not None:
            assert all(v is None for v in [LEFT, RIGHT]), msg1.format("LEFT and RIGHT", "ABOVE")
            assert BELOW is not None, msg2.format("ABOVE", "BELOW")

        if BELOW is not None:
            assert all(v is None for v in [LEFT, RIGHT]), msg1.format("LEFT and RIGHT", "BELOW")
            assert ABOVE is not None, msg2.format("BELOW", "ABOVE")

        if RIGHT is not None:
            assert all(v is None for v in [ABOVE, BELOW]), msg1.format("ABOVE and BELOW", "RIGHT")
            assert LEFT is not None, msg2.format("RIGHT", "LEFT")

        if LEFT is not None:
            assert all(v is None for v in [ABOVE, BELOW]), msg1.format("ABOVE and BELOW", "LEFT")
            assert RIGHT is not None, msg2.format("LEFT", "RIGHT")

        """
        delete me
        UP = (0, -1)
        RIGHT = (1, 0)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        """
        # Get the direction of travel, this is dependant on the order in which the keyword args are passed
        # e.g (LEFT=1, RIGHT=2) is traveling RIGHT, while (RIGHT=1, LEFT=1) is travelling LEFT
        if LEFT is not None:
            # Consider the kwargs in the order they were recieved
            for k, v in kwargs.items():
                if k == "LEFT":
                    self.starting_offset = kwargs["LEFT"]  # the integer passed
                    self.ending_offset = kwargs["RIGHT"]
                    self.direction_of_travel = (1, 0)   # RIGHT, expressed in xy terms
                    break
                if k == "RIGHT":
                    self.starting_offset = kwargs["RIGHT"]
                    self.ending_offset = kwargs["LEFT"]
                    self.direction_of_travel = (-1, 0)   # LEFT, expressed in xy terms
                    break
        elif ABOVE is not None:
            for k, v in kwargs.items():
                if k == "ABOVE":
                    self.starting_offset = kwargs["ABOVE"]
                    self.ending_offset = kwargs["BELOW"]
                    self.direction_of_travel = (0, 1)   # DOWN, expressed in xy terms
                    break
                if k == "BELOW":
                    self.starting_offset = kwargs["BELOW"]
                    self.ending_offset = kwargs["ABOVE"]
                    self.direction_of_travel = (0, -1)   # UP, expressed in xy terms
                    break
        else:
            raise ValueError('Invalid keywords passed to WITHIN engine.You must have either LEFT'
                    + ' and RIGHT, or ABOVE and BELOW keywords.')

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
        HDim(cells, "Dimensions 1, WITHIN(LEFT=1, RIGHT=1), ABOVE)

        This is specifying age is above the observation, but only within the range of
        one to the left through 1 to the right.

        So in that example, we're searching (from the observation) for an age dimension
        cell via the following pattern.

        |   A  |  B   |  C   |  D   |
        |      |      |      |      |
        |   7  |  8   |  9   |      |
        |   4  |  5   |  6   |      |
        |   1  |  2   |  3   |      |
        |      |  ob  |      |      |

        With the header cell we're "looking up" being the first of the cells we've labelled
        1-9 (in that order) that is a cell we've also selected as being part of the "Age" dimension,
        relative to the observation in question (the cell marked "ob" in this example).
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

        This is to allow us to consume the appropriate cells via their range. So with the
        original ABOVE and LEFT->RIGHT sequence

        -- pseudo code --
        for i in range(0, len(sequence), 2):
            print(cells[i])
            print(cells[1+1])

        gets us:
            larry
            curly
            ray
            egon
            foo
            bar
        ------------

        Which would be the exact sequence of consideration for a lookup of WITHIN(LEFT=0, RIGHT=1)
        from an observation existing in cell A4.

        Note - we basically need to sequence the whole table bag here, so any cell that doesn't intersect with
        a cell from out dimension selection is just a pointer to None (otherwise this will get computationally expensive).
        """

        # Use the pointer on the 1st cell to get the pristine table the cell bag was formed from
        pristine_table = []
        for pristine_cell in cell_bag.table.unordered_cells:
            pristine_table.append(pristine_cell)

        # Pristine table bags are always exactly square
        self.table_height = max([cell.y for cell in pristine_table])
        self.table_width = max([cell.x for cell in pristine_table])

        # TODO - it is CRITICAL to take a hard look at refactoring this for performance when its all working!
        # I doubt this is even remotely efficient (so lets get the tests working, then we're free to rip the following to bits and make it faster)
        sequence = []

        oops = 'Aborting, WITHIN engine not correctly imbibing all table cells. Expected {} cells, Imbibing {}' # TODO, funny but ffs dont leave it as oops

        """
        delete me
        UP = (0, -1)
        RIGHT = (1, 0)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        """

        if self.direction == ABOVE:

            # Scenario 1: Scanning leftwards moving upwards from the bottom right of the table/tab
            if self.direction_of_travel == (-1, 0):
                for y_offset in range(self.table_height, -1, -1):
                    for x_offset in range(self.table_width, -1, -1):
                        single_cell_bag = [cell for cell in pristine_table if cell.x == x_offset and cell.y == y_offset]
                        sequence.append(single_cell_bag if single_cell_bag in cell_bag else None)

            # Scenario 2: Scanning rightwards moving upwards from the bottom left of the table/tab
            elif self.direction_of_travel == (1, 0):
                for y_offset in range(self.table_height, -1, -1):
                    for x_offset in range(0, self.table_width+1, 1):
                        possible_cell_as_list = [cell for cell in pristine_table if cell.x == x_offset and cell.y == y_offset]
                        assert len(possible_cell_as_list) == 1, f'Pristine table is {pristine_table}'
                        possible_cell = possible_cell_as_list[0]
                        is_in_dimension = len([cell for cell in cell_bag if cell.x == possible_cell.x and cell.y == possible_cell.y]) > 0
                        sequence.append(possible_cell if is_in_dimension else NoneCell(x=x_offset, y=y_offset))
            else:
                raise ValueError(f'A direction of travel of {self.direction_of_travel} is incomptible with an ABOVE directed lookup')

        return tuple(sequence) # render the sequence immutable because we're not massocists


    def lookup(self, cell):
        """
        Given a cell, lookup the first correct dimension header cell within the specified range of offsets.

        Note: see the docstring for _sequencer for a explanation of how this works
        """

        start_cell = [x for x in self.sequence if x.x == cell.x-self.starting_offset and x.y == cell.y][0]
        start_at = self.sequence.index(start_cell)

        found_cell = None
        for i in range(0, len(self.sequence)):
            if self.sequence[i].x < cell.x-self.starting_offset:
                continue
            if not isinstance(self.sequence[i], NoneCell):
                found_cell = self.sequence[i]
                break

        if found_cell is None:
            raise ValueError(f'Unsuccessful withing lookup for cell {cell} in dimension {self.label}')

        # Apply str level cell value override if applicable
        if found_cell.value in self.cellvalueoverride:
            value = self.cellvalueoverride[found_cell.value]
        elif found_cell in self.cellvalueoverride:
            value = self.cellvalueoverride[found_cell]
        else:
            value = found_cell.value

        return found_cell, value