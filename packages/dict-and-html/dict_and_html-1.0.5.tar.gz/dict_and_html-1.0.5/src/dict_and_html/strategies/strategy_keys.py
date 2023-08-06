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
