from faker import Faker, Factory
from random import randint, choices
import string
import datetime
import snowflake.connector


def create_accounts():
    accounts = []
    fake = Faker()
    acc_type = ['savings', 'current', 'salary']
    linked = [True, False]

    for i in range(1, 10):
        account = {
            'acc_num': ''.join(["{}".format(randint(0, 9)) for num in range(0, 20)]),
            'customer_name': fake.name(),
            'unique_identity': ''.join(choices(string.ascii_uppercase, k=3)) + ''.join(choices(string.digits, k=4)),
            'phone_number': fake.phone_number(),
            'balance': randint(10000, 10000000),
            'acc_type': acc_type[randint(0, 2)],
            'upper_limit': randint(10000000, 20000000),
            'credit_cards_linked': linked[randint(0, 1)],
            'loan_amount': randint(100000, 1000000),
            'email': fake.email(),
            'last_login_at': datetime.datetime(2021, 5, 1) + datetime.timedelta(days=randint(25, 29)),
            'created_at': datetime.datetime(2021, 5, 1) + datetime.timedelta(days=randint(1, 24))
        }
        accounts.append(account)
    return accounts


def create_branches():
    branches = []
    fake = Faker()
    bank_type = ['PRIVATE', 'CENTRAL']

    for i in range(1, 10):
        branch = {
            'id': ''.join(choices(string.ascii_uppercase, k=2)) + ''.join(choices(string.digits, k=4)),
            'address': fake.address(),
            'ifsc_code': ''.join(choices(string.ascii_uppercase, k=2)) + ''.join(choices(string.digits, k=4)),
            'employees_count': randint(25, 100),
            'micr_code': ''.join(choices(string.ascii_uppercase, k=2)) + ''.join(choices(string.digits, k=4)),
            'established_on': datetime.datetime(randint(1995, 2021), randint(1, 11), randint(1, 30)),
            'type': bank_type[randint(0, 1)]
        }
        branches.append(branch)
    return branches


def create_credit_cards(account_numbers):
    cards = []
    card_type = ['VISA', 'MASTER', 'EXPRESS', 'RUPAY']

    if len(account_numbers) <= 0:
        return

    for acc_num in account_numbers:
        num = randint(1, 10)
        if num >= 3:
            card = {
                'card_number': str(randint(1000, 9999)) + '-' + str(randint(1000, 9999)) + '-' + str(
                    randint(1000, 9999)) + '-' + str(randint(1000, 9999)),
                'cvv': randint(100, 999),
                'valid_upto': str(randint(1, 12)) + '/' + str(randint(2020, 2028)),
                'acc_id': acc_num,
                'limit': randint(10000, 500000),
                'type': card_type[randint(0, 3)]
            }
            cards.append(card)

    return cards


def create_transactions(account_numbers):
    transactions = []
    debit = [True, False]
    fake = Faker()

    if len(account_numbers) <= 0:
        return

    for acc_num in account_numbers:
        num = randint(1, 10)
        if num >= 3:
            transaction = {
                'id': ''.join(choices(string.ascii_uppercase, k=3)) + ''.join(choices(string.digits, k=5)),
                'from_acc_id': acc_num,
                'to_acc_id': account_numbers[randint(0, len(account_numbers) - 1)],
                'amount': randint(100, 100000),
                'debit': debit[randint(0, 1)],
                'started_at': datetime.datetime(2021, 6, 1) + datetime.timedelta(days=randint(1, 20)),
                'merchant_name': fake.company(),
                'end_balance': randint(10000, 1000000)
            }
            transactions.append(transaction)
    return transactions


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


def generate_account_data():
    insert_acc_sql = """
    INSERT INTO FINANCE.FINANCE."ACCOUNTS" (ACC_NUM, CUSTOMER_NAME, UNIQUE_IDENTITY, PHONE_NUMBER, BALANCE, ACC_TYPE, UPPER_LIMIT, CREDIT_CARDS_LINKED, LOAN_AMOUNT, EMAIL, CREATED_AT, LAST_LOGIN_AT) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    account_numbers = []
    accounts = create_accounts()
    conn = create_conn()
    cur = conn.cursor()

    for acc in accounts:
        cur.execute(insert_acc_sql, (
        acc['acc_num'], acc['customer_name'], acc['unique_identity'], acc['phone_number'], acc['balance'],
        acc['acc_type'], acc['upper_limit'], acc['credit_cards_linked'], acc['loan_amount'], acc['email'],
        acc['created_at'], acc['last_login_at'],))
        acc_num = acc['acc_num']
        account_numbers.append(acc_num)

    conn.commit()
    return account_numbers


def generate_branch_data():
    insert_branch_sql = """
    INSERT INTO FINANCE.FINANCE.BRANCHES (ID, ADDRESS, IFSC_CODE, EMPLOYEE_COUNT, MICR_CODE, ESTABLISHED_ON, "TYPE") VALUES(%s, %s, %s, %s, %s, %s, %s);
    """

    branches = create_branches()
    conn = create_conn()
    cur = conn.cursor()

    for branch in branches:
        cur.execute(insert_branch_sql, (
        branch['id'], branch['address'], branch['ifsc_code'], branch['employees_count'], branch['micr_code'],
        branch['established_on'], branch['type'],))

    conn.commit()


def generate_credit_card_data(account_numbers):
    insert_cc_sql = """
    INSERT INTO FINANCE.FINANCE.CREDIT_CARDS (CARD_NUMBER, CVV, VALID_UPTO, ACC_ID, "LIMIT", "TYPE") VALUES(%s, %s, %s, %s, %s, %s);
    """

    cards = create_credit_cards(account_numbers)
    conn = create_conn()
    cur = conn.cursor()

    for cc in cards:
        cur.execute(insert_cc_sql,
                    (cc['card_number'], cc['cvv'], cc['valid_upto'], cc['acc_id'], cc['limit'], cc['type'],))

    conn.commit()


def generate_transactions(account_numbers):
    insert_trans_sql = """
    INSERT INTO FINANCE.FINANCE.TRANSACTIONS_LOGS (ID, FROM_ACC_ID, TO_ACC_ID, AMOUNT, DEBIT, STARTED_AT, MERCHANT_NAME, END_BALANCE) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
    """

    trans = create_transactions(account_numbers)
    conn = create_conn()
    cur = conn.cursor()

    for tran in trans:
        cur.execute(insert_trans_sql, (
        tran['id'], tran['from_acc_id'], tran['to_acc_id'], tran['amount'], tran['debit'], tran['started_at'],
        tran['merchant_name'], tran['end_balance'],))

    conn.commit()


def generate_finance_data():
    print('Generating data')
    print('Accounts......')
    account_numbers = generate_account_data()
    print('Branches......')
    generate_branch_data()
    print('Credit cards......')
    generate_credit_card_data(account_numbers)
    print('transactions......')
    generate_transactions(account_numbers)


generate_finance_data()
