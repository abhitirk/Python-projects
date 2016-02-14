class SinglyLinkedNode(object):
    """
    Singly Linked Node class
    """
    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):
    """
    Singly Linked List class
    """
    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self._head = None
        pass

    def len(self):
        """
        Returns length/size of the linked list
        :return: length
        """
        length = 0
        node = self._head
        while node is not None:
            length += 1
            node = node._next
        return length
        pass

    def iter(self):
        """
        prints all elements in List starting from head
        """
        node = self._head
        while node is not None:
            print node._item,
            node = node._next
        pass

    def getvalue(self, key):
        """
        Chained hash table operation - get value related to a key from a node
        :param key: input sent from user
        :return: value of key if found, else -1
        """
        node = self._head
        while node is not None:
            [(k, v)] = node._item.items()
            if k == key:
                return v
            node = node._next
        return -1
        pass

    def contains(self, key):
        """
        chained hash table operation - check if key is present
        :param key: input sent from user
        :return: 1 - if key is found in Bin, 0 otherwise
        """
        node = self._head
        while node is not None:
            [(k, v)] = node._item.items()
            if k == key:
                    return 1
            node = node._next
        return 0
        pass

    def containsitem(self, item):
        """
        linked list operation - check if item is in the list
        :param item: sent from user
        :return: 1 if found in the List, 0 otherwise
        """
        node = self._head
        while node is not None:
            if item == node._item:
                    return 1
            node = node._next
        return 0
        pass

    def remove(self, key):
        """
        Deletion for Chained Hash Table operation
        :param key: input sent from user
        :return: 1 - Deletion successful, 0 - Key not found
        """
        node = self._head
        prev_node = None
        while node is not None:
            [(k, v)] = node._item.items()
            if k == key:
                if prev_node is not None:
                    prev_node._next = node._next
                else:
                    self._head = node._next
                return 1
            prev_node = node
            node = node._next
        return 0
        pass

    def removeitem(self, item):
        """
        Deletion for singly linked list operation
        :param item: input from user
        :return: 1 - Deletion successful, 0 - Key not found
        """
        node = self._head
        prev_node = None
        while node is not None:
            if item == node._item:
                if prev_node is not None:
                    prev_node._next = node._next
                else:
                    self._head = node._next
                return 1
            prev_node = node
            node = node._next
        return 0
        pass

    def prepend(self, item):
        """
        Prepend item at beginning of list
        :param item:
        :return:
        """
        node = SinglyLinkedNode(item, self._head)
        self._head = node
        pass

    def __repr__(self):
        s = "List:" + "->".join([item for item in self])
        return s


class ChainedHashDict(object):
    """
    Chained Hash Table of Dictionaries
    """
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self._slot = {}
        self._max_load = max_load
        self._hashfunc = hashfunc
        self._bincount = bin_count
        for i in range(bin_count):
            self._slot[i] = SinglyLinkedList()
        pass

    @property
    def load_factor(self):
        """
        Obtain the current load factor
        """
        n = 0
        bincount = self._bincount
        for i in range(bincount):
            n += self._slot[i].len()
        m = len(self._slot)
        loadfactor = n/float(m)
        return loadfactor
        pass

    @property
    def bin_count(self):
        """
        Returns the current bin count
        """
        return len(self._slot)
        pass

    def rebuild(self, bincount):
        """
        Rebuild this hash table with a new bin count
        """
        self._bincount = bincount
        for i in range(bincount):
            self._slot[i] = SinglyLinkedList()
        pass

    def __getitem__(self, key):
        """
        Get value of a particular key
        """
        hashvalue = self._hashfunc(key) % self._bincount
        item = self._slot[hashvalue].getvalue(key)
        return item
        pass

    def __setitem__(self, key, value):
        """
        Enter a key-value pair into a slot in the table
        """
        hashvalue = self._hashfunc(key) % self._bincount
        data = {key: value}
        self._slot[hashvalue].prepend(data)
        pass

    def __delitem__(self, key):
        """
        Delete an item associated with a certain key
        """
        hashvalue = self._hashfunc(key) % self._bincount
        remove_flag = self._slot[hashvalue].remove(key)
        if remove_flag == 1:
            return "Item with key %s is removed successfully..." % key
        else:
            return "Error - key does not exist in table..."
        pass

    def __contains__(self, key):
        """
        Check if hash table contains an item associated with a key
        """
        hashvalue = self._hashfunc(key) % self._bincount
        contains_flag = self._slot[hashvalue].contains(key)
        if contains_flag == 1:
            return 1
        else:
            return 0
        pass

    def __len__(self):
        """
        Returns the length of the table, i.e, number of items present
        """
        length = 0
        bincount = self._bincount
        for i in range(bincount):
            length += self._slot[i].len()
        return length
        pass

    def display(self):
        """
        shows which items are in which bins
        """
        for i in range(0, self._bincount):
            print "Bin %d -- " % (i+1),
            self._slot[i].iter()
            print ""
        pass


class OpenAddressHashDict(object):
    """
    Open Addressing Hash Table
    """
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        """
        Initialize
        :param bin_count: no. of bins
        :param max_load: maximum load factor
        :param hashfunc: hash function to be used
        """
        super(OpenAddressHashDict, self).__init__()
        self._slot = {}
        self._max_load = max_load
        self._hashfunc = hashfunc
        self._bincount = bin_count
        for i in range(bin_count):
            self._slot[i] = None
        pass
        pass

    @property
    def load_factor(self):
        """
        Obtain the current load factor
        """
        n = self.__len__()
        m = len(self._slot)
        loadfactor = n/float(m)
        return loadfactor
        pass

    @property
    def bin_count(self):
        """
        Returns the current bin count
        """
        return len(self._slot)
        pass

    def rebuild(self, bincount):
        """
        Rebuild this hash table with a new bin count
        """
        self._bincount = bincount
        for i in range(bincount):
            self._slot[i] = None
        pass

    def __getitem__(self, key):
        """
        Get value of a particular key
        """
        for i in range(self._bincount):
            hashvalue = (self._hashfunc(key)+i) % self._bincount
            if self._slot[hashvalue] is None:
                return None
            else:
                [(k, v)] = self._slot[hashvalue].items()
                if key == k:
                    return v
        return None
        pass

    def __setitem__(self, key, value):
        """
        Enter a key-value pair into a slot in the table
        """
        data = {key: value}
        for i in range(self._bincount):
            hashvalue = (self._hashfunc(key)+i) % self._bincount
            if (self._slot[hashvalue] is None or self._slot[hashvalue] == 'DELETED'):  # NOQA
                self._slot[hashvalue] = data
                return hashvalue
        return None
        pass

    def __delitem__(self, key):
        """
        Delete an item associated with a certain key
        """
        for i in range(self._bincount):
            hashvalue = (self._hashfunc(key)+i) % self._bincount
            if self._slot[hashvalue] is None:
                return "Error - key does not exist in table..."
            else:
                [(k, v)] = self._slot[hashvalue].items()
                if key == k:
                    self._slot[hashvalue] = 'DELETED'
                    return "Item with key %s is removed successfully..." % key
        return "Error - key does not exist in table..."
        pass

    def __contains__(self, key):
        """
        Check if hash table contains an item associated with a key
        """
        for i in range(self._bincount):
            hashvalue = (self._hashfunc(key)+i) % self._bincount
            if (self._slot[hashvalue] is None) or (self._slot[hashvalue] == 'DELETED'):  # NOQA
                return None
            else:
                [(k, v)] = self._slot[hashvalue].items()
                if key == k:
                    return hashvalue
        return None
        pass

    def __len__(self):
        """
        Returns the length of the table, i.e, number of items present
        """
        length = 0
        bincount = self._bincount
        for i in range(bincount):
            if self._slot[i] is not None:
                length += 1
        return length
        pass

    def display(self):
        """
        shows which items are in which bins
        """
        for i in range(0, self._bincount):
            print "Bin %d -- " % (i+1),
            print self._slot[i]
        pass


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):
    """
    Dictionary with a Binary Search Tree structure
    """
    def __init__(self):
        """
        Initialize with setting tree root to NIL
        """
        super(BinarySearchTreeDict, self).__init__()

        self._root = None
        pass

    def height(self, node):
        """
        returns height of the tree
        """
        if node is None:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1
        pass

    def tree_minimum(self, node):
        """
        Returns the node with the minimum key
        """
        while node.left is not None:
            node = node.left
        return node
        pass

    def transplant(self, u, v):
        """
        Transplant nodes during deletion
        """
        if u.parent is None:
            self._root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent
        pass

    def inorder_keys(self):
        """
        Yield keys in the tree using INORDER traversal
        """
        stack = []
        current = self._root
        while True:
            try:
                while current is not None:
                    stack.append(current)
                    current = current.left
                if not stack:
                    return
                current = stack.pop()
                [(k, v)] = current.data.items()
                yield k
                while current.right is None and stack:
                    current = stack.pop()
                    [(k, v)] = current.data.items()
                    yield k
                current = current.right
            except StopIteration:
                raise Exception("Error - not all items were yielded")
        pass

    def postorder_keys(self):
        """
        Yield keys in the tree using POSTORDER traversal
        """
        stack = []
        current = self._root
        while True:
            try:
                while current is not None:
                    stack.append((current, False))
                    current = current.left
                if stack:
                    current, visited = stack.pop()
                    [(k, v)] = current.data.items()
                else:
                    return
                while (current.right is None) or (visited is True):
                    yield k
                    current, visited = stack.pop()
                    [(k, v)] = current.data.items()
                else:
                    if not stack and visited:
                        [(k, v)] = current.data.items()
                        yield k
                        return
                    stack.append((current, True))
                    current = current.right
            except StopIteration:
                raise Exception("Error - not all items were yielded")
        pass

    def preorder_keys(self):
        """
        Yield keys in the tree using PREORDER traversal
        """
        stack = []
        current = self._root
        while True:
            try:
                while current is not None:
                    [(k, v)] = current.data.items()
                    yield k
                    stack.append(current)
                    current = current.left
                if not stack:
                    return
                current = stack.pop()
                while current.right is None and stack:
                    current = stack.pop()
                current = current.right
            except StopIteration:
                raise Exception("Error - not all items were yielded")
        pass

    def items(self):
        """
        an INORDER traversal where both key-value pairs are yield
        """
        stack = []
        current = self._root
        while True:
            try:
                while current is not None:
                    stack.append(current)
                    current = current.left
                if not stack:
                    return
                current = stack.pop()
                yield current.data
                while current.right is None and stack:
                    current = stack.pop()
                    yield current.data
                current = current.right
            except StopIteration:
                raise Exception("Error - not all items were yielded")
        pass

    def getnode(self, key):
        """
        Find node associated with a key
        """
        stack = []
        current = self._root
        while True:
            while current is not None:
                stack.append(current)
                current = current.left
            if not stack:
                return
            current = stack.pop()
            [(k, v)] = current.data.items()
            if k == key:
                return current
            while current.right is None and stack:
                current = stack.pop()
                [(k, v)] = current.data.items()
                if k == key:
                    return current
            current = current.right
        pass

    def __getitem__(self, key):
        """
        Find value associated with a key in a node within the tree
        """
        stack = []
        current = self._root
        while True:
            while current is not None:
                stack.append(current)
                current = current.left
            if not stack:
                return
            current = stack.pop()
            [(k, v)] = current.data.items()
            if k == key:
                yield v
            while current.right is None and stack:
                current = stack.pop()
                [(k, v)] = current.data.items()
                if k == key:
                    yield v
            current = current.right
        pass

    def __setitem__(self, key, value):
        """
        Insert a key-value pair into the tree
        """
        data = {key: value}
        [(k, v)] = data.items()
        x = self._root
        print x
        y = None
        while x is not None:
            y = x
            [(xkey, xval)] = x.data.items()
            print "xkey: %d " % int(xkey)
            if int(k) < int(xkey):
                print "probe left of x=%d" % int(xkey)
                x = x.left
            else:
                print "probe right of x=%d" % int(xkey)
                x = x.right
        z = BinaryTreeNode(data, None, None, y)
        if y is None:
            print "Inserting at root"
            self._root = BinaryTreeNode(data, None, None, None)
        else:
            [(ykey, yval)] = y.data.items()
            print "ykey: %d " % int(ykey)
            if int(k) < int(ykey):
                print "Inserting left of y=%d" % int(ykey)
                y.left = z
            else:
                print "Inserting right of y=%d" % int(ykey)
                y.right = z
        pass

    def __delitem__(self, key):
        """
        Delete a node associated with a key in the tree
        """
        z = self.getnode(key)
        if z is not None:
            if z.left is None:
                self.transplant(z, z.right)
            elif z.right is None:
                self.transplant(z, z.left)
            else:
                y = self.tree_minimum(z.right)
                if y.parent != z:
                    self.transplant(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self.transplant(z, y)
                y.left = z.left
                y.left.parent = y
            return True
        return False
        pass

    def __contains__(self, key):
        """
        Check if tree contains a node with a certain key
        """
        stack = []
        current = self._root
        while True:
            while current is not None:
                stack.append(current)
                current = current.left
            if not stack:
                return False
            current = stack.pop()
            [(k, v)] = current.data.items()
            if k == key:
                return True
            while current.right is None and stack:
                current = stack.pop()
                [(k, v)] = current.data.items()
                if k == key:
                    return True
            current = current.right
        return False
        pass

    def __len__(self):
        """
        Returns no. of items in the tree
        :return: a variable containing the number of items in the tree
        """
        length = 0
        stack = []
        current = self._root
        while True:
            while current is not None:
                stack.append(current)
                current = current.left
            if not stack:
                return length
            current = stack.pop()
            length += 1
            while current.right is None and stack:
                current = stack.pop()
                length += 1
            current = current.right
        pass

    def display(self):
        """
        Display the tree using both Inorder and Preorder
        traversal in two seperate lines
        """
        inorderkeys = self.inorder_keys()
        print "INORDER TRAVERSAL: ",
        for i in inorderkeys:
            print i,
        preorderkeys = self.preorder_keys()
        print "\nPREORDER TRAVERSAL: ",
        for i in preorderkeys:
            print i,
        pass


def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """
    def hashfunc(item):
        return bin
    return hashfunc


def main():
    while True:
        print "Choose among the following options: \n "
        print "1-Singly Linked List \n2-Chained Hash Dictionary \n3-Open Addressing Hash Dictionary \n4-Binary Search Tree \n0 - Exit program"  # NOQA
        opt = input("Enter your option: ")
        if opt == 0:
            break
        elif opt == 1:
            sll = SinglyLinkedList()
            while True:
                if sll.len() > 0:
                    print "Choose among the following options: "
                    print "1-Insert items (prepend)"
                    print "2-Display list contents (iterate)"
                    print "3-Check if it contains an item"
                    print "4-Delete item"
                    print "5-Display length of list"
                    print "0-Exit Linked List operations"
                    c_opt = input("Enter your choice:")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter items till you're done (blank to go back): "  # NOQA
                        while True:
                            item = raw_input("Enter item (blank to exit): ")
                            if item == '':
                                break
                            sll.prepend(item)
                    elif c_opt == 2:
                        print "Displaying list contents: ",
                        sll.iter()
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 3:
                        item = raw_input("Enter item to check if it exists in the list: ")  # NOQA
                        if sll.containsitem(item) == 0:
                            print "Sorry, the list does not contain that item."
                        else:
                            print "Yes! The list does contain that item."
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 4:
                        item = raw_input("Enter the item that has to be removed: ")  # NOQA
                        if sll.removeitem(item) == 1:
                            print "Item successfully deleted..."
                        else:
                            print "Error - item to be deleted not found"
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 5:
                        print "The length of the list is: %d " % sll.len()
                        raw_input("\nPress Enter to continue...")
                else:
                    insert_opt = raw_input("List is empty. Press enter to start inserting values (Enter 0 to exit):")  # NOQA
                    if insert_opt == '0':
                        break
                    else:
                        print "Enter items till you're done (blank to go back): "  # NOQA
                        while True:
                            item = raw_input("Enter item (blank to exit): ")
                            if item == '':
                                break
                            sll.prepend(item)

        elif opt == 2:
            c = ChainedHashDict()
            while True:
                if c.__len__() > 0:
                    print "Choose among the following options: "
                    print "1-Insert"
                    print "2-Get a value"
                    print "3-Check if present in table"
                    print "4-Delete item"
                    print "5-Display entire table with contents"
                    print "6-Rebuild the table with a new bin count"
                    print "7-Show current bin count"
                    print "8-Show current load factor"
                    print "0-Exit Chained Hash Table operations"
                    c_opt = input("Enter your choice:")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter the keys and the respective values till you're done. (Enter blank to go back anytime)"  # NOQA
                        while True:
                            loadfactor_current = c.load_factor
                            if loadfactor_current == c._max_load:
                                print "Maximum load reached! "
                                print "Do you want to continue adding items? This will change increase the table size."  # NOQA
                                choice = raw_input("y/n?")
                                if choice == 'y':
                                    currentbincount = c._bincount
                                    newbincount = c._bincount * 2
                                    for i in range(currentbincount, newbincount):  # NOQA
                                        c._slot[i] = SinglyLinkedList()
                                    c._bincount = newbincount
                                    print "Table size has been doubled to: %d" % c.bin_count  # NOQA
                                else:
                                    break
                            insertkey = raw_input("Enter key (blank to exit): ")  # NOQA
                            if insertkey == '':
                                break
                            insertval = raw_input("Enter value (blank to exit): ")  # NOQA
                            if insertval == '':
                                break
                            c.__setitem__(insertkey, insertval)
                            loadfactor_current = c.load_factor
                            print "Current Load Factor: %.2f" % loadfactor_current  # NOQA
                            print "Maximum Load Factor: %.2f" % c._max_load
                            if loadfactor_current == c._max_load:
                                print "WARNING! Maximum load reached!"

                    elif c_opt == 2:
                        key = raw_input("Enter key to retrieve value: ")
                        value = c.__getitem__(key)
                        if value == -1:
                            print "Table does not contain an item with that key!"  # NOQA
                        else:
                            print "The value of the entered key is: %s" % value  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 3:
                        key = raw_input("Enter key to check if it exists: ")  # NOQA
                        if c.__contains__(key) == 0:
                            print "Sorry, the table does not contain an item with that key"  # NOQA
                        else:
                            print "Yes! Table does contain an item with that key..."  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 4:
                        key = raw_input("Enter key to delete that item")
                        print c.__delitem__(key)
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 5:
                        print "Displaying the entire table with its contents:\n"  # NOQA
                        c.display()
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 6:
                        rebuild_opt = input("Are you sure you want to rebuild the table? 1-yes, 0-no")  # NOQA
                        if rebuild_opt == 1:
                            bincount = input("Enter the number of bins in the new table")  # NOQA
                            if bincount > 0 and bincount < 100:
                                c = ChainedHashDict()
                                c.rebuild(bincount)
                                print "Hash table rebuilt successfully with %d bins" % bincount  # NOQA
                            else:
                                print "Please enter a value between 0 and 100"  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 7:
                        print "The current number of bins is: %d" % c.bin_count  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 8:
                        print "The current Load Factor is: %.2f" % c.load_factor  # NOQA
                        raw_input("\nPress Enter to continue...")
                else:
                    print "Hash Table is empty. Choose one of the following options: "  # NOQA
                    print "1-Insert a value"
                    print "2-Rebuild the table with a new bin count"
                    print "3-Show current bin count"
                    print "4-Use Terrible Hash function"
                    print "0-Exit Chained Hash Table operations"
                    c_opt = input("Enter your choice: ")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter the keys and the respective values till you're done. (Enter blank to go back anytime)"  # NOQA
                        while True:
                            loadfactor_current = c.load_factor
                            if loadfactor_current == c._max_load:
                                print "Maximum load reached! "
                                print "Do you want to continue adding items? This will change increase the table size."  # NOQA
                                choice = raw_input("y/n?")
                                if choice == 'y':
                                    currentbincount = c._bincount
                                    newbincount = c._bincount * 2
                                    for i in range(currentbincount, newbincount):  # NOQA
                                        c._slot[i] = SinglyLinkedList()
                                    c._bincount = newbincount
                                    print "Table size has been doubled to: %d" % c.bin_count  # NOQA
                                else:
                                    break
                            insertkey = raw_input("Enter key (blank to exit): ")  # NOQA
                            if insertkey == '':
                                break
                            insertval = raw_input("Enter value(blank to exit): ")  # NOQA
                            if insertval == '':
                                break
                            print ""
                            c.__setitem__(insertkey, insertval)
                            loadfactor_current = c.load_factor
                            print "Current Load Factor: %.2f" % loadfactor_current  # NOQA
                            print "Maximum Load Factor: %.2f" % c._max_load
                            if loadfactor_current == c._max_load:
                                print "WARNING! Maximum load reached!"

                    elif c_opt == 2:
                        rebuild_opt = input("Are you sure you want to rebuild the table? 1-yes, 0-no")  # NOQA
                        if rebuild_opt == 1:
                            bincount = input("Enter the number of bins in the new table")  # NOQA
                            if bincount > 0 and bincount < 100:
                                c = ChainedHashDict()
                                c.rebuild(bincount)
                                print "Hash table rebuilt successfully with %d bins" % bincount  # NOQA
                            else:
                                print "Please enter a value between 0 and 100"  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 3:
                        print "The current number of bins is: %d" % c.bin_count  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 4:
                        end_of_table = c.bin_count - 1
                        c._hashfunc = terrible_hash(end_of_table)
                        print "Terrible hash function is set. Items will always map to end of table"  # NOQA

        elif opt == 3:
            c = OpenAddressHashDict()
            while True:
                if c.__len__() > 0:
                    print "Choose among the following options: "
                    print "1-Insert"
                    print "2-Get a value"
                    print "3-Check if present in table"
                    print "4-Delete item"
                    print "5-Display entire table with contents"
                    print "6-Rebuild the table with a new bin count"
                    print "7-Show current bin count"
                    print "8-Show current load factor"
                    print "0-Exit Open Addressing Hash Table operations"
                    c_opt = input("Enter your choice:")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter the keys and the respective values till you're done. (Enter blank to go back anytime)"  # NOQA
                        while True:
                            loadfactor_current = c.load_factor
                            if loadfactor_current >= c._max_load:
                                print "Maximum load reached! "
                                print "Do you want to continue adding items? This will change increase the table size."  # NOQA
                                choice = raw_input("y/n?")
                                if choice == 'y':
                                    currentbincount = c._bincount
                                    newbincount = c._bincount * 2
                                    for i in range(currentbincount, newbincount):  # NOQA
                                        c._slot[i] = None
                                    c._bincount = newbincount
                                    print "Table size has been doubled to: %d" % c.bin_count  # NOQA
                                else:
                                    break
                            insertkey = raw_input("Enter key (blank to exit): ")  # NOQA
                            if insertkey == '':
                                break
                            insertval = raw_input("Enter value (blank to exit): ")  # NOQA
                            if insertval == '':
                                break
                            c.__setitem__(insertkey, insertval)
                            loadfactor_current = c.load_factor
                            print "Current Load Factor: %.2f" % loadfactor_current  # NOQA
                            print "Maximum Load Factor: %.2f" % c._max_load
                            if loadfactor_current >= c._max_load:
                                print "WARNING! Maximum load reached!"

                    elif c_opt == 2:
                        key = raw_input("Enter key to retrieve value: ")
                        value = c.__getitem__(key)
                        if value is None:
                            print "Table does not contain an item with that key!"  # NOQA
                        else:
                            print "The value of the entered key is: %s" % value  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 3:
                        key = raw_input("Enter key to check if it exists: ")  # NOQA
                        contains = c.__contains__(key)
                        if contains is None:
                            print "Sorry, the table does not contain an item with that key"  # NOQA
                        else:
                            print "Yes! Table does contain an item with that key in position: %d" % (contains + 1)  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 4:
                        key = raw_input("Enter key to delete that item")
                        print c.__delitem__(key)
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 5:
                        print "Displaying the entire table with its contents:\n"  # NOQA
                        c.display()
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 6:
                        rebuild_opt = input("Are you sure you want to rebuild the table? 1-yes, 0-no")  # NOQA
                        if rebuild_opt == 1:
                            bincount = input("Enter the number of bins in the new table")  # NOQA
                            if bincount > 0 and bincount < 100:
                                c = OpenAddressHashDict()
                                c.rebuild(bincount)
                                print "Hash table rebuilt successfully with %d bins" % bincount  # NOQA
                            else:
                                print "Please enter a value between 0 and 100"  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 7:
                        print "The current number of bins is: %d" % c.bin_count  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 8:
                        print "The current Load Factor is: %.2f" % c.load_factor  # NOQA
                        raw_input("\nPress Enter to continue...")
                else:
                    print "Hash Table is empty. Choose one of the following options: "  # NOQA
                    print "1-Insert a value"
                    print "2-Rebuild the table with a new bin count"
                    print "3-Show current bin count"
                    print "4-Use terrible hash function"
                    print "0-Exit Open Addressing Hash Table operations"
                    c_opt = input("Enter your choice: ")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter the keys and the respective values till you're done. (Enter blank to go back anytime)"  # NOQA
                        while True:
                            loadfactor_current = c.load_factor
                            if loadfactor_current >= c._max_load:
                                print "Maximum load reached! "
                                print "Do you want to continue adding items? This will change increase the table size."  # NOQA
                                choice = raw_input("y/n?")
                                if choice == 'y':
                                    currentbincount = c._bincount
                                    newbincount = c._bincount * 2
                                    for i in range(currentbincount, newbincount):  # NOQA
                                        c._slot[i] = None
                                    c._bincount = newbincount
                                    print "Table size has been doubled to: %d" % c.bin_count  # NOQA
                                else:
                                    break
                            insertkey = raw_input("Enter key (blank to exit): ")  # NOQA
                            if insertkey == '':
                                break
                            insertval = raw_input("Enter value(blank to exit): ")  # NOQA
                            if insertval == '':
                                break
                            print ""
                            c.__setitem__(insertkey, insertval)
                            loadfactor_current = c.load_factor
                            print "Current Load Factor: %.2f" % loadfactor_current  # NOQA
                            print "Maximum Load Factor: %.2f" % c._max_load  # NOQA
                            if loadfactor_current >= c._max_load:
                                print "WARNING! Maximum load reached!"  # NOQA

                    elif c_opt == 2:
                        rebuild_opt = input("Are you sure you want to rebuild the table? 1-yes, 0-no")  # NOQA
                        if rebuild_opt == 1:
                            bincount = input("Enter the number of bins in the new table")  # NOQA
                            if bincount > 0 and bincount < 100:
                                c = OpenAddressHashDict()
                                c.rebuild(bincount)
                                print "Hash table rebuilt successfully with %d bins" % bincount  # NOQA
                            else:
                                print "Please enter a value between 0 and 100"  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 3:
                        print "The current number of bins is: %d" % c.bin_count  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 4:
                        end_of_table = c.bin_count - 1
                        c._hashfunc = terrible_hash(end_of_table)
                        print "Terrible hash function is set. Items will always map from end of table"  # NOQA
        elif opt == 4:
            bst = BinarySearchTreeDict()
            while True:
                if bst.__len__() > 0:
                    print "Choose among the following options: "
                    print "1-Insert a new item into the tree"
                    print "2-Inorder Traversal"
                    print "3-Preorder Traversal"
                    print "4-Postorder Traversal"
                    print "5-Height of the tree"
                    print "6-Get items (key and value)"
                    print "7-Get value associated with Key"
                    print "8-Delete item associated with Key"
                    print "9-Check if tree contains a certain Key"
                    print "10-Obtain length, i.e. no of items in Tree"
                    print "11-Display all keys (inorder and preorder)"
                    print "0-Exit Binary Search Tree Operations"
                    c_opt = input("Enter your choice:")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter the keys and the respective values till you're done. (Enter blank to go back anytime)"  # NOQA
                        while True:
                            insertkey = raw_input("Enter key (blank to exit): ")  # NOQA
                            if insertkey == '' or insertkey == 0:
                                break
                            insertval = raw_input("Enter value (blank to exit): ")  # NOQA
                            if insertval == '':
                                break
                            bst.__setitem__(insertkey, insertval)
                    elif c_opt == 2:
                        inorderkeys = bst.inorder_keys()
                        print "INORDER TRAVERSAL: "
                        for i in inorderkeys:
                            print i,
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 3:
                        preorderkeys = bst.preorder_keys()
                        print "PREORDER TRAVERSAL: "
                        for i in preorderkeys:
                            print i,
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 4:
                        postorderkeys = bst.postorder_keys()
                        print "POSTORDER TRAVERSAL: "
                        for i in postorderkeys:
                            print i,
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 5:
                        node = bst._root
                        height = bst.height(node)
                        print "The height of the tree is: %d " % height
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 6:
                        inorderitems = bst.items()
                        print "ALL ITEMS IN INORDER TRAVERSAL: "
                        for i in inorderitems:
                            print i,
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 7:
                        itemkey = raw_input("Enter key (blank to exit): ")  # NOQA
                        if itemkey == '' or itemkey == 0:
                            break
                        value = bst.__getitem__(itemkey)
                        print "Values with key %s are as follows: " % itemkey  # NOQA
                        for i in value:
                            print i,
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 8:
                        delkey = raw_input("Enter key (blank to exit): ")  # NOQA
                        if delkey == '' or delkey == 0:
                            break
                        if bst.__delitem__(delkey):
                            print "Item with key: %s is successfully deleted from tree..." % delkey  # NOQA
                        else:
                            print "Error - key not found in tree!"
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 9:
                        searchkey = raw_input("Enter key (blank to exit): ")  # NOQA
                        if searchkey == '' or searchkey == 0:
                            break
                        if bst.__contains__(searchkey):
                            print "Item with key: %s was found!..." % searchkey  # NOQA
                        else:
                            print "Key not found in tree!"
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 10:
                        length = bst.__len__()
                        print "The no. of items in the tree is: %d" % length  # NOQA
                        raw_input("\nPress Enter to continue...")
                    elif c_opt == 11:
                        bst.display()
                        raw_input("\nPress Enter to continue...")
                else:
                    print "Tree is empty. Choose one of the following options: "  # NOQA
                    print "1-Insert a value"
                    print "0-Exit Binary Search Tree operations"
                    c_opt = input("Enter your choice: ")
                    if c_opt == 0:
                        break
                    elif c_opt == 1:
                        print "Enter the keys and the respective values till you're done. (Enter blank to go back anytime)"  # NOQA
                        while True:
                            insertkey = raw_input("Enter key (blank to exit): ")  # NOQA
                            if insertkey == '' or insertkey == 0:
                                break
                            insertval = raw_input("Enter value (blank to exit): ")  # NOQA
                            if insertval == '':
                                break
                            bst.__setitem__(insertkey, insertval)
pass

main()
