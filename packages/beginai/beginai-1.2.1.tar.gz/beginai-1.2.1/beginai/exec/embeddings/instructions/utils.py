def sequence_encoder(categories_list):
    """
    get a numerical code for each category.
    """
    categories_list = sorted(categories_list)
    return list(range(1, len(categories_list) + 1))
