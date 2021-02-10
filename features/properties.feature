Feature: Ensure that when a file is read, the correct cell properties are also stored along side each cell.
    I want to be able to load any file into databaker which could contain a number of cell property
    formatting styles. When I load in a file, I want these formatting styles to be preserved in some manner.

    Scenario Outline: Select bold cells from any file type.
        Given we load an xls file named <File Name>
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
            #| "exampleproperties.xlsx"    |


    Scenario Outline: Select underlined cells from any file type.
        Given we load an xls file named <File Name>
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
            #| "exampleproperties.xlsx"    |


    Scenario Outline: Select italic cells from any file type.
        Given we load an xls file named <File Name>
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
            #| "exampleproperties.xlsx"    |

    
    Scenario Outline: Select struckout cells from any file type.
        Given we load an xls file named <File Name>
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
            #| "exampleproperties.xlsx"    |


    Scenario Outline: Select cells with particular font from any file type.
        Given we load an xls file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                  | value                    |  
        | font_selection       | tab.is_font_name()       |
        Then the selection for "font_selection" should be equal to
        """
        ['a 2015']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |

    Scenario Outline: Select cells with size property from any file type.
        Given we load an xls file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                  | value                    |  
        | size_selection       | tab.is_size()            |  
        Then the selection for "size_selection" should be equal to
        """
        ['']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |

    
    Scenario Outline: Select cells with particular font colour from any file type.
        Given we load an xls file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                         | value                      |  
        | font_colour_selection       | tab.is_font_colour()       |
        Then the selection for "font_colour_selection" should be equal to
        """
        ['']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |


    Scenario Outline: Select cells with particular background colour from any file type.
        Given we load an xls file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                         | value                            |  
        | back_colour_selection       | tab.is_background_colour()       |
        Then the selection for "back_colour_selection" should be equal to
        """
        ['']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |


    Scenario Outline: Select cells with any border from any file type.
        Given we load an xls file named <File Name>
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
        Given we load an xls file named <File Name>
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


    Scenario Outline: Select cells with formatting string from any file type.
        Given we load an xls file named <File Name>
        And select the sheet "Sheet1"
        And we define cell selections as
        | key                               | value                            |  
        | formatting_string_selection       | tab.is_formatting_string()       |
        Then the selection for "formatting_string_selection" should be equal to
        """
        ['']
        """

        Examples: File Types
            | File Name                   |
            | "exampleproperties.xls"     |
            #| "exampleproperties.xlsx"    |
