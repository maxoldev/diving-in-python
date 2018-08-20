class Value:
    def __init__(self):
        self.__value = 0

    def __set__(self, instance, value):
        self.__value += (1 - instance.commission) * value

    def __get__(self, instance, owner):
        return self.__value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


new_account = Account(0.1)
new_account.amount = 100
print(new_account.amount)
