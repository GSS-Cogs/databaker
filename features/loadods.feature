Feature: Load ods files
  I want to load ods files into databaker

  # Starting from a file_object
  # TODO - we'll also need the other scenario of starting from a path/string location to the actual file
  # so the "Given" I've just replaced once framework.py can handle both entry points.
  Scenario: Load ods file 1
    Given we use a file object created from "2018internationaltradeinservicesdatatables.ods"
    Then we confirm the names of the loaded tabs are equal to:
    """
    ["Notes", "Index", "1. NUTS1, industry", "2. NUTS1, industry, destination",
    "3. NUTS2, industry", "4. NUTS2, industry, destination", "5. NUTS3, destination",
    "6. City Region, industry", "7. City Region, industry, dest.", "8. Travel", "9. Tidy format"]
    """
    And the output "some_name" should be equal to:
    """
    1. NUTS1, industry
    """
    