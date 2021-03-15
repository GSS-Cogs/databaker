Feature: Define dimension using bag.is/is_not_richtext()
    I want to be able to define a dimension by identifying all the richtext or 
    non-richtext values from a bag of cells.

    Scenario Outline: Define construction type by non-richtext values in row "6"
    Given we load a file named <File Name>
    And select the sheet "Sheet2"
    And we define cell selections as
      | key                     |value                                                             |  
      | construction_type       | tab.excel_ref("A6"+":P6").is_not_richtext().is_not_blank()       |
    Then we confirm the cell selection contains "7" cells.
    And we confirm the cell selection is equal to:
    """
    {<P6 'All Work'>, <C6 'New Housing'>, <K6 'Repair and Maintenance'>, <J6 'All New Work'>, <E6 'Total Housing'>, <O6 'All Repair and Maintenance'>, <F6 'Other New Work'>}
    """

    Examples: File Types
            | File Name                   |
            | "bakingtestdataset.xls"     |
            | "bakingtestdataset.xlsx"    |

Scenario Outline: Define construction type by richtext values in row "6"
    Given we load a file named <File Name>
    And select the sheet "Sheet2"
    And we define cell selections as
      | key                           |value                                                         |  
      | blank_construction_type       | tab.excel_ref("A6"+":P6").is_richtext().is_not_blank()       |
    Then we confirm the cell selection contains "0" cells.
    And we confirm the cell selection is equal to:
    """
    set()
    """

    Examples: File Types
            | File Name                   |
            | "bakingtestdataset.xls"     |
            | "bakingtestdataset.xlsx"    |