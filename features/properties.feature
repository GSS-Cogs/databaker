Feature: Ensure that when a file is read, the correct cell properties are also stored along side each cell.
    I want to be able to load any file into databaker which could contain a number of cell property
    formatting styles. When I load in a file, I want these formatting styles to be preserved in some manner.

    Scenario Outline: Select bold cells from any file type.
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                       | value                           |  
        | bold_selection            | tab.excel_ref('E').is_bold()    |
        Then the selection for "bold_selection" should be equal to
        """
        ['This is BOLD']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            | "exampleproperties.xlsx"    |


    Scenario Outline: Select underlined cells from any file type.
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                         | value                   |  
        | underline_selection         | tab.is_underline()      |
        Then the selection for "underline_selection" should be equal to
        """
        ['This is Underlined']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            | "exampleproperties.xlsx"    |


    Scenario Outline: Select italic cells from any file type.
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                       | value                           |  
        | italic_selection          | tab.excel_ref('C').is_italic()  |
        Then the selection for "italic_selection" should be equal to
        """
        ['This is Italic']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            | "exampleproperties.xlsx"    |

    
    Scenario Outline: Select struckout cells from any file type.
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                       | value                              |  
        | strikeout_selection       | tab.excel_ref('E').is_strikeout()  |
        Then the selection for "strikeout_selection" should be equal to
        """
        ['This is Strikeout']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            | "exampleproperties.xlsx"    |


    Scenario Outline: Select cells with any border from any file type.
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                         | value                     |  
        | any_border_selection        | tab.is_any_border()       |
        Then the selection for "any_border_selection" should be equal to
        """
        ['All borders', 'Any border']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |


    Scenario Outline: Select cells with all borders from any file type.
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                         | value                     |  
        | all_borders_selection       | tab.is_all_border()       |
        Then the selection for "all_borders_selection" should be equal to
        """
        ['All borders']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |

    Scenario Outline: Select all non-blank cells
        Given we load a file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                         | value                     |  
        | non_blank_selection         | tab.excel_ref("C").is_not_blank()       |
        Then the selection for "non_blank_selection" should be equal to
        """
        ['12015', '2015', '20152', 'Any border', 'This is Italic']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            | "exampleproperties.xlsx"    |

