
CALL_SET_SCHEME= 'c_set_scheme_'



CALL_CAPTURE_WORD = "capture_word_"
CALL_CHANGE_WORD = "change_word_"
MESS_CAPTURE_WORD = 'Выберите слово или введите с клавиатуры и отправьте боту часть слова'
TEXT_CHANGE_WORD = "Изменить слово"
MESS_CAPT_WORD_CONFIRM= "✅CONFIRM1✅"
NUM_CAPTURE_WORD_COLS = 2
NUM_CAPTURE_WORD_ROWS = 10
CHECK_CAPTURE_WORD= '🟣'

CALL_CAPTURE_GROUP = "add_group_"
CALL_CHANGE_GROUP = "change_group_"
MESS_CAPTURE_GROUP = 'Выберите слово или введите с клавиатуры и отправьте боту часть слова'
TEXT_CHANGE_GROUP = "Изменить группу"
MESS_CAPT_GROUP_CONFIRM= "✅CONFIRM2✅"
NUM_CAPTURE_GROUP_COLS = 1
NUM_CAPTURE_GROUP_ROWS = 10
CHECK_CAPTURE_GROUP= '🟣'


CALL_CAPTURE_USER = "add_user_"
CALL_CHANGE_USER = "change_user_"
MESS_CAPTURE_USER = 'Выберите слово или введите с клавиатуры и отправьте боту часть слова'
TEXT_CHANGE_USER = "Изменить юзеров"
MESS_CAPT_USER_CONFIRM= "✅CONFIRM3✅"
NUM_CAPTURE_USER_COLS = 2
NUM_CAPTURE_USER_ROWS = 10
CHECK_CAPTURE_USER= '🟣'


CALL_CAPTURE_DATE = "add_date_"
CALL_CHANGE_DATE = "change_date_"
MESS_CAPTURE_DATE = 'Выберите слово или введите с клавиатуры и отправьте боту часть слова'
TEXT_CHANGE_DATE = "Изменить слово"
MESS_CAPT_DATE_CONFIRM= "✅CONFIRM4✅"
NUM_CAPTURE_DATE_COLS = 4
NUM_CAPTURE_DATE_ROWS = 5
CHECK_CAPTURE_DATE= '🟣'


CALL_ADD_ENDING = "add_ending_"
MESS_ADD_ENDING = 'Поверьте все и подтвердите'
TEXT_ADD_ENDING_CONFIRM= "✅CONFIRM4✅"
CALL_CHANGING_WORD = "changing_word_"
CALL_CHANGING_USER = "changing_user_"
CALL_CHANGING_DATE = "changing_date_"







M_ADM_MENU = "Welcome to main admin menu"

T_ADM_MENU_ADDING = "📌📌Add word, media etc📌📌"
T_ADM_MENU_ADDING_BACK = "-Add menu-"
C_ADM_MENU_ADDING = "c_adm_menu_add"

T_ADM_MENU_SETTING = "📌Set task to user📌"
T_ADM_MENU_SETTING_BACK = "-Set task menu-"
C_ADM_MENU_SETTING = "c_adm_menu_set"

T_ADM_MENU_EDITING = "Editing"
T_ADM_MENU_EDITING_BACK = "-Edit menu-"
C_ADM_MENU_EDITING = "c_adm_menu_edit"

CALL_CONFIRM= "@confirm_"

MESS_MORE_CHOOSING = 'Можете выбрать еще или нажмите подтверждение'
MESS_NULL_CHOOSING = 'Нельзя продолжить пока ничего не выбрано'
MESS_NULL_CHOOSING2 = 'Ну вообще никак нельзя продолжить пока ничего не выбрано'



M_ADM_SETTING = "Choose what do you want to set or assign"

M_ADM_ADDING = "Choose what do you want to add"


T_ADM_ADD_WORD = "📌Add word📌"
C_ADM_ADD_WORD = "c_adm_add_word"


T_ADM_SET_SCHEME = "📌Set task by scheme📌"
C_ADM_SET_SCHEME = "c_adm_set_scheme"

T_ADM_SET_COLL = "Set task with some media or collocation"
C_ADM_SET_COLL = "c_adm_set_coll"



CALL_INPUT_WORD = "input_word_"






MESS_INPUT_WORD = "Vvedite slovo"





CALL_CAPTURE_LEVEL = "capture_level_"
LEVEL_LIST = ['A1','A2','B1','B2','C1','C2']
CALL_CHANGE_LEVEL = "change_level_"
NUM_CAPTURE_LEVEL_COLS = 3
NUM_CAPTURE_LEVEL_ROWS = 10
CHECK_CAPTURE_LEVEL= '🟣'
TEXT_CHANGE_LEVEL = "Изменить уровень"
MESS_CAPTURE_LEVEL = 'Выберите уровень или введите с клавиатуры и отправьте боту часть названия'
MESS_CAPT_LEVEL_CONFIRM= "✅LCONFIRM✅"

levels_state_dict = {
    'state_name': 'capture_level_state',
    'state_kb_check': CHECK_CAPTURE_LEVEL,
    'state_kb_cols': NUM_CAPTURE_LEVEL_COLS,
    'state_kb_rows': NUM_CAPTURE_LEVEL_ROWS,
    'state_main_message': MESS_CAPTURE_LEVEL,
    'state_change_but_text': TEXT_CHANGE_LEVEL,
    'state_confirm_but_text': MESS_CAPT_LEVEL_CONFIRM,
}






MESS_SET_SCHEME = "Choose word or write letters"




CALL_ADD_WORD= 'c_add_word_'
CALL_ADD_GROUP = "add_group_"
CALL_ADD_USER = "add_user_"
CALL_ADD_DATE = "add_date_"


MESS_CONFIRM= "✅CONFIRM✅"



NUM_SET_SCHEME_GROUP_COLS = 1
NUM_SET_SCHEME_GROUP_ROWS = 10
CHECK_SET_SCHEME_GROUP= '🟣'

NUM_SET_SCHEME_USER_COLS = 2
NUM_SET_SCHEME_USER_ROWS = 10
CHECK_SET_SCHEME_USER= '🟣'

NUM_SET_SCHEME_DATE_COLS = 4
NUM_SET_SCHEME_DATE_ROWS = 5
CHECK_SET_SCHEME_DATE= '🟣'




word_state_dict = {
    'state_name': 'input_word_state',
    'state_kb_check': None,
    'state_kb_cols': None,
    'state_kb_rows': None,
    'state_main_message': MESS_CAPTURE_WORD,
    'state_change_but_text': TEXT_CHANGE_WORD,
    'state_confirm_but_text': MESS_CAPT_WORD_CONFIRM
}




ADM_ADD_ADDING_BY_SCHEMA_NOTHING = 'Вы ничего не выбрали, выбирайте еще и подтвердите выбор'
ADM_ADD_TASK_BY_SCHEMA_DAY = 'А теперь выберите дату начала схемы изучения или введите в формате ДД.ММ.ГГГГ'
ADM_ADD_TASK_BY_SCHEMA_DAY_REP = 'Выберите дату или проверьте формат: ДД.ММ.ГГГГ'
ADM_ADD_TASK_BY_SCHEMA_CONFIRMATION = 'Проверьте и подтвердите запись в базу данных:'
ADM_ADD_TASK_BY_SCHEMA_CONFIRMATION_REP = 'Печатать не нужно. Пожалуйста, подтвердите или отмените:'
ADM_ADD_TASK_BY_SCHEMA_ERROR = 'Ошибка при записи в базу данных, обратитесь к администратору'
ADM_ADD_TASK_BY_SCHEMA_ADDED_WORD = 'Задание по схемам по словам\n{}\nдля\n{}\nдобавлено в базу данных!'
ADM_ADD_TASK_BY_SCHEMA_ADDED_MEDIA = 'Задание по изучению коллокации \n{}\nдля\n{}\nдобавлено в базу данных!'
ADM_ADD_TASK_BY_SCHEMA_AGAIN = 'Создаем тест заново, выбирайте слово или напечатайте его или его часть:'



# из конфиг
REMINDER_INTERVAL='09:00 - 22:00' # время работы напоминатора
REMINDER_SLEEP_INTERVAL=60*60 # промежутки между запусками функции напоминатора
SENDING_SLEEP_INTERVAL=1 #интервалы между отправкой сообщений пользователям

COUNT_OF_DELETED_MESSAGES = 15
COUNT_OF_LAST_WORDS_ADDING_MEDIA=10

STUDYING_DAY_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 21, 28, 35]
TEST_TYPES = ['test4','test7']