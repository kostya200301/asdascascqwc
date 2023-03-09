from random import randint
from datetime import datetime

def get_map(tick):
    return {"seccode": tick.seccode, "price": tick.price, "quantity": tick.quantity, "tradetime": tick.tradetime}

class Node:
    def __init__(self, data):
        self.item = data
        self.nref = None
        self.pref = None

class DoublyLinkedList:
    def __init__(self):
        self.start_node = None
        self.count = 0
        self.end_node = None

    def insert_in_emptylist(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            self.end_node = new_node
            self.count += 1
        else:
            print("list is not empty")

    def insert_at_start(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            self.count += 1
            print("node inserted")
            return
        new_node = Node(data)
        new_node.nref = self.start_node
        self.start_node.pref = new_node
        self.start_node = new_node
        self.count += 1

    def insert_at_end(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            self.end_node = new_node
            self.count += 1
            return new_node
        n = self.end_node
        new_node = Node(data)
        n.nref = new_node
        new_node.pref = n
        self.count += 1
        self.end_node = new_node
        return new_node


    def traverse_list(self):
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            while n is not None:
                print(n.item.quantity, " ")
                n = n.nref

    def add_to_file(self):
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            file = open(get_map(n.item)["seccode"] + ".txt", "a")
            while n is not None:
                # print("deal", n.item, n.item.count)
                file.write(str(get_map(n.item)) + "\n")
                n = n.nref
            file.close()

    def add_to_file_start_from_date(self, date):
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            file = open(get_map(n.item)["seccode"] + ".txt", "a")
            while n is not None:
                # print("deal", n.item, n.item.count)
                if (datetime.strptime(n.item.tradetime, '%m.%d.%Y %H:%M:%S') > date):
                    print("add", n.item.tradetime)
                    file.write(str(get_map(n.item)) + "\n")
                n = n.nref
            file.close()

    def delete_at_start(self):
        if self.start_node is None:
            print("The list has no element to delete")
            return
        if self.start_node.nref is None:
            self.count -= 1
            del self.start_node
            self.start_node = None
            return
        to_del_node = self.start_node
        self.start_node = self.start_node.nref
        del to_del_node
        self.count -= 1


    def delete_at_end(self):
        if self.start_node is None:
            print("The list has no element to delete")
            return
        if self.start_node.nref is None:
            self.start_node = None
            self.end_node = None
            self.count -= 1
            return
        n = self.end_node
        n.pref.nref = None
        self.count -= 1
