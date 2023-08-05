from faker import Faker, Factory
from random import randint, choices
import string
import datetime
import snowflake.connector


def create_conn():
    conn = snowflake.connector.connect(
        user='winash',
        password='myD33ksh@k@n@lu',
        account='kf71436.us-east-1',
        warehouse='COMPUTE_WH',
        database='CUSTOMERS_DATABASE',
        schema='CUSTOMERS'
    )
    return conn


def create_cust_trans():
    trans = []
    fake = Faker()
    product_type = ['Industrial', 'row materials', 'electronics', 'softwares', 'books']
    success = [True, False]

    for i in range(1, 10):
        tr = {
            'customer_name': fake.name(),
            'transaction_id': ''.join(choices(string.ascii_uppercase, k=3)) + ''.join(choices(string.digits, k=5)),
            'merchant_name': fake.company(),
            'product_type': product_type[randint(0, 4)],
            'amount': randint(100, 10000),
            'transaction_at': datetime.datetime.now() + datetime.timedelta(minutes=randint(1, 20)),
            'success': success[randint(0, 1)]
        }
        trans.append(tr)
    return trans


def generate_transactions_data():
    insert_sql = """INSERT INTO CUSTOMERS_DATABASE.CUSTOMERS.CUSTOMERS_TRANSACTIONS (CUSTOMER_NAME, 
    TRANSACTIONS_ID, MERCHANT_NAME, AMOUNT, PRODUCT_TYPE, TRANSACTION_AT, SUCCESS) VALUES(%s, %s, %s, %s, %s, %s, %s); """

    trans = create_cust_trans()
    conn = create_conn()
    cur = conn.cursor()

    for tr in trans:
        cur.execute(insert_sql, (
            tr['customer_name'], tr['transaction_id'], tr['merchant_name'], tr['amount'], tr['product_type'],
            tr['transaction_at'], tr['success'],))

    conn.commit()


def generate_data():
    print('Generating data')
    generate_transactions_data()


# generate_data()
a = datetime.datetime(2021, 6, 22, 14, 10, 0)
b = datetime.datetime.today()

print(a, '  ', b)