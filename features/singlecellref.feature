Feature: Define a dimension as a value from a single cell reference.
  I want to be able to define a dimension as a value from a single cell reference which stays constant for all observations.

  Scenario Outline: Define unit from single cell reference.
    Given we load a file named <File Name>
    And select the sheet "Sheet2"
    And we define cell selections as
      | key             | value                                   |  
      | unit            | tab.excel_ref("P5")                     |
    Then we confirm the cell selection is the correct type.
    """
    <class 'xypath.xypath.Bag'>
    """
    Then we confirm the cell selection is equal to:
    """
    {<P5 '(£Million)'>}
    """

    Examples: File Types
      | File Name                   |
      | "bakingtestdataset.xls"     |
      | "bakingtestdataset.xlsx"    |