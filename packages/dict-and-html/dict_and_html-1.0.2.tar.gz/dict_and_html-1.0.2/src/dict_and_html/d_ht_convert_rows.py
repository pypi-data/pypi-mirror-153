# d_ht_convert_rows.py

# Is it possible to inherit html_and_py from dict_and_html?
# import html_and_py for creating HTML
# import strategies to extend behavior

from html_and_py import *
from strategies import *


# todo (2) Based on previous analysis (1), this is another independent module
#  that prints a Python dict as <tr> rows of an HTML <table>, eventually with
#  nested <table>'s. As it turns out, this is a headless <table>, meaning
#  that the origin <table> (with <thead> and <tbody>) is written before this
#  module. Currently, it is dict_and_html.py that calls
#  convert_dict_rows_into_table_rows; in fact, it is calling a converter from
#  dict_rows into table_rows, and it's saving its output in a <tbody>
#  element. This is done from the dict_and_html.py module. This module is
#  generic as well: it works on any Python dict, not just a JSON dict. The
#  dict_and_html.py module is called by json_and_html_table.py. What should
#  really happen here is that json_and_html_table.py calls dict_and_html.py (
#  currently dict_and_html.py) and passes the desired strategies;
#  dict_and_html.py adapts its output based on the strategies received.
# todo (1) Is this just a dictionary-to-html-table conversion? If so, this could
#  be a separate module for just dictionary-to-table conversion. Then,
#  dict_and_html could be using this dict-to-html-table module with its own
#  settings. And other projects could also benefit from their own
#  specification on how to convert the dictionary into a table; for example,
#  adding id's and href's based on certain rules. It can be added with an
#  "attribute strategy for keys and values", which is an application of the
#  strategy design pattern. According to this, I could extend the
#  functionality of the code that brings table rows to life, specifically
#  table columns for each row. Attributes will be set according to the output
#  from the "attribute strategy". The context for the strategy are keys and
#  values, so these need to be passed. It can be split into strategy for keys
#  and strategy for values. This way, there are two smaller contexts, one for
#  keys and one for values as well. Each strategy outputs what the attributes
#  should look like, parametrized by the input key or value. For example,
#  and id or href attribute could be set based on the context for the key or
#  value. Another approach for this idea is to create a module that traverses
#  an HTML <table> and adds the id and href attributes to keys and values
#  respectively if it finds matches. The problem with this approach is that
#  multiple id's can exist. It all depends on the domain of the input data.
#  Hence, instead of creating a general id-href-walker module for all HTML
#  <table>'s possible, it's best to start from data that has a certain
#  meaning, data from a certain domain, and specify what behavior the
#  attribute should assume in correspondence of certain values of keys and
#  values. It seems a good fit for the strategy design pattern. Note that
#  this very file d_ht_convert_rows.py could be considered the default
#  strategy. Though, it's pretty likely that every child strategy would
#  benefit from already putting dictionary keys and values in <td> elements.
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

        # todo (1) Based on previous analysis, the module can be a more
        #  general dict-to-html-table conversion. It could be an extensible
        #  module in regard to how to convert keys and values. For
        #  example, here there could be a callback to an extension library
        #  which can be programmed to perform actions based on the value
        #  of the keys. E.g. if the key matches a certain pattern, then add
        #  an id attribute to its wrapper <td> element.
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
