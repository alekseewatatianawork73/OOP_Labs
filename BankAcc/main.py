# базовое исключение для банковских операций
class BankError(Exception):
    pass


# ошибка при работе с отрицательными суммами
class NegativeAmountError(BankError):
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"Невозможно выполнить операцию с отрицательной суммой: {amount}")


# ошибка при недостатке средств на счете
class InsufficientFundsError(BankError):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Недостаточно средств. Баланс: {balance}, запрошено: {amount}")


# ошибка при работе с заблокированным счетом
class AccountLockedError(BankError):
    def __init__(self):
        super().__init__("Счет заблокирован. Операция невозможна")


# основной класс банковского счёта
class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self._balance = initial_balance
        self._is_locked = False

    def balance(self):
        return self._balance

    # пополнение счета
    def deposit(self, amount):
        if self._is_locked:
            raise AccountLockedError()

        if amount <= 0:
            raise NegativeAmountError(amount)

        self._balance += amount
        return self._balance

    # снятие средств со счета
    def withdraw(self, amount):
        if self._is_locked:
            raise AccountLockedError()

        if amount <= 0:
            raise NegativeAmountError(amount)

        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        self._balance -= amount
        return self._balance

    # блокировка/разблокировка счёта
    def lock(self):
        self._is_locked = True

    def unlock(self):
        self._is_locked = False

    def __str__(self):
        status = "заблокирован" if self._is_locked else "активен"
        return f"Счет #{self.account_number}, баланс: {self._balance}, статус: {status}"


# класс для реализации безопасных банковских операций
class SafeBankOperation:
    def __init__(self, account, operation_type, amount):
        self.account = account
        self.operation_type = operation_type
        self.amount = amount
        self.result = None
        self.error = None

    # переопределение оператора with
    def __enter__(self):
        try:
            if self.operation_type == "deposit":
                self.result = self.account.deposit(self.amount)
            elif self.operation_type == "withdraw":
                self.result = self.account.withdraw(self.amount)
            else:
                raise ValueError("Неизвестный тип операции")
            return self.result
        except BankError as e:
            self.error = e
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, BankError):
            print(f"Ошибка банковской операции: {exc_val}")
            return True  # Подавляем исключение
        return False


# проверка работы программы
def test_bank_account():
    print("\nТест 1: Создание счета и проверка баланса")
    account = BankAccount("123456789", 1000)
    print(account)

    print("\nТест 2: Корректное пополнение счета")
    try:
        account.deposit(500)
        print(f"Успешное пополнение. Новый баланс: {account.balance()}")
    except BankError as e:
        print(f"Ошибка: {e}")

    print("\nТест 3: Попытка пополнения отрицательной суммой")
    try:
        account.deposit(-100)
    except NegativeAmountError as e:
        print(f"Поймано исключение: {e}")

    print("\nТест 4: Корректное снятие средств")
    try:
        account.withdraw(300)
        print(f"Успешное снятие. Новый баланс: {account.balance()}")
    except BankError as e:
        print(f"Ошибка: {e}")

    print("\nТест 5: Попытка снятия суммы, превышающей баланс")
    try:
        account.withdraw(2000)
    except InsufficientFundsError as e:
        print(f"Поймано исключение: {e}")

    print("\nТест 6: Блокировка счета и попытка операции")
    account.lock()
    print(f"Статус счета: {'заблокирован' if account._is_locked else 'активен'}")
    try:
        account.deposit(100)
    except AccountLockedError as e:
        print(f"Поймано исключение: {e}")

    print("\nТест 7: Использование контекстного менеджера для безопасной операции")
    account.unlock()
    with SafeBankOperation(account, "deposit", 250) as result:
        if result is not None:
            print(f"Операция успешна. Новый баланс: {result}")

    with SafeBankOperation(account, "withdraw", 5000) as result:
        if result is None:
            print("Операция не выполнена из-за ошибки")

    print("\n--- Итоговое состояние счета ---")
    print(account)


test_bank_account()
