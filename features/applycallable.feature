Feature: Apply callables passed in at runtime to a dimension constructor
    As a data enginner. When I construct a databaker dimension, I want to be able to pass in a function, lambda or
    other callable that acts upon any values returned by a lookup to a dimension.

    Scenario Outline: Apply a callable to a dimension constructor for a CLOSEST engine
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key             | value                                   |  
        | month           | tab.excel_ref("B6:B25").is_not_blank()  |
        | observations    | tab.excel_ref("C6:I25")                 |
        And we define the dimensions as
        """
        HDim(month, "Month", CLOSEST, ABOVE, apply=lambda x: f"I am the month: {x}")
        """
        Then the lookup from an observation in cell "C8" to the dimension "Month" returns the value "I am the month: Jan"
        And the lookup from an observation in cell "C13" to the dimension "Month" returns the value "I am the month: Apr"
        And the lookup from an observation in cell "C18" to the dimension "Month" returns the value "I am the month: Jul"
        And the lookup from an observation in cell "C23" to the dimension "Month" returns the value "I am the month: Oct"

        Examples: File Types
            | File Name                       |
            | "bakingtestdataset.xls"         |
            | "bakingtestdataset.xlsx"        |
            | "bakingtestdataset.ods"         |

    Scenario Outline: Apply a callable to a dimension constructor for a DIRECT engine
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key             | value                                   |  
        | top_dims        | tab.excel_ref("D5:I5")                  |
        | observations    | tab.excel_ref("C6:I25")                 |
        And we define the dimensions as
        """
        HDim(top_dims, "Top Dims", DIRECTLY, ABOVE, apply=lambda x: f'{x} got this text added.')
        """
        Then the lookup from an observation in cell "D8" to the dimension "Top Dims" returns the value "Dim 1 got this text added."
        And the lookup from an observation in cell "E8" to the dimension "Top Dims" returns the value "Dim 2 got this text added."
        And the lookup from an observation in cell "F8" to the dimension "Top Dims" returns the value "Dim 3 got this text added."
        And the lookup from an observation in cell "G8" to the dimension "Top Dims" returns the value "Dim 4 got this text added."

        Examples: File Types
            | File Name                       |
            | "bakingtestdataset.xls"         |
            | "bakingtestdataset.xlsx"        |
            | "bakingtestdataset.ods"         |


    
    Scenario Outline: Apply a callable to a dimension constructor for a WITHIN engine

        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
            | key               | value                                   |  
            | cats_and_dogs     | tab.excel_ref("3").is_not_blank()       |
            | observations      | tab.excel_ref("C6:I25")                 |
        And we define the dimensions as
            """
            HDim(cats_and_dogs, "Cats And Dogs", WITHIN(right=2, left=1), ABOVE, apply=lambda x: f'I love {x} a whole bunch')
            """
        Then the lookup from an observation in cell "C25" to the dimension "Cats And Dogs" returns the value "I love Cats a whole bunch"
        And the lookup from an observation in cell "F25" to the dimension "Cats And Dogs" returns the value "I love Cats a whole bunch"
        And the lookup from an observation in cell "G25" to the dimension "Cats And Dogs" returns the value "I love Dogs a whole bunch"
        And the lookup from an observation in cell "I25" to the dimension "Cats And Dogs" returns the value "I love Dogs a whole bunch"


    Scenario Outline: Apply multiple ordered callables to a dimension constructor for a DIRECT engine
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key             | value                                   |  
        | top_dims        | tab.excel_ref("D5:I5")                  |
        | observations    | tab.excel_ref("C6:I25")                 |
        And we define the dimensions as
        """
        HDim(top_dims, "Top Dims", DIRECTLY, ABOVE, apply=(lambda x: f'{x} got this text added.', lambda x: x.replace(' got this', '')))
        """
        Then the lookup from an observation in cell "D8" to the dimension "Top Dims" returns the value "Dim 1 text added."
        And the lookup from an observation in cell "E8" to the dimension "Top Dims" returns the value "Dim 2 text added."
        And the lookup from an observation in cell "F8" to the dimension "Top Dims" returns the value "Dim 3 text added."
        And the lookup from an observation in cell "G8" to the dimension "Top Dims" returns the value "Dim 4 text added."

        Examples: File Types
            | File Name                       |
            | "bakingtestdataset.xls"         |
            | "bakingtestdataset.xlsx"        | 
            | "bakingtestdataset.ods"         |

