def types_filter(products):
    return set((product.type + 's' if product.type != 'Headphones' else product.type).lower() for product in products)
