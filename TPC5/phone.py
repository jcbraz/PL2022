import re

class State:
    def __init__(self, isActive=True, balance=0.0):
        self.isActive = isActive
        self.balance = balance

    def get_isActive(self):
        return self.isActive

    def get_balance(self):
        return self.balance


class Ativo(State):
    def __init__(self):
        super().__init__(True, 0.0)

    def add_balance(self, balance: float):
        self.balance += balance

    def hangup(self):
        self.isActive = False


class EmChamada(State):
    def __init__(self, balance: float):
        super().__init__(True, balance)

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

def coin_handling(coin_sequence: str, balance: float):

    coin_value_pattern = re.compile(r'(\d+(?:c|e))')
    coins = re.findall(coin_value_pattern, coin_sequence)
    

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
    while active_command.lower() != 'levantar':
        if active_command.lower() == 'abortar':
            print('maq: Operação abortada. Volte sempre!')
            flag = True
            break
        print(
            'maq: O telefone está inactivo. Levante o telefone antes de executar qualquer comando')
        active_command = input()

    phone = Ativo()
    active_command = input('maq: Introduza moedas\n')

    while True:

        if active_command.lower() == 'pousar' or active_command.lower() == 'abortar':
            break
            
        coin_matching = re.match(coin_pattern, active_command)
        if coin_matching:
            try:
                balance, formatted_balance = coin_handling(
                    active_command, phone.get_balance())
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

    print(f"troco={format_balance(phone.get_balance())}; Volte sempre!")


main()

# extra
# def structure_exchange(formatted_balance: str) -> str:

#     exchange = []
#     coin_num = 0
#     euros = int(format_balance[0])
#     cent_index = formatted_balance.find('c')
#     if formatted_balance[cent_index - 2] == 'e':
#         cents = int(formatted_balance[cent_index - 1])
#     else:
#         first_cents_num = formatted_balance[cent_index - 2]
#         second_cents_num = formatted_balance[cent_index - 1]
#         cents = int(first_cents_num.join(second_cents_num))

#     if euros % 2 == 0:
#         coin_num = euros/2
#         exchange.append(f'{coin_num}x2e')
#     else:
#         if euros != 1:
#             coin_num = euros-1/2
#             exchange.append(f'{coin_num}x2')
#             exchange.append('1x1e')
#         else:
#             exchange.append('1x1e')

#     if cents % 2 == 0:
#         if cents < 20:
#             exchange.append('1x10c')
#         else:
#             rest_cents = cents/20
#             coin_num = cents // 20
#             if not rest_cents.is_integer():
#                 exchange.append(f'{coin_num}x20c')
#                 exchange.append('1x10c')
#             else:
#                 exchange.append(f'{rest_cents}x20c')
#     else:
#         if cents % 5 == 0:
#             if cents < 20:
#                 exchange.append('1x10c')
#             else:
#                 rest_cents = cents/20
#                 coin_num = cents // 20
#                 if not rest_cents.is_integer():
#                     exchange.append(f'{coin_num}x20c')
#                     exchange.append('1x10c')
#                     exchange.append('1x5c')
#                 else:
#                     exchange.append(f'{rest_cents}x20c')
#                     exchange.append('1x5c')
            

#     return exchange


# def handle_cents(cents: float, num_to_verify: int) -> list:

#     exchange = []

#     if cents % num == 0:
#         if cents < 20:
#             exchange.append('1x10c')
#         else:
#             rest_cents = cents/20
#             coin_num = cents // 20
#             if not rest_cents.is_integer():
#                 exchange.append(f'{coin_num}x20c')
#                 exchange.append('1x10c')
#             else:
#                 exchange.append(f'{rest_cents}x20c')