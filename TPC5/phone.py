import re


class State:
    def __init__(self):
        self.isActive = False
        self.balance = 0

    def __init__(self, isActive: bool):
        self.isActive = isActive
        self.balance = 0

    def __init__(self, balance: float):
        self.isActive = True
        self.balance = balance

    def __init__(self, isActive: bool, balance: float):
        self.isActive = isActive
        self.balance = balance

    def get_isActive(self):
        return self.isActive

    def get_balance(self):
        return self.balance


class Ativo(State):

    def __init__(self):
        super().__init__(True, 0)

    def add_balance(self, balance: float):
        self.balance = balance

    def hangup(self):
        self.isActive = False


class EmChamada(State):

    def __init__(self, balance: float):
        super().__init__(self, balance)

    def __init__(self, ativo: Ativo):
        super().__init__(ativo.get_isActive(), ativo.get_balance())

    def update_balance(self, fee: float):
        self.balance -= fee

    def hangup(self):
        self.isActive = False


def format_balance(balance: float):

    balance = round(balance, 2)
    balance_str = str(balance)
    
    first_digit = balance_str[0]
    decimal_pos = balance_str.find('.')
    decimals = balance_str[decimal_pos + 1:]

    formatted_balance = f'{first_digit}e{decimals}c'
    return formatted_balance


def coin_handling(regular_expression, balance: float):

    coin_section = regular_expression.group(1)
    coin_value_pattern = re.compile(r'(\d+(?:c|e))')
    coins = coin_value_pattern.findall(coin_section)

    if not coins:
        raise Exception("maq: Sequência de moedas inválida!\n")

    coin_values = {
        "1c": 0.01,
        "2c": 0.02,
        "5c": 0.05,
        "10c": 0.1,
        "20c": 0.2,
        "50c": 0.5,
        "1e": 1,
        "2e": 2
    }

    final_balance = balance
    invalid_coin = None
    for coin in coins:
        print(coin)
        if coin not in coin_values:
            invalid_coin = coin
        else:
            final_balance += coin_values[coin]

    formatted_balance = format_balance(final_balance)

    if invalid_coin:
        print(f"maq:{coin} - moeda inválida; saldo \n= {formatted_balance}")

    return final_balance, formatted_balance


def number_handling(regular_expression, balance: float):

    blocked_numbers = {"601", "641"}
    call_prices = {
        "00": 1.50,
        "2": 0.25,
        "800": 0,
        "808": 0.10
    }

    number_section = regular_expression.group(1)
    phone_pattern = re.compile(r'^(00|2|800|808|641|601)\d+$')
    number = phone_pattern.match(number_section)

    if not number:
        raise Exception("maq: Número inserido inválido!\n")

    prefix = number.group(1)
    if prefix in blocked_numbers:
        raise Exception(
            "maq: Esse número não é permitido neste telefone. Queira discar novo número!\n")

    resulting_call_price = call_prices[prefix]
    if balance < resulting_call_price:
        raise Exception('Saldo Insuficiente! Introduza mais moedas\n')

    return resulting_call_price


def main():

    coin_pattern = re.compile(r"MOEDA\s+((\d+(?:c|e)(?:,\s*)?)*)")
    phone_pattern = re.compile(r"T=(\d{9}|00\d+)")

    active_command = input()
    flag = False
    while active_command.lower() != 'levantar':
        if active_command.lower() == 'abortar':
            print('maq: Operação abortada. Volte sempre!')
            flag = True
            break
        print(
            'maq: O telefone está inactivo. Levante o telefone antes de executar qualquer comando')
        active_command = input()

    if not flag:

        if active_command.lower() == 'pousar' or active_command.lower() == 'abortar':
            phone.hangup()
            flag = True

        phone = Ativo()
        active_command = input('maq: Introduza moedas\n')

        while phone.get_isActive() is True:

            coin_matching = re.match(coin_pattern, active_command)
            if coin_matching:
                try:
                    balance, formatted_balance = coin_handling(
                        coin_matching, phone.get_balance())
                    phone.add_balance(balance)
                    print(f'maq: saldo = {formatted_balance}\n')
                except Exception as e:
                    print("maq:", e)

            active_command = input('maq: Introduza o número de telefone\n')

            number_matching = re.match(phone_pattern, active_command)
            if number_matching:
                call_fee = 0
                try:
                    call_fee = number_handling(
                        number_matching, phone.get_balance())
                    phone = EmChamada(phone)
                    phone.update_balance(call_fee)
                    print(
                        f'maq: Chamada em curso...\n saldo disponível = {format_balance(phone.get_balance())}')
                except Exception as e:
                    print("maq:", e)

            active_command = input()

        print(f"troco={phone.get_balance()}; Volte sempre!")


main()
