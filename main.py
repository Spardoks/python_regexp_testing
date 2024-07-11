import csv
import re


# Каждая запись в адресной книге имеет вид
# lastname,firstname,surname,organization,position,phone,email
# телефон и e-mail у одного человека может быть только один
# если совпали одновременно Фамилия и Имя, это точно один и тот же человек (даже если не указано его отчество)


# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# Заготовка для упрощения работы при дальнейшем написании кода и группировке
header_pos = 0
data_pos = 1
data_len = len(contacts_list)
lastname_pos = contacts_list[header_pos].index("lastname")
firstname_pos = contacts_list[header_pos].index("firstname")
surname_pos = contacts_list[header_pos].index("surname")
organization_pos = contacts_list[header_pos].index("organization")
position_pos = contacts_list[header_pos].index("position")
phone_pos = contacts_list[header_pos].index("phone")
email_pos = contacts_list[header_pos].index("email")


# Задача 1
# Пройти по списку контактов, каждый элемент которого является списком информации о контакте и
# поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
# В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.
# Подсказка: работайте со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" "), регулярки здесь НЕ НУЖНЫ.
for i in range(data_pos, data_len):
    contact = contacts_list[i]
    lastname, firstname, surname = (" ".join([contact[lastname_pos], contact[firstname_pos], contact[surname_pos]])).split(" ")[:3]
    contact[lastname_pos], contact[firstname_pos], contact[surname_pos] = lastname, firstname, surname


# Задача 2
# Пройти по списку контактов, каждый элемент которого является списком информации о контакте и
# привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
# Подсказка: используйте регулярки для обработки телефонов.
for i in range(data_pos, data_len):
    contact = contacts_list[i]
    phone = contact[phone_pos]
    # удалить специальные символы для поиска телефонов более удобно
    phone = re.sub(r"[\(\)\-]", r"", phone)
    # удалить лишние пробелы
    phone = re.sub(r" +", r" ", phone)
    # удалить пробелы в начале
    phone = re.sub(r"^ ",  r"", phone)
    # удалить пробелы между цифрами
    phone = re.sub(r"(\d) ", r"\1", phone)
    # удалить пробел между точкой и чем-нибудь
    phone = re.sub(r"(\.) ", r"\1", phone)
    # привести к нужному формату телефон
    phone = re.sub(r"(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})(доб\.\d{4})?",
                   r"+7(\2)\3-\4-\5 \6", phone)
    # удалить последние пробелы, может появится, если доб. номер не указан
    phone = re.sub(r" +$", r"", phone)
    contact[phone_pos] = phone


# Задача 3
# Объединить все дублирующиеся записи о человеке в одну.
# Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).
# Хреновая подсказка, так как изначально сказано, что человек ожнозначно определяется по ФИ
# Будем группировать по ФИ
contacts_list_formatted = []
contacts_list_formatted.append(contacts_list[header_pos])
group_cache = {}
for i in range(data_pos, data_len):
    contact = contacts_list[i]
    lastname, firstname = contact[lastname_pos], contact[firstname_pos]
    if lastname not in group_cache:
        group_cache[lastname] = {}
    if firstname not in group_cache[lastname]:
        # Такие ФИ первый раз встретили
        # Запомним  порядковый номер контакта в сгруппированном списке
        contacts_list_formatted.append(contact)
        group_cache[lastname][firstname] = len(contacts_list_formatted) - 1
    else:
        # Такие ФИ уже были
        # Заполним только непустые поля
        contact_formatted_pos = group_cache[lastname][firstname]
        contact_formatted = contacts_list_formatted[contact_formatted_pos]
        if contact_formatted[surname_pos] == "":
            contact_formatted[surname_pos] = contact[surname_pos]
        if contact_formatted[organization_pos] == "":
            contact_formatted[organization_pos] = contact[organization_pos]
        if contact_formatted[position_pos] == "":
            contact_formatted[position_pos] = contact[position_pos]
        if contact_formatted[phone_pos] == "":
            contact_formatted[phone_pos] = contact[phone_pos]
        if contact_formatted[email_pos] == "":
            contact_formatted[email_pos] = contact[email_pos]


# Записываем отредактированную адресную книгу в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_formatted)
