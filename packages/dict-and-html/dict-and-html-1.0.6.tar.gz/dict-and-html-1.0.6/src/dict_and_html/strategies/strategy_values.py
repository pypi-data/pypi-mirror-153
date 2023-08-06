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
