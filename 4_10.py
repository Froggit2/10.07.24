import threading
import time
import queue
class Table:
    def __init__(self, number_table):
        self.number = number_table
        self.is_busy = False

class Customer(threading.Thread):
    def __init__(self, number_customer, cafe):
        self.number = number_customer
        self.cafe = cafe
        self.table = None
        self.event = threading.Event()
        super().__init__()

    def run(self):
        self.cafe.request_table(self)
        self.event.wait()  # Ждем, пока не получим стол, перенес в метод run
        if self.table:
            print(f'Посетитель номер {self.number} кушает за столом {self.table.number}.')
            time.sleep(4)  # Имитация времени приема пищи,чиобы проверить корректность кода
            print(f'Посетитель номер {self.number} покушал и ушёл.')
            self.cafe.release_table(self.table)

class Cafe:
    def __init__(self, tables_count):
        self.queue = queue.Queue()
        self.tables = tables_count
        self.customer_count = 0
        self.lock = threading.Lock()

    def customer_arrival(self):
        for i in range(1, 21):
            self.customer_count += 1
            customer = Customer(self.customer_count, self)
            customer.start()
            time.sleep(1)

    def request_table(self, customer):
        with self.lock:
            for table in self.tables:
                if not table.is_busy:
                    table.is_busy = True
                    customer.table = table
                    print(f'Посетитель номер {customer.number} сел за стол {table.number}.')
                    customer.event.set()
                    return
            print(f'Посетитель номер {customer.number} ожидает свободный стол.')
            self.queue.put(customer)

    def release_table(self, table):
        with self.lock:
            table.is_busy = False
            print(f'Стол {table.number} освободился.')
            if not self.queue.empty():
                waiting_customer = self.queue.get()
                table.is_busy = True
                waiting_customer.table = table
                print(f'Посетитель номер {waiting_customer.number} сел за стол {table.number}.')
                waiting_customer.event.set()


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)

customer_arrival_thread.start()
customer_arrival_thread.join()

for thread in threading.enumerate():
    if thread != threading.current_thread():
        thread.join()