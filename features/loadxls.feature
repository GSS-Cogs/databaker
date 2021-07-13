Feature: Load xls files
  I want to load xls files into databaker

  Scenario: Load xls file 1
    Given we load a file named "2018internationaltradeinservicesdatatables.xls"
    Then we confirm the names of the loaded tabs are equal to:
    """
    ["Notes", "Index", "1. NUTS1, industry", "2. NUTS1, industry, destination",
    "3. NUTS2, industry", "4. NUTS2, industry, destination", "5. NUTS3, destination",
    "6. City Region, industry", "7. City Region, industry, dest.", "8. Travel", "9. Tidy format"]
    """
    And an expected output should be equal to:
    """
    1. NUTS1, industry
    """ 