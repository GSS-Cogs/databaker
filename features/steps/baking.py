import json
import os

from behave import *
from pathlib import Path
from databaker.framework import loadxlstabs
from databaker.jupybakeutils import *
from databaker.structure_csv_default import *
from databaker.constants import *

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

###
#This feature works by using a custom dataset which displays all strict and direction qualities
#in a single tab. This has been prior transformed and converted to a CSV file which is brought
#in as a fixture and then converted into a dataframe. In the steps we then can complete the 
#transform steps again until .topandas() is called and then we can compare the two resulting
#dataframes for any inconsistencies - hopefully none! 
###


#From the tab, define all dimensions and observations in the usual transform manner.
@given(u'we define cell selections as')
def step_impl(context):
    tab = context.tab_selected
    context.selections = {}

    for row in context.table:
        context.selections[row[0]] = eval(row[1])

#Now we build the dimensions list.
@given(u'we define the dimensions as')
def step_impl(context):
    dimension_statments = context.text.split("\n")
    context.dimensions = []
    for ds in dimension_statments:

        # Modify the statment to get the selection from context, so
        # HDim(year, "Year", CLOSEST, LEFT)
        # becomes
        # HDim(context.selections["year"], "Year", CLOSEST, LEFT)
        ds_tokens = ds.split(",")
        ds0 = ds_tokens[0]
        ds0 = ds0.split("(")[0]+f'(context.selections[\'{ds0.split("(")[1]}\'],'
        ds = ds0 + ",".join(ds_tokens[1:])
        context.dimensions.append(eval(ds))

#We use the list to instanciate a conversion segment object.
@given(u'we create a ConversionSegment object.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Given we create a ConversionSegment object.')
    context.tidy_sheet = ConversionSegment(context.tab_selected, context.dimensions, context.selections["observations"])


#The conversion segment object is converted into a dataframe using it's function .topandas()
#This is the function which takes ages because it now loops for all dims and obs.
@given(u'we convert the ConversionSegment object into a pandas dataframe.')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Given we convert the ConversionSegment object into a pandas dataframe.')
    context.df = context.tidy_sheet.topandas()


#Bring the csv fixture in as the expected output and convert that into a dataframe making sure the data type of the 'Day' dimension is set to 'object'.
@given(u'we have the file "{expected_csv}" transformed back into a pandas dataframe.')
def step_impl(context, expected_csv):
    #raise NotImplementedError(u'STEP: Given we have the expected CSV file transformed back into a pandas dataframe.')
    path_to_csv = get_fixture(expected_csv)
    context.expected_df = pandas.read_csv(path_to_csv, dtype = {"Day": object})


#Use the x.equals(y) function to test both dataframes are identical.
@then(u'the two dataframes should be identical.')
def step_impl(context):
    assert context.df.equals(context.expected_df), "{} \n\ntransform dataframe is not identcial to expected CSV dataframe \n\n {}\n".format((context.df), (context.expected_df))

    #if context.df.equals(context.expected_df):
    #    step = "Success"

    #else:
    #    raise NotImplementedError(u'STEP: Then the two dataframes should be identical.')