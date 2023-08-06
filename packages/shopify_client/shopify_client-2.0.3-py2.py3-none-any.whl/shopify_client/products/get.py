import shopify

from .schema import ProductsInput


class ProductGet:
    def get(self, products_input):
        response = shopify.GraphQL().execute(self.get_query(), self.get_variables(products_input))
        return response

    def get_query(self):
        return '''
            query GetProducts($first: Int, $last: Int, $after: String, $before: String, $reverse: Boolean, $query: String, $metafieldsFirst: Int, $namespace: String){   
                products(first: $first, last: $last, after: $after, before: $before, reverse: $reverse, query: $query) {
                    edges {
                        cursor
                        node {
                            id
                            title
                            handle
                            status
                            productType
                            tags
                            metafields(first: $metafieldsFirst, namespace: $namespace) {
                                edges {
                                    node {
                                        id
                                        key
                                        value
                                    }
                                } 
                            }
                        }
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                    }    
                }
            }
        '''

    def get_variables(self, products_input: ProductsInput):
        return {
            'first': products_input.first,
            'last': products_input.last,
            'after': products_input.after,
            'before': products_input.before,
            'reverse': products_input.reverse,
            'query': products_input.query,
            'metafieldsFirst': products_input.metafields_first,
            'namespace': products_input.metafields_namespace
        }
