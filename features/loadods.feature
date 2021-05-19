Feature: Load ods files
  I want to load ods files into databaker

  Scenario: Load ods file 1 from file object
    Given we use a file object created from "2018internationaltradeinservicesdatatables.ods"
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

  Scenario: Load ods file 1 from file name
    Given we load a file named "2018internationaltradeinservicesdatatables.ods"
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

  Scenario: Load ods file 1 from file path
    Given we load a file from the path "/Users/charlesrendle/databaker-docker/databaker-ods-loader/databaker/features/fixtures/2018internationaltradeinservicesdatatables.ods"
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
    