# функция добавления в множество нажатых с кнопок значений
def add_item_in_aim_set(aim_list: set, item: int | str) -> set:
    # если
    if isinstance(item, int):
        aim_list.add(item)
    if isinstance(item, str):
        number_list = item.split(',')
        number_set = {int(num.strip()) for num in number_list if num.isdigit()}
        aim_list = aim_list | number_set
    return aim_list


def set_check_in_group_list(group_list: list, aim_list: set, check: str = '🟣') -> list:
    new_group_list = group_list.copy()
    for i in range(len(group_list)):
        number_list = group_list[i].split(',')
        number_set = {int(num.strip()) for num in number_list if num.isdigit()}
        if number_set.issubset(aim_list):
            new_group_list[i] = check + new_group_list[i] + check
            # if item == int(button_list[i].split('-', 1)[0]):
    return new_group_list



def set_check_in_button_list(button_list: list, aim_list: set, check: str = '🟣') -> list:
    button_list_clear = [int(x.split('-', 1)[0]) for x in button_list]
    new_button_list = button_list.copy()
    for i in range(len(button_list)):
        if button_list_clear[i] in aim_list:
            new_button_list[i] = check + new_button_list[i] + check
            # if item == int(button_list[i].split('-', 1)[0]):
    return new_button_list

aim_set = set()
button_list = ['1-a', '2-b', '3-c', '4-d', '5-e', '6-f', '7-g', '8-h', '9-i', '10-j', '11-k', '12-l']
group1 = "1,2,3,4,5"
group2 = "3,4,5,6,7"
group3 = "1,5,11"
group_list = [group1, group2, group3]

added_item1 = 1
added_item2 = 5
added_item3 = 11
print(f'начальный - {aim_set}')

aim_set = add_item_in_aim_set(aim_set, added_item1)
button_list1 = set_check_in_button_list(button_list, aim_set)
group_list1 = set_check_in_group_list(group_list, aim_set)
group_list1 =group_list
print('-----------------')
print(f'после добавления {added_item1} - {aim_set}')
print(button_list1)
print(group_list1)

aim_set = add_item_in_aim_set(aim_set, group1)
button_list2 = set_check_in_button_list(button_list, aim_set)
group_list2 = set_check_in_group_list(group_list, aim_set)
print('-----------------')
print(f'после добавления {group1} - {aim_set}')
print(button_list2)
print(group_list2)

aim_set = add_item_in_aim_set(aim_set, group3)
button_list3 = set_check_in_button_list(button_list, aim_set)
group_list3 = set_check_in_group_list(group_list, aim_set)
print('-----------------')
print(f'после добавления {group3} - {aim_set}')
print(button_list3)
print(group_list3)

# s = set()
s = {}
if s:
    print("2222")
    print(s)
else:
    print("1111")









