import threading
import time
import queue
class Table:
    def __init__(self, number_table):
        self.number = number_table
        self.is_busy = False
class Customer(threading.Thread):
    def __init__(self, number_costumer, caffe):
        self.number = number_costumer
        self.cafe = caffe
        super().__init__()

    def run(self):
        table = self.cafe.serve_customer(self)
        time.sleep(1)
        self.cafe.release_table(table)
class Cafe:
    def __init__(self, tabless):
        self.queue = queue.Queue()
        self.tables = tabless
        self.customer_count = 0

    def customer_arrival(self):
        for i in range(1, 21):
            self.customer_count += 1
            customer = Customer(self.customer_count, self)
            customer.start()
            time.sleep(1)

    def serve_customer(self, customer):
        for table in self.tables:
            self.queue.put(table)
            if not table.is_busy:
                table.is_busy = True
                print(f'Посетитель номер {customer.number} сел за стол {table.number}.')
                time.sleep(4)
                print(f'Посетитель номер {customer.number} покушал и ушёл.')
                return table
        print(f'Посетитель номер {customer.number} ожидает свободный стол.')
        self.queue.get(customer)

    def release_table(self, table):
        if not self.queue.empty():
            ojidanie_customer = self.queue.get()
            self.serve_customer(customer=ojidanie_customer)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)
customer_arrival_thread_1 = threading.Thread(target=cafe.customer_arrival)

customer_arrival_thread_1.start()
customer_arrival_thread_1.join()