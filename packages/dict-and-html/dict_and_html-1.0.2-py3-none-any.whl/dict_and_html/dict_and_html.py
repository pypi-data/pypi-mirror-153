# dict_and_html.py

# import html_and_py to create HTML
# import d2ht_convert_rows submodule

from html_and_py import *
from d_ht_convert_rows import convert_dict_rows_into_table_rows

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


# todo (4) This can become its own Python module.
def dict_and_html(source_dictionary: dict,
                  table_root_name: str = 'Dict And Html Table',
                  attribute_strategies: dict = None) -> str:
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
