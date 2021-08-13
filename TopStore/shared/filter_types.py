def types_filter(products):
    return set((product.type + 's' if product.type != 'Headphones' else product.type) for product in products)
