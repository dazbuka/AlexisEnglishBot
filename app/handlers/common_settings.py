from enum import Enum

class MediaType(Enum):
    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    LOCATION = "location"
    CONTACT = "contact"
    STICKER = "sticker"
    ANIMATION = "animation"



CALL_MAIN_MENU= '@m_main_menu️'
BTEXT_MAIN_MENU= '-Main menu-️'
MESS_MAIN_MENU = "Im Alexis English Bot! Welcome to main menu"
TEXT_MAIN_MENU_BACK = "Exit to main menu"


CALL_ADMIN_MENU= '@m_admin_menu️'
BTEXT_ADMIN_MENU= '🛠️---Admin menu NEW---🛠️'
MESS_ADMIN_MENU = "!Welcome to main admin menu"
TEXT_ADMIN_MENU_BACK = "Exit to main admin menu"


TEXT_MENU_ADDING = "-Add word, media etc-"
TEXT_MENU_ADDING_BACK = "-Exit to ADDING menu-"
CALL_ADDING_MENU = "c_adm_menu_add"


MESS_SETTING_MENU = "Choose what do you want to set or assign"
T_ADM_MENU_SETTING = "📌Set task to user📌"
T_ADM_MENU_SETTING_BACK = "-Set task menu-"
CALL_SETTING_MENU = "c_adm_menu_set"


T_ADM_MENU_EDITING = "Editing"
T_ADM_MENU_EDITING_BACK = "-Edit menu-"
C_ADM_MENU_EDITING = "c_adm_menu_edit"



CALL_SET_SCHEME= 'c_set_scheme_'


MESS_MORE_CHOOSING = 'Можете выбрать еще или нажмите подтверждение'
MESS_NULL_CHOOSING = 'Нельзя продолжить пока ничего не выбрано'
MESS_ADDED_TO_DB = 'Информация добавлена в базу данных!'
MESS_ERROR_ADDED_TO_DB = 'Ошибка при записи в базу данных, обратитесь к администратору'

CALL_CONFIRM= "@confirm_"
TEXT_BUTTON_CONFIRM= "✅CONFIRM✅"


CALL_CAPTURE_WORD = "capture_word_"
CALL_CHANGING_WORD = "changing_word_"
MESS_CAPTURE_WORD = 'Выберите слово или введите с клавиатуры и отправьте боту часть этого слова (его номер)'
TEXT_CHANGE_WORDS = "Изменить слово"
NUM_CAPTURE_WORD_COLS = 2
NUM_CAPTURE_WORD_ROWS = 10
CHECK_CAPTURE_WORD= '🟣'


CALL_CAPTURE_PART = "capture_part_"
CALL_CHANGING_PART = "changing_part_"
MESS_CAPTURE_PART = 'Выберите часть речи или введите с клавиатуры и отправьте боту часть названия'
TEXT_CHANGE_PART = "Изменить часть речи"
NUM_CAPTURE_PART_COLS = 3
NUM_CAPTURE_PART_ROWS = 10
CHECK_CAPTURE_PART= '🟣'
PART_LIST = ['noun','verb','adjective','adverb','pronoun','numerals','idiom','phrasal verb','new2']


CALL_CAPTURE_LEVEL = "capture_level_"
CALL_CHANGING_LEVEL = "changing_level_"
MESS_CAPTURE_LEVEL = 'Выберите уровень или введите с клавиатуры и отправьте боту часть названия'
TEXT_CHANGE_LEVEL = "Изменить уровень"
NUM_CAPTURE_LEVEL_COLS = 3
NUM_CAPTURE_LEVEL_ROWS = 10
CHECK_CAPTURE_LEVEL= '🟣'
LEVEL_LIST = ['A1','A2','B1','B2','C1','C2']


CALL_CAPTURE_GROUP = "capture_group_"
CALL_CHANGING_GROUP = "changing_group_"
MESS_CAPTURE_GROUP = 'Выберите группу или введите с клавиатуры и отправьте боту часть названия группы (ее номер)'
TEXT_CHANGE_GROUP = "Изменить группу"
NUM_CAPTURE_GROUP_COLS = 1
NUM_CAPTURE_GROUP_ROWS = 10
CHECK_CAPTURE_GROUP= '🟣'


CALL_CAPTURE_USER = "capture_user_"
CALL_CHANGING_USER = "changing_user_"
MESS_CAPTURE_USER = 'Выберите пользователя или введите с клавиатуры и отправьте боту часть его имени (или номер)'
TEXT_CHANGE_USER = "Изменить юзеров"
NUM_CAPTURE_USER_COLS = 2
NUM_CAPTURE_USER_ROWS = 10
CHECK_CAPTURE_USER= '🟣'


CALL_CAPTURE_DATE = "capture_date_"
CALL_CHANGING_DATE = "changing_date_"
MESS_CAPTURE_DATE = 'Выберите слово или введите с клавиатуры и отправьте боту часть слова'
TEXT_CHANGE_DATE = "Изменить дату"
NUM_CAPTURE_DATE_COLS = 4
NUM_CAPTURE_DATE_ROWS = 5
CHECK_CAPTURE_DATE= '🟣'

CALL_CAPTURE_DAY = "capture_daу_"
CALL_CHANGING_DAY = "changing_day_"
MESS_CAPTURE_DAY = 'Выберите день изучения или введите с клавиатуры и отправьте боту часть слова'
TEXT_CHANGE_DAY = "Изменить дeнь"
NUM_CAPTURE_DAY_COLS = 4
NUM_CAPTURE_DAY_ROWS = 8
CHECK_CAPTURE_DAY= '🟣'


MESS_ADD_ENDING = 'Поверьте все и подтвердите'
CALL_ADD_ENDING = "add_ending_"


CALL_INPUT_WORD = "input_word_"
MESS_INPUT_WORD = "Введите слово для словаря"
TEXT_CHANGE_WORD = "Изменить слово"

CALL_INPUT_COLL = "input_coll_"
CALL_CHANGING_COLL = "changing_coll_"
MESS_INPUT_COLL = "Введите коллокацию для изучаемого слова"
TEXT_CHANGE_COLL = "Изменить коллокацию"

CALL_INPUT_MEDIA = "input_media_"
CALL_CHANGING_MEDIA = "changing_media_"
MESS_INPUT_MEDIA = "Добавьте медиа: введите текст, отправьте картинку или видео"
TEXT_CHANGE_MEDIA = "Изменить медиа"

CALL_INPUT_CAPTION = "input_caption_"
CALL_CHANGING_CAPTION = "changing_caption_"
MESS_INPUT_CAPTION = "Введите caption"
TEXT_CHANGE_CAPTION = "Изменить caption"

CALL_INPUT_DEFINITION = "input_definition_"
CALL_CHANGING_DEFINITION = "changing_definition_"
MESS_INPUT_DEFINITION = "Введите определение на английском языке"
TEXT_CHANGE_DEFINITION = "Изменить определение"

CALL_INPUT_TRANSLATION = "input_translation_"
CALL_CHANGING_TRANSLATION = "changing_translation_"
MESS_INPUT_TRANSLATION = "Введите русский перевод"
TEXT_CHANGE_TRANSLATION = "Изменить определение"


MESS_SET_SCHEME = "Choose word or write letters"












MESS_ADDING_MENU = "Choose what do you want to add"


T_ADM_ADD_WORD = "📌Add word📌"
C_ADM_ADD_WORD = "c_adm_add_word"

T_ADM_ADD_COLL = "📌Add collocation📌"
C_ADM_ADD_COLL = "c_adm_add_coll"

T_ADM_SET_SCHEME = "📌Set task by scheme📌"
C_ADM_SET_SCHEME = "c_adm_set_scheme"

T_ADM_SET_COLL = "Set task with some media or collocation"
C_ADM_SET_COLL = "c_adm_set_coll"







CALL_ADD_WORD= 'c_add_word_'
CALL_ADD_COLL= 'c_add_coll_'

CALL_ADD_COLL= 'c_add_coll_'

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