# d_ht_convert_rows.py

# Is it possible to inherit html_and_py from dict_and_html?
# import html_and_py for creating HTML
# import strategies to extend behavior
from html_and_py import *
from strategies.strategy_keys import attribute_strategy_for_key
from strategies.strategy_values import attribute_strategy_for_value


# Based on previous analysis, this is another independent module that prints
# a Python dict as <tr> rows of an HTML <table>, eventually with nested
# <table>'s As it turns out, this is a headless <table>, meaning that there
# is a wrapper <table> (with <thead> and <tbody>), written before this
# module. Currently, dict_and_html.py calls
# convert_dict_rows_into_table_rows and saves its output in a <tbody> element.
# Other projects can benefit from this package by specifying custom
# strategies of conversion of keys and values. For example, adding id's and
# href's based on certain rules. It can be added with an "attribute strategy
# for keys and values", which is an application of the strategy design
# pattern.  According to this, I could extend the functionality of the code
# that brings table rows to life, specifically table columns for each row.
# Attributes will be set according to the output from the "attribute
# strategy". The context for the strategy are the keys and values of the
# dictionary being converted into table, so these need to be passed. It can
# be split into strategy for keys and strategy for values. This way,
# there are two, smaller contexts. For example, each attribute strategy
# outputs a dictionary object that describes a set of HTML attributes. In
# this example, an id and a href attribute could be set based on the context
# for the key and the value respectively.
def convert_dict_rows_into_table_rows(source_dictionary: dict,
                                      attribute_strategies: dict = None
                                      ) -> [dict]:
    ##
    # Walk through the source dictionary collecting keys and values
    # - For each key, add <tr><td>
    # - For each value,
    #    if value is a singleton, <td> is populated with the value
    #    if value is a nested dict, <td> is populated with a new <table> and a
    #     sub-processing of its keys and values takes place recursively
    #
    # To solve this problem recursively, we need this method to convert each
    # key-value pair of a source dictionary into just the following HTML:
    #   <tr> <td> KEY </td>   <td> VALUE </td> </tr>
    #
    # For nested tables, spawn a new <table> inside the VALUE <td></td>:
    #   <tr>
    #     <td> KEY </td>
    #     <td>
    #     <table> VALUE </table>
    #     </td>
    #   </tr>
    ##
    output_rows = []
    for dict_key, dict_value in source_dictionary.items():
        value_children_table = []
        value_children_text = ''
        if type(dict_value) == dict:
            # print("We have a nested dictionary")
            value_children_table.append(create_html({
                'tag': 'table',
                'children': convert_dict_rows_into_table_rows(dict_value)
            }))
        else:
            # print("We have a singleton value")
            value_children_text = dict_value

        # Attribute strategy design pattern
        key_attributes = attribute_strategy_for_key(
            dict_key,
            key_strategy=attribute_strategies
        )
        value_attributes = attribute_strategy_for_value(
            dict_value,
            value_strategy=attribute_strategies
        )

        key_column = create_html({
            'tag': 'td',
            'attributes': key_attributes,
            'text': dict_key
        })
        value_column = create_html({
            'tag': 'td',
            'attributes': value_attributes,
            'children': value_children_table,
            'text': value_children_text
        })
        current_table_row = create_html({
            'tag': 'tr',
            'children': [
                key_column,
                value_column
            ]
        })
        output_rows.append(current_table_row)
        # print("Current row:")
        # print(current_table_row)

    return output_rows
