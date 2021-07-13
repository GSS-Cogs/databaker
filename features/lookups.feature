Feature: Create lookup engines
  I want databaker to store accurate lookup information for a given dimension, given the direction and type of lookup.

    Scenario: Create a DIRECTLY dimensionsional lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |  
        | day             | tab.excel_ref("C9:C12")                 |
        | county          | tab.excel_ref("J15:J17")                |
        | top_dims        | tab.excel_ref("G5:I5")                  |
        | bottom_dims     | tab.excel_ref("D26:E26")                |
    And we define the dimensions as
        """
        HDim(day, "Day", DIRECTLY, LEFT)
        HDim(county, "County", DIRECTLY, RIGHT)
        HDim(top_dims, "Top Dims", DIRECTLY, ABOVE)
        HDim(bottom_dims, "Bottom Dims", DIRECTLY, BELOW)
        """
    Then the "DIRECTLY" dimension "Day" has stored lookup information equal to
        """
        {"8": {"get": ["{<C9 22.0>}"]}, "9": {"get": ["{<C10 29.0>}"]}, "1": {"0": {"get": ["{<C11 1.0>}"]}, "1": {"get": ["{<C12 8.0>}"]}}}
        """
    Then the "DIRECTLY" dimension "County" has stored lookup information equal to
        """
        {"1": {"4": {"get": ["{<J15 'NI County 5'>}"]}, "5": {"get": ["{<J16 'Sco County 1'>}"]}, "6": {"get": ["{<J17 'Sco County 2'>}"]}}}
        """
    Then the "DIRECTLY" dimension "Top Dims" has stored lookup information equal to
        """
        {"6": {"get": ["{<G5 'Dim 4'>}"]}, "7": {"get": ["{<H5 'Dim 5'>}"]}, "8": {"get": ["{<I5 'Dim 6'>}"]}}
        """
    Then the "DIRECTLY" dimension "Bottom Dims" has stored lookup information equal to
        """
        {"3": {"get": ["{<D26 'Dim 7'>}"]}, "4": {"get": ["{<E26 'Dim 8'>}"]}}
        """ 

    Scenario: Create a CLOSEST dimensionsional lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |  
        | year            | tab.excel_ref("A13")                    |
        | unit            | tab.excel_ref("M13")                    |
        | month           | tab.excel_ref("B6:B15").is_not_blank()  |
        | under_dim       | tab.excel_ref("D27")                    |
    And we define the dimensions as
        """
        HDim(year, "Year", CLOSEST, LEFT)
        HDim(unit, "Unit", CLOSEST, RIGHT)
        HDim(month, "Month", CLOSEST, ABOVE)
        HDim(under_dim, "Under Dim", CLOSEST, BELOW)
        """
    Then the "CLOSEST" dimension "Year" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 0, "highest_offset": 99999999999, "dimension_cell": "{<A13 'Year'>}"}}
        """
    Then the "CLOSEST" dimension "Unit" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 0, "highest_offset": 12, "dimension_cell": "{<M13 'Unit'>}"}}
        """
    Then the "CLOSEST" dimension "Month" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 5, "highest_offset": 9, "dimension_cell": "{<B6 'Jan'>}"}, "1": {"lowest_offset": 10, "highest_offset": 99999999999, "dimension_cell": "{<B11 'Apr'>}"}}
        """
    Then the "CLOSEST" dimension "Under Dim" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 0, "highest_offset": 26, "dimension_cell": "{<D27 'Another Dim 2'>}"}}
        """

Scenario: Create a CONSTANT dimension
    Given we load a file named "bakingtestdataset.xls"
        And select the sheet "Sheet1"
        And we define cell selections as
        | key             | value                                   | 
        | observations    | tab.excel_ref("D6:I25")                 |
    And we define the dimensions as
        """
        HDimConst("Constant1", "foo")
        HDimConst("Constant2", "bar")
        """
    Then all lookups to dimension "Constant1" should return the value "foo"
    And all lookups to dimension "Constant2" should return the value "bar"

# Within Scenario 1
Scenario: Create a WITHIN ABOVE, right to left dimensionsional lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key               | value                                   |  
        | cats_and_dogs     | tab.excel_ref("3").is_not_blank()       |
        | observations      | tab.excel_ref("C6:I25")                 |
    And we define the dimensions as
        """
        HDim(cats_and_dogs, "Cats And Dogs", WITHIN(right=2, left=1), ABOVE)
        """
    Then the lookup from an observation in cell "C25" to the dimension "Cats And Dogs" returns "{<E3 'Cats'>}"
    And the lookup from an observation in cell "F25" to the dimension "Cats And Dogs" returns "{<E3 'Cats'>}"
    And the lookup from an observation in cell "G25" to the dimension "Cats And Dogs" returns "{<I3 'Dogs'>}"
    And the lookup from an observation in cell "I25" to the dimension "Cats And Dogs" returns "{<I3 'Dogs'>}"

# Within Scenario 2
Scenario: Create a WITHIN ABOVE, left to right lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key               | value                                   |  
        | cats_and_dogs     | tab.excel_ref("3").is_not_blank()       |
        | observations      | tab.excel_ref("C6:I25")                 |
    And we define the dimensions as
        """
        HDim(cats_and_dogs, "Cats And Dogs", WITHIN(left=1, right=2), ABOVE)
        """
    Then the lookup from an observation in cell "C25" to the dimension "Cats And Dogs" returns "{<E3 'Cats'>}"
    And the lookup from an observation in cell "F25" to the dimension "Cats And Dogs" returns "{<E3 'Cats'>}"
    And the lookup from an observation in cell "G25" to the dimension "Cats And Dogs" returns "{<I3 'Dogs'>}"
    And the lookup from an observation in cell "I25" to the dimension "Cats And Dogs" returns "{<I3 'Dogs'>}"

# Within Scenario 3
Scenario: Create a WITHIN BELOW, right to left lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key               | value                                   |  
        | sheep_and_ducks   | tab.excel_ref("28").is_not_blank()      |
        | observations      | tab.excel_ref("C6:I25")                 |
    And we define the dimensions as
        """
        HDim(sheep_and_ducks, "Sheep and Ducks", WITHIN(right=2, left=1), BELOW)
        """
    Then the lookup from an observation in cell "C6" to the dimension "Sheep and Ducks" returns "{<E28 'Sheep'>}"
    And the lookup from an observation in cell "F6" to the dimension "Sheep and Ducks" returns "{<E28 'Sheep'>}"
    And the lookup from an observation in cell "G6" to the dimension "Sheep and Ducks" returns "{<I28 'Ducks'>}"
    And the lookup from an observation in cell "I6" to the dimension "Sheep and Ducks" returns "{<I28 'Ducks'>}"

# Within Scenario 4
Scenario: Create a WITHIN BELOW, left to right lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key               | value                                   |  
        | sheep_and_ducks   | tab.excel_ref("28").is_not_blank()      |
        | observations      | tab.excel_ref("C6:I25")                 |
    And we define the dimensions as
        """
        HDim(sheep_and_ducks, "Sheep and Ducks", WITHIN(left=1, right=2), BELOW)
        """
    Then the lookup from an observation in cell "C6" to the dimension "Sheep and Ducks" returns "{<E28 'Sheep'>}"
    And the lookup from an observation in cell "F6" to the dimension "Sheep and Ducks" returns "{<E28 'Sheep'>}"
    And the lookup from an observation in cell "G6" to the dimension "Sheep and Ducks" returns "{<I28 'Ducks'>}"
    And the lookup from an observation in cell "I6" to the dimension "Sheep and Ducks" returns "{<I28 'Ducks'>}"

# Within Scenario 5
Scenario: Create a WITHIN LEFT, below to above lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key                   | value                                         |  
        | birds_and_fish        | tab.excel_ref("A").one_of(["Fish", "Birds"])  |
        | observations          | tab.excel_ref("C6:I25")                       |
    And we define the dimensions as
        """
        HDim(birds_and_fish, "Birds and Fish", WITHIN(below=3, above=4), LEFT)
        """
    Then the lookup from an observation in cell "I7" to the dimension "Birds and Fish" returns "{<A10 'Birds'>}"
    And the lookup from an observation in cell "I10" to the dimension "Birds and Fish" returns "{<A10 'Birds'>}"
    And the lookup from an observation in cell "I17" to the dimension "Birds and Fish" returns "{<A17 'Fish'>}"
    And the lookup from an observation in cell "I19" to the dimension "Birds and Fish" returns "{<A17 'Fish'>}"

# Within Scenario 6
Scenario: Create a WITHIN RIGHT, above to below lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key                   | value                                    |  
        | horses_and_cows       | tab.excel_ref("L").is_not_blank()        |
        | observations          | tab.excel_ref("C6:I25")                  |
    And we define the dimensions as
        """
        HDim(horses_and_cows, "Horses and Cows", WITHIN(above=3, below=3), RIGHT)
        """
    Then the lookup from an observation in cell "C7" to the dimension "Horses and Cows" returns "{<L10 'Horses'>}"
    And the lookup from an observation in cell "C10" to the dimension "Horses and Cows" returns "{<L10 'Horses'>}"
    And the lookup from an observation in cell "C17" to the dimension "Horses and Cows" returns "{<L17 'Cows'>}"
    And the lookup from an observation in cell "C19" to the dimension "Horses and Cows" returns "{<L17 'Cows'>}"

# Within Scenario 7
Scenario: Create a WITHIN RIGHT, below to above lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key                   | value                                    |  
        | horses_and_cows       | tab.excel_ref("L").is_not_blank()        |
        | observations          | tab.excel_ref("C6:I25")                  |
    And we define the dimensions as
        """
        HDim(horses_and_cows, "Horses and Cows", WITHIN(below=3, above=3), RIGHT)
        """
    Then the lookup from an observation in cell "C7" to the dimension "Horses and Cows" returns "{<L10 'Horses'>}"
    And the lookup from an observation in cell "C10" to the dimension "Horses and Cows" returns "{<L10 'Horses'>}"
    And the lookup from an observation in cell "C17" to the dimension "Horses and Cows" returns "{<L17 'Cows'>}"
    And the lookup from an observation in cell "C19" to the dimension "Horses and Cows" returns "{<L17 'Cows'>}"

# Within Scenario 8
Scenario: Create a WITHIN LEFT, above to below lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key                   | value                                    |  
        | birds_and_fish        | tab.excel_ref("A").is_not_blank()        |
        | observations          | tab.excel_ref("C6:I25")                  |
    And we define the dimensions as
        """
        HDim(birds_and_fish, "Birds and Fish", WITHIN(above=3, below=4), LEFT)
        """
    Then the lookup from an observation in cell "I7" to the dimension "Birds and Fish" returns "{<A10 'Birds'>}"
    And the lookup from an observation in cell "I10" to the dimension "Birds and Fish" returns "{<A10 'Birds'>}"
    And the lookup from an observation in cell "I17" to the dimension "Birds and Fish" returns "{<A17 'Fish'>}"
    And the lookup from an observation in cell "I19" to the dimension "Birds and Fish" returns "{<A17 'Fish'>}"

Scenario: Create a complex series of WITHIN dimensional lookups
    Given we load a file named "complexwithinexample.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key               | value                                                    |  
        | observations      | tab.excel_ref("C4:J35").is_not_blank()                   |
        | month             | tab.excel_ref("A").one_of(["Jan", "Jul"])                |
        | year              | tab.excel_ref("A").one_of(["2019.0", "2020.0", "2021.0"])  |
    And we define the dimensions as
        """
        HDim(month, "Month", WITHIN(below=1, above=6), LEFT)
        HDim(year, "Year", WITHIN(below=2, above=5), LEFT)
        """
    Then the lookup from an observation in cell "D8" to the dimension "Month" returns "{<A5 'Jan'>}"
    And the lookup from an observation in cell "D8" to the dimension "Year" returns "{<A6 2019.0>}"
    And the lookup from an observation in cell "D10" to the dimension "Month" returns "{<A11 'Jul'>}"
    And the lookup from an observation in cell "D10" to the dimension "Year" returns "{<A12 2019.0>}"
    And the lookup from an observation in cell "H35" to the dimension "Month" returns "{<A29 'Jan'>}"
    And the lookup from an observation in cell "H35" to the dimension "Year" returns "{<A30 2021.0>}"

Scenario: Create a WITHIN dimensional lookup with 0 dimension selections
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key               | value                                   |  
        | sheep_and_ducks   | tab.excel_ref("29").is_not_blank()      |
        | observations      | tab.excel_ref("C6:I25")                 |
    And we define the dimensions as
        """
        HDim(sheep_and_ducks, "Sheep and Ducks", WITHIN(right=2, left=1), BELOW)
        """
    And we create a ConversionSegment object.
    Then we attempt to extract the dimensions, capturing the first exception as
        """
        Unsuccessful within lookup for cell <C6 1.0> in dimension "Sheep and Ducks". Direction was BELOW and we were scanning LEFT but no header cell was found in the specified range.
        """