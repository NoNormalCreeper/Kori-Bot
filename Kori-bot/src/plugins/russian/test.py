# units = ['', 'K', 'M', 'B', 'T', 'P']
# def resolve_formated_number(num) -> int:
#     num = str(num)
#     num = num.replace(' ', '')
#     try:
#         return int(num)
#     except ValueError:
#         if ',' in num:
#             num = num.replace(',', '')
#         else:
#             num = num.upper()
#             for unit in units[1:]:
#                 if unit in num:
#                     num = num.replace(unit, '')
#                     num = float(num) * (1000**units.index(unit))
#                     return int(num)
#             # not found
#             return 0
#         return int(num)

# print(resolve_formated_number('12.33222222324234b'))

def number_format(num) -> str:
    # auto add thousand delimiter
    num = str(num)
    digit = ''
    if '.' in num:
        digit = num.split('.')[1]
        num = num.split('.')[0]
    def add_delimiter(num):
        if len(num) > 3:
            return add_delimiter(num[:-3]) + ',' + num[-3:]
            # add_delimiter(num)
        else:
            return num
    num = add_delimiter(num)
    if digit:
        num = num + '.' + digit
    return num

print(number_format('21912312123123238403.1221321323132'))