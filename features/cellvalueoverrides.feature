Feature: Create lookup engines
  I want databaker to store accurate lookup information for a given dimension, given the direction and type of lookup.

    Scenario: Apply cellvalueoverrides via a dictionary with a DIRECTLY lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:I10")                 | 
        | county          | tab.excel_ref("J6:J10").is_not_blank()  |
    And we define the dimensions as
        """
        HDim(county, "County", DIRECTLY, RIGHT, cellvalueoverride={"Eng County 2": "Mongolia County 1"})
        """
    And we create a ConversionSegment object.
    And we convert the ConversionSegment object into a pandas dataframe.
    Then the unique contents of the "County" column should be equal to
        """
        ['Eng County 1', 'Eng County 3', 'Eng County 4', 'Eng County 5', 'Mongolia County 1']
        """

    Scenario: Apply cellvalueoverrides via a dictionary with a CLOSEST lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:D26")                 | 
        | month           | tab.excel_ref("B6:B25").is_not_blank()  |
    And we define the dimensions as
        """
        HDim(month, "Month", CLOSEST, ABOVE, cellvalueoverride={"Oct": "Of Sundays"})
        """
    And we create a ConversionSegment object.
    And we convert the ConversionSegment object into a pandas dataframe.
    Then the unique contents of the "Month" column should be equal to
        """
        ['Apr', 'Jan', 'Jul', 'Of Sundays']
        """

    Scenario: Apply cellvalueoverrides at the cell level to work with a DIRECTLY lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:D10")                 | 
        | county          | tab.excel_ref("J6:J10").is_not_blank()  |
    And we define the dimensions as
        """
        HDim(county, "County", DIRECTLY, RIGHT)
        """
    And I add a cell value override for the cell "J10" in the dimension "County" to the string "Mongolia East 16"
    And we create a ConversionSegment object.
    And we convert the ConversionSegment object into a pandas dataframe.
    Then the unique contents of the "County" column should be equal to
        """
        ['Eng County 1', 'Eng County 2', 'Eng County 3', 'Eng County 4', 'Mongolia East 16']
        """   

    Scenario: Apply cellvalueoverrides at the cell level to work with a CLOSEST lookup
    Given we load a file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:D26")                 | 
        | month           | tab.excel_ref("B6:B25").is_not_blank()  |
    And we define the dimensions as
        """
        HDim(month, "Month", CLOSEST, ABOVE)
        """
    And I add a cell value override for the cell "B6" in the dimension "Month" to the string "April Fools Day"
    And we create a ConversionSegment object.
    And we convert the ConversionSegment object into a pandas dataframe.
    Then the unique contents of the "Month" column should be equal to
        """
        ['Apr', 'April Fools Day', 'Jul', 'Oct']
        """