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

# из конфиг
REMINDER_INTERVAL='09:00 - 22:00' # время работы напоминатора
REMINDER_SLEEP_INTERVAL=60*60 # промежутки между запусками функции напоминатора
SENDING_SLEEP_INTERVAL=1 #интервалы между отправкой сообщений пользователям

COUNT_OF_DELETED_MESSAGES = 15
COUNT_OF_LAST_WORDS_ADDING_MEDIA=10

STUDYING_DAY_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 21, 28, 35]
TEST_TYPES = ['test4','test7']



CALL_MAIN_MENU= '@m_main_menu️'
BTEXT_MAIN_MENU= '-Main menu-️'
MESS_MAIN_MENU = "Im Alexis English Bot! Welcome to main menu"
BTEXT_MAIN_MENU_BACK = "Exit to main menu"

CALL_STUDY_MENU= '@m_study_menu️'
BTEXT_STUDY_MENU= '---Study menu NEW---'
MESS_STUDY_MENU = "Welcome to study menu!"
BTEXT_STUDY_MENU_BACK = "Exit to study menu"

CALL_REVISION_MENU= '@m_revision_menu️'
BTEXT_REVISION_MENU= '---Revision menu NEW---'
MESS_REVISION_MENU = "Welcome to revision menu!"
BTEXT_REVISION_MENU_BACK = "Exit to revision menu"

CALL_CONFIG_MENU= '@m_config_menu️'
BTEXT_CONFIG_MENU= '---Config menu NEW---'
MESS_CONFIG_MENU = "Welcome to config menu!"
BTEXT_CONFIG_MENU_BACK = "Exit to config menu"

CALL_ADMIN_MENU= '@m_admin_menu️'
BTEXT_ADMIN_MENU= '🛠️---Admin menu NEW---🛠️'
MESS_ADMIN_MENU = "!Welcome to main admin menu"
BTEXT_ADMIN_MENU_BACK = "Exit to main admin menu"


CALL_ADDING_MENU = "@c_adm_menu_add"
MESS_ADDING_MENU = "Choose what do you want to add"
BTEXT_ADDING_MENU = "📌Add words, collocation and other📌"
BTEXT_ADDING_MENU_BACK = "-Exit to ADDING menu-"

CALL_ADD_WORD= 'c_add_word_'
BTEXT_ADD_WORD = "📌Add word📌"

CALL_ADD_COLL= 'c_add_coll_'
BTEXT_ADD_COLL = "📌Add collocation📌"

CALL_ADD_GROUP = "c_add_group_"
BTEXT_ADD_GROUP = "📌Add group📌"

CALL_ADD_HOMEWORK = "c_add_homework_"
BTEXT_ADD_HOMEWORK = "📌Add homework📌"


CALL_SETTING_MENU = "@c_adm_menu_set"
MESS_SETTING_MENU = "Choose what do you want to set or assign"
BTEXT_SETTING_MENU = "📌Set task to user📌"
BTEXT_SETTING_MENU_BACK = "-Set task menu-"

CALL_SET_SCHEME= 'c_set_scheme_'
BTEXT_SET_SCHEME = "📌Set task by scheme📌"

CALL_SET_COLL = "c_set_coll"
BTEXT_SET_COLL = "Set task with some collocation"


CALL_EDITING_MENU = "c_adm_menu_edit"
MESS_EDITING_MENU = "Choose what do you want to set or assign"
BTEXT_EDITING_MENU = "Editing"
BTEXT_EDITING_MENU_BACK = "-Edit menu-"




# common
MESS_MORE_CHOOSING = 'Можете выбрать еще или нажмите подтверждение'
MESS_NULL_CHOOSING = 'Нельзя продолжить пока ничего не выбрано'
MESS_ADDED_TO_DB = 'Информация добавлена в базу данных!'
MESS_ERROR_ADDED_TO_DB = 'Ошибка при записи в базу данных, обратитесь к администратору'
CALL_CONFIRM= "@confirm_"
TEXT_BUTTON_CONFIRM= "✅CONFIRM✅"

MESS_ADD_ENDING = 'Поверьте все и подтвердите'
CALL_ADD_ENDING = "add_ending_"


# capturing word
CALL_CAPTURE_WORDS = "capture_words_"
CALL_CHANGING_WORDS = "changing_words_"
MESS_CAPTURE_WORDS = 'Выберите слово или введите с клавиатуры и отправьте боту часть этого слова (его номер)'
BTEXT_CHANGE_WORDS = "Изменить слова"
NUM_CAPTURE_WORDS_COLS = 2
NUM_CAPTURE_WORDS_ROWS = 10
CHECK_CAPTURE_WORDS= '🟣'

# capturing collocations
CALL_CAPTURE_COLLS = "capture_colls_"
CALL_CHANGING_COLLS = "changing_colls_"
MESS_CAPTURE_COLLS = 'Выберите коллокацию или введите с клавиатуры и отправьте боту ее часть'
BTEXT_CHANGE_COLLS = "Изменить коллокации"
NUM_CAPTURE_COLLS_COLS = 1
NUM_CAPTURE_COLLS_ROWS = 10
CHECK_CAPTURE_COLLS= '🟣'

# capturing part
CALL_CAPTURE_PARTS = "capture_parts_"
CALL_CHANGING_PARTS = "changing_parts_"
MESS_CAPTURE_PARTS = 'Выберите часть речи или введите с клавиатуры и отправьте боту часть названия'
BTEXT_CHANGE_PARTS = "Изменить часть речи"
NUM_CAPTURE_PARTS_COLS = 3
NUM_CAPTURE_PARTS_ROWS = 10
CHECK_CAPTURE_PARTS= '🟣'
PARTS_LIST = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'numerals', 'idiom', 'phrasal verb', 'new2']

# capturing level
CALL_CAPTURE_LEVELS = "capture_levels_"
CALL_CHANGING_LEVELS = "changing_levels_"
MESS_CAPTURE_LEVELS = 'Выберите уровень или введите с клавиатуры и отправьте боту часть названия'
BTEXT_CHANGE_LEVELS = "Изменить уровень"
NUM_CAPTURE_LEVELS_COLS = 3
NUM_CAPTURE_LEVELS_ROWS = 10
CHECK_CAPTURE_LEVELS= '🟣'
LEVELS_LIST = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

# capturing group
CALL_CAPTURE_GROUPS = "capture_groups_"
CALL_CHANGING_GROUPS = "changing_groups_"
MESS_CAPTURE_GROUPS = 'Выберите группу или введите с клавиатуры и отправьте боту часть названия группы (ее номер)'
BTEXT_CHANGE_GROUPS = "Изменить группу"
NUM_CAPTURE_GROUPS_COLS = 1
NUM_CAPTURE_GROUPS_ROWS = 10
CHECK_CAPTURE_GROUPS= '🟣'

# capturing user
CALL_CAPTURE_USERS = "capture_users_"
CALL_CHANGING_USERS = "changing_users_"
MESS_CAPTURE_USERS = 'Выберите пользователя или введите с клавиатуры и отправьте боту часть его имени (или номер)'
BTEXT_CHANGE_USERS = "Изменить юзеров"
NUM_CAPTURE_USERS_COLS = 2
NUM_CAPTURE_USERS_ROWS = 10
CHECK_CAPTURE_USERS= '🟣'

# capturing date
CALL_CAPTURE_DATES = "capture_dates_"
CALL_CHANGING_DATES = "changing_dates_"
MESS_CAPTURE_DATES = 'Выберите дату'
BTEXT_CHANGE_DATES = "Изменить дату"
NUM_CAPTURE_DATES_COLS = 4
NUM_CAPTURE_DATES_ROWS = 5
CHECK_CAPTURE_DATES= '🟣'

# capturing day
CALL_CAPTURE_DAYS = "capture_daуs_"
CALL_CHANGING_DAYS = "changing_days_"
MESS_CAPTURE_DAYS = 'Выберите день изучения или введите с клавиатуры и отправьте боту часть слова'
BTEXT_CHANGE_DAYS = "Изменить дeнь"
NUM_CAPTURE_DAYS_COLS = 4
NUM_CAPTURE_DAYS_ROWS = 8
CHECK_CAPTURE_DAYS= '🟣'

# input word
CALL_INPUT_WORD = "input_word_"
CALL_CHANGING_WORD = "changing_word_"
MESS_INPUT_WORD = "Введите слово для словаря"
BTEXT_CHANGE_WORD = "Изменить слово"
# input group
CALL_INPUT_GROUP = "input_group_"
CALL_CHANGING_GROUP = "changing_group_"
MESS_INPUT_GROUP = "Введите название группы"
BTEXT_CHANGE_GROUP = "Изменить название группы"
# input homework
CALL_INPUT_HOMEWORK = "input_homework_"
CALL_CHANGING_HOMEWORK = "changing_homework_"
MESS_INPUT_HOMEWORK = "Введите домашнее задание"
BTEXT_CHANGE_HOMEWORK = "Изменить домашнее задание"
# input collocation
CALL_INPUT_COLL = "input_coll_"
CALL_CHANGING_COLL = "changing_coll_"
MESS_INPUT_COLL = "Введите коллокацию для изучаемого слова"
BTEXT_CHANGE_COLL = "Изменить коллокацию"
# input media
CALL_INPUT_MEDIA = "input_media_"
CALL_CHANGING_MEDIA = "changing_media_"
MESS_INPUT_MEDIA = "Добавьте медиа: введите текст, отправьте картинку или видео"
BTEXT_CHANGE_MEDIA = "Изменить медиа"
# input caption
CALL_INPUT_CAPTION = "input_caption_"
CALL_CHANGING_CAPTION = "changing_caption_"
MESS_INPUT_CAPTION = "Введите caption"
BTEXT_CHANGE_CAPTION = "Изменить caption"
# input definition
CALL_INPUT_DEFINITION = "input_definition_"
CALL_CHANGING_DEFINITION = "changing_definition_"
MESS_INPUT_DEFINITION = "Введите определение на английском языке"
BTEXT_CHANGE_DEFINITION = "Изменить определение"
# input translation
CALL_INPUT_TRANSLATION = "input_translation_"
CALL_CHANGING_TRANSLATION = "changing_translation_"
MESS_INPUT_TRANSLATION = "Введите русский перевод"
BTEXT_CHANGE_TRANSLATION = "Изменить определение"