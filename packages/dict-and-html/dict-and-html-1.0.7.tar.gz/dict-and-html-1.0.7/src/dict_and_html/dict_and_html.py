# dict_and_html.py

# import html_and_py to create HTML
# import d2ht_convert_rows submodule

from html_and_py import *
# from d_ht_convert_rows import convert_dict_rows_into_table_rows


###########################
# strategy_keys.py
###########################
def attribute_strategy_for_key(key,
                               key_strategy: dict = None) -> dict:
    attributes = {}

    if key_strategy is None:
        # print("default key strategy", len([key]))
        len([key])  # just to avoid triggering warnings
    else:
        ##
        # Example of strategy
        ##
        # if type(key) == float:
        #     attributes.update({
        #         'style': 'font-style: italic;'
        #     })
        # else:
        #     print("Not float: %s" % key)
        pass

    return attributes
###########################
# strategy_keys.py
###########################


###########################
# strategy_values.py
###########################
def attribute_strategy_for_value(value,
                                 value_strategy: dict = None) -> dict:
    attributes = {}

    if value_strategy is None:
        # print("default value strategy", len([value]))
        len([value])  # just to avoid triggering warnings
    else:
        ##
        # Example of strategy
        ##
        # if type(value) == float:
        #     attributes.update({
        #         'style': 'font-style: italic;'
        #     })
        # else:
        #     print("Not float: %s" % value)
        pass

    return attributes
###########################
# strategy_value.py
###########################


###########################
# d_ht_convert_rows.py
###########################
# Is it possible to inherit html_and_py from dict_and_html?
# import html_and_py for creating HTML
# import strategies to extend behavior
# from html_and_py import *
# from strategy_keys import attribute_strategy_for_key
# from strategy_values import attribute_strategy_for_value
###########################
# d_ht_convert_rows.py
###########################

DOCTYPE = init_doctype("html")
TABLE_STYLE = """table,
table * {
  border: solid black 1px;
  border-collapse: collapse;
}"""
HTML_STYLE = create_html({
    'tag': 'style',
    'text': TABLE_STYLE
})


###########################
# d_ht_convert_rows.py
###########################
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
###########################
# d_ht_convert_rows.py
###########################


def dict_and_html(source_dictionary: dict,
                  table_root_name: str = 'Dict And Html Table',
                  attribute_strategies: dict = None) -> str:
    """
    It converts the source_dictionary into an HTML table, wrapping it in a
    complete HTML page. If a name is passed to table_root_name, it will be
    printed in the header <thead> of the table. It can be passed a set of
    strategies in attribute_strategies to include additional processing in
    the conversion of the key-value pair from the source_dictionary into a
    row of the HTML table. All that needs to be done to enable this feature
    is to pass an extra argument to dict_and_html to specify the strategies
    to apply. These strategies have not been coded yet.

    :param source_dictionary: Input Python dictionary
    :param table_root_name: Text for the header of the HTML table
    :param attribute_strategies: Python dictionary to select a strategy of
    processing for key-value pairs in the source_dictionary
    :return: An HTML-formatted string representing an HTML page containing the
    table conversion of the source_dictionary
    """
    output = "" + DOCTYPE

    table_children = []
    table_header = create_html({
        'tag': 'thead',
        'children': [
            create_html({
                'tag': 'tr',
                'children': [
                    create_html({
                        'tag': 'th',
                        'text': table_root_name
                    })
                ]
            })
        ]
    })
    table_children.append(table_header)
    table_body = create_html({
        'tag': 'tbody',
        'children': convert_dict_rows_into_table_rows(
            source_dictionary,
            attribute_strategies
        )
    })
    table_children.append(table_body)

    # print(table_header)
    # print(table_body)

    html_page = create_html({
        'tag': 'html',
        'children': [
            create_html({
                'tag': 'head',
                'children': [HTML_STYLE]
            }),  # head
            create_html({
                'tag': 'body',
                'children': [
                    create_html({
                        'tag': 'table',
                        'children': [
                            table_header,
                            table_body
                        ]
                    })  # table
                ]
            })  # body
        ]
    })

    # print("  >>  Printing html_page")
    # print(html_page)
    # print("  >>  Rendering html_page")
    # print(render_html(html_page))

    output += render_html(html_page)
    return output
