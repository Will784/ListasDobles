from Models.ProductNode import ProductNode


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add_product(self, product):
        node = ProductNode(product)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            node.previous = self.tail
            self.tail.next = node
            self.tail = node
        self.current = node
        self.size += 1
        return node

    def add_after_current(self, product):
        if self.current is None:
            return self.add_product(product)
        node = ProductNode(product)
        following = self.current.next
        node.previous = self.current
        node.next = following
        self.current.next = node
        if following is not None:
            following.previous = node
        else:
            self.tail = node
        self.current = node
        self.size += 1
        return node

    def find_node(self, product_id):
        node = self.head
        while node is not None:
            if node.product.product_id == product_id:
                return node
            node = node.next
        return None

    def remove_product(self, product_id):
        node = self.find_node(product_id)
        if node is None:
            return False
        before = node.previous
        after = node.next
        if before is not None:
            before.next = after
        else:
            self.head = after
        if after is not None:
            after.previous = before
        else:
            self.tail = before
        if self.current is node:
            self.current = after if after is not None else before
        node.previous = None
        node.next = None
        self.size -= 1
        return True

    def search_products(self, text):
        needle = text.strip().lower()
        node = self.head
        while node is not None:
            product = node.product
            if (
                needle in product.name.lower()
                or needle in product.category.lower()
                or needle in product.code.lower()
            ):
                yield node
            node = node.next

    def can_go_previous(self):
        return self.current is not None and self.current.previous is not None

    def can_go_next(self):
        return self.current is not None and self.current.next is not None

    def go_previous(self):
        if not self.can_go_previous():
            return False
        self.current = self.current.previous
        return True

    def go_next(self):
        if not self.can_go_next():
            return False
        self.current = self.current.next
        return True

    def go_to(self, product_id):
        node = self.find_node(product_id)
        if node is None:
            return False
        self.current = node
        return True

    def traverse_forward(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def traverse_backward(self):
        node = self.tail
        while node is not None:
            yield node
            node = node.previous

    def clear(self):
        node = self.head
        while node is not None:
            following = node.next
            node.previous = None
            node.next = None
            node = following
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0
