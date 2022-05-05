VALUE_VALIDATION_PASSWORD_MIN_LENGTH=8
VALUE_VALIDATION_PASSWORD_MAX_LENGTH=20
VALUE_DEFAULT_AVATAR='avartar/default.png'
KEY_IS_VERIFIED='is_verified'
MESSAGE_USER_NOT_FOUND='User not found'
VALUE_AUTH_USER='auth_user'
KEY_DETAIL='detail'
KEY_STATUS_CODE='status_code'
KEY_RESULTS='results'
VALUE_SUCCESS='Success'
MESSAGE_VALIDATION_PASSWORD_LEAST_CHARACTER='Password must be at least {} characters'\
	.format(VALUE_VALIDATION_PASSWORD_MIN_LENGTH)
MESSAGE_VALIDATION_PASSWORD_MOST_CHARACTER='Password must be at most {} characters'\
	.format(VALUE_VALIDATION_PASSWORD_MAX_LENGTH)
MESSAGE_VALIDATION_PASSWORD_CONTAIN_DIGIT='Password must contain at least one digit'
MESSAGE_VALIDATION_PASSWORD_CONTAIN_UPPERCASE='Password must contain at least one uppercase letter'
VALUE_SUBJECT_VERIFICATION_EMAIL='Verify your email address to complete registration'
MESSAGE_VALIDATION_PASSWORD_CONTAIN_LOWERCASE='Password must contain at least one lowercase letter'
MESSAGE_VALIDATION_PASSWORD_NOT_CONTAIN_SPECIAL_CHARACTER='Password must not contain special characters'
KEY_USERNAME='username'
KEY_EMAIL='email'
KEY_AVARTAR='avartar'
KEY_MOBILE_NUMBER='mobile_number'
KEY_FIRST_NAME='first_name'
KEY_LAST_NAME='last_name'
KEY_ADDRESS='address'
KEY_CITY='city'
KEY_COUNTRY='country'
KEY_POSTAL_CODE='postal_code'
KEY_BIRTHDAY='birthday'
KEY_FORMAT='format'
VALUE_STRING_FORMAT_DATE='%Y-%m-%d'
MESSAGE_GET_PROFILE_SUCCESS='Get profile success'
KEY_INPUT_TYPE='input_type'
VALUE_PASSWORD='password'
KEY_TOKEN='token'
KEY_PASSWORD='password'
KEY_PASSWORD2='password2'
KEY_READ_ONLY='read_only'
VALUE_VALIDATION_USERNAME_MIN_LENGTH=5
VALUE_VALIDATION_USERNAME_MAX_LENGTH=20
MESSAGE_VALIDATION_USERNAME_LEAST_CHARACTER='Username must be at least {} characters'\
	.format(VALUE_VALIDATION_USERNAME_MIN_LENGTH)
MESSAGE_VALIDATION_USERNAME_MOST_CHARACTER='Username must be at most {} characters'\
	.format(VALUE_VALIDATION_USERNAME_MAX_LENGTH)
MESSAGE_VALIDATION_USERNAME_CONTAIN_LETTER_AND_DIGIT='Username must contain at least one letter and one digit'
MESSAGE_VALIDATION_USERNAME_NOT_CONTAIN_SPECIAL_CHARACTER='Username must not contain special characters'
MESSAGE_USERNAME_EXIST='Username already exist'
VALUE_VALIDATION_REGEX_EMAIL=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
VALUE_VALIDATION_EMAIL_MIN_LENGTH=5
VALUE_VALIDATION_EMAIL_MAX_LENGTH=50
MESSAGE_VALIDATION_EMAIL_LEAST_CHARACTER='Email must be at least {} characters'\
	.format(VALUE_VALIDATION_EMAIL_MIN_LENGTH)
MESSAGE_VALIDATION_EMAIL_MOST_CHARACTER='Email must be at most {} characters'\
	.format(VALUE_VALIDATION_EMAIL_MAX_LENGTH)
MESSAGE_EMAIL_EXIST='Email already exist'
MESSAGE_EMAIL_INVALID='Email is invalid'
VALUE_VALIDATION_MOBILENUMBER_MIN_LENGTH=10
VALUE_VALIDATION_MOBILENUMBER_MAX_LENGTH=10
VALUE_VALIDATION_MOBILENUMBER_REGEX=r'^[0-9]{10}$'
MESSAGE_MOBILENUMBER_INVALID='Mobile number is invalid'
MESSAGE_MOBILE_NUMBER_EXIST='Mobile number already exist'
MESSAGE_VALIDATION_PASSWORD_NOT_MATCH='Password not match'
KEY_ACCESS='access'
MESSAGE_REGISTER_SUCCESS='Register success. Please verify your email address'
MESSAGE_INVALID_KEY='Invalid key'
KEY_KEY='key'
KEY_USER_ID='user_id'
KEY_VERIFICATION_KEY='verification_key'
KEY_TYPE='type'
KEY_DETAIL='detail'
VALUE_VERIFY_EMAIL='verify_email'
MESSAGE_TOKEN_TYPE_INVALID='Token type is invalid'
MESSAGE_EMAIL_ALREADY_VERIFIED='Email already verified'
MESSAGE_ACCESS_DENIED='Access denied'
KEY_VERIFICATION_EXPIRY='verification_expiry'
MESSAGE_LINK_EXPIRED='Link expired'
MESSAGE_VERIFIED_SUCCESS='Verified success'
MESSAGE_USERNAME_NOT_EXISTS='Username not exists'
MESSAGE_EMAIL_RESENT_SUCCESS='Email resent success'
MESSAGE_USER_NOT_ACTIVE='User not active'
MESSAGE_UNABLE_TO_LOGIN_WITH_PROVIDER='Unable to login with provider'
MESSAGE_MUST_INCLUDE_USERNAME='Must include username'
MESSAGE_LOGIN_SUCCESS='Login success'
MESSAGE_MOBILE_NUMBER_EXIST='Mobile number already exist'
VALUE_IMAGE_MAX_SIZE=5
MESSAGE_VALIDATION_IMAGE_SIZE='Image size must be less than {}MB'\
	.format(VALUE_IMAGE_MAX_SIZE)
VALUE_IMAGE_EXTENSION_ALLOWED=['jpg', 'jpeg', 'png']
MESSAGE_VALIDATION_IMAGE_EXTENSION='Image extension must be {}'\
	.format(', '.join(VALUE_IMAGE_EXTENSION_ALLOWED))
VALUE_EMAIL_CONTENT_TYPES=['text/html']
VALUE_IMAGE_CONTENT_TYPES=['image/jpeg', 'image/png']
MESSAGE_IMAGE_TYPE_INVALID='Image type is invalid'
MESSAGE_IMAGE_SIZE_TOO_LARGE='Image size too large'
MEASSAGE_PROFILE_UPDATE_SUCCESS='Profile update success'
KEY_OLD_PASSWORD='old_password'
KEY_NEW_PASSWORD='new_password'
KEY_NEW_PASSWORD2='new_password2'
KEY_WRITE_ONLY='write_only'
MESSAGE_PASSWORD_INCORRECT='Password incorrect'
MESSAGE_PASSWORD_UPDATE_SUCCESS='Password update success'
VALUE_RESET_PASSWORD='reset_password'
MESSAGE_EMAIL_NOT_EXIST='Email not exist'
MESSAGE_RESET_PASSWORD_SUCCESS='Reset password success. Please check your email'
MESSAGE_VERIFY_EMAIL_FIRST='Please verify your email first'
MESSAGE_KEY_HAS_EXPIRED='Key has expired'
MESSAGE_SEND_RESET_PASSWORD_SUCCESS='Send reset password success. Please check your email'
VALUE_ACCESS_TOKEN='access_token'
MESSAGE_RESET_PASSWORD_SUCCESS='Reset password success. Please check your email'
KEY_REFRESH_TOKEN='refresh_token'
MESSAGE_LOGOUT_SUCCESS='Logout success'
MESSAGE_LOGOUT_EVERYWHERE_SUCCESS='Logout everywhere success'
KEY_ROTATE_REFRESH_TOKENS='ROTATE_REFRESH_TOKENS'
KEY_BLACKLIST_AFTER_ROTATION='BLACKLIST_AFTER_ROTATION'
MESSAGE_REFRESH_TOKEN_SUCCESS='Refresh token success'
KEY_REFRESH='refresh'
VALUE_INVALID_KEY='Invalid key'
MESSAGE_INVALID_TOKEN='Invalid token'
VALUE_PROFILE = 'profile'
VALUE_REGISTRATION = 'registration'
VALUE_LOGIN = 'login'
VALUE_REFRESH = 'refresh'
VALUE_LOGOUT = 'logout'
VALUE_LOGOUT_EVERYWHERE = 'logout_everywhere'
VALUE_UPDATE_PROFILE = 'update_profile'
VALUE_CHANGE_PASSWORD = 'change_password'
VALUE_VERIFY_EMAIL = 'verify_email'
VALUE_REVERIFY_EMAIL = 'reverify_email'
PROFILE_URL=VALUE_PROFILE + '/'
REGISTRATION_URL=VALUE_REGISTRATION + '/'
LOGIN_URL=VALUE_LOGIN + '/'
REFRESH_URL=VALUE_REFRESH + '/'
LOGOUT_URL=VALUE_LOGOUT + '/'
LOGOUT_EVERYWHERE_URL=VALUE_LOGOUT_EVERYWHERE + '/'
UPDATE_PROFILE_URL=VALUE_UPDATE_PROFILE + '/'
CHANGE_PASSWORD_URL=VALUE_CHANGE_PASSWORD + '/'
VERIFY_EMAIL_URL=VALUE_VERIFY_EMAIL + '/'
REVERIFY_EMAIL_URL=VALUE_REVERIFY_EMAIL + '/'
VALUE_ALLOWED_NUMBER_CHAR='0123456789'
VALUE_POST_METHOD='POST'
VALUE_GET_METHOD='GET'
VALUE_PUT_METHOD='PUT'
VALUE_DELETE_METHOD='DELETE'
KEY_REQUEST='request'
VALUE_LESSON_CONTENT='lesson_content'
VALUE_ITEM_CONTENT='item_content'
VALUE_TEST_CONTENT='test_content'
VALUE_QUIZ_CONTENT='quiz_content'
KEY_ID='id'
KEY_NAME='name'
KEY_DESCRIPTION='description'
VALUE_NAME_MIN_LENGTH=3
VALUE_NAME_MAX_LENGTH=50
MESSAGE_VALIDATION_NAME_LEAST_CHAR='Name must be least {} characters'\
	.format(VALUE_NAME_MIN_LENGTH)
MESSAGE_VALIDATION_NAME_MOST_CHAR='Name must be most {} characters'\
	.format(VALUE_NAME_MAX_LENGTH)
MESSAGE_LESSON_EXIST='Lesson already exist'
KEY_VOCABULARY='vocabulary'
KEY_TYPING_COUNT='typing_count'
KEY_RIGHT_COUNT='right_count'
KEY_WRONG_LIST='wrong_list'
MESSAGE_VOCABULARY_NOT_EXIST='Vocabulary not exist'
MESSSAGE_VOCABULARY_EXIST='Vocabulary already exist'
KEY_LESSON='lesson'
KEY_ITEM='item'
MESSAGE_LESSON_NOT_EXIST='Lesson not exist'
MESSAGE_LESSON_ITEM_NOT_EXIST='Lesson item not exist'
MESSAGE_LESSON_CONTENT_NOT_EXIST='Lesson content not exist'
MESSAGE_LESSON_CONTENT_EXIST='Lesson content already exist'
MESSAGE_TEST_EXIST='Test already exist'
KEY_QUESTION='question'
KEY_ANSWER='answer'
KEY_ANSWER1='answer1'
KEY_ANSWER2='answer2'
KEY_ANSWER3='answer3'
KEY_CORRECT_ANSWER='correct_answer'
KEY_QUESTION_TYPE='question_type'
KEY_REQUIRED='required'
MESSAGE_FIND_WORD_HAS_MEANING='Find word has meaning of \'{}\' in dictionary?'
MESSAGE_FIND_MEANING_OF='Find meaning of \'{}\' in dictionary?'
MESSAGE_QUIZ_NOT_EXIST='Quiz not exist'
MESSAGE_QUIZ_EXIST='Quiz already exist'
KEY_QUIZ='quiz'
KEY_TEST='test'
MESSAGE_TEST_NOT_EXIST='Test not exist'
MESSAGE_TEST_CONTENT_NOT_EXIST='Test content not exist'
MESSAGE_TEST_CONTENT_EXIST='Test content already exist'
VALUE_LESSONS=r'lessons'
VALUE_LESSON_ITEMS=r'lesson_items'
VALUE_LESSON_CONTENTS=r'lesson_contents'
VALUE_TESTS=r'tests'
VALUE_QUIZZES=r'quizzes'
VALUE_QUIZ_CONTENTS=r'quiz_contents'
MESSAGE_SUCCESS='Success'
KEY_STATUS_CODE='status_code'
KEY_RESULTS='results'
SEARCH_WORD='^word'
SEARCH_MEANING='meaning'
SEARCH_EXAMPLE='example'
SEARCH_PHONETIC='phonetic'
SEARCH_POS='=pos'
SEARCH_LANGUAGE='=language'
SEARCH_COLLECTION_NAME='^collection_name'
KEY_WORD='word'
KEY_POS='pos'
KEY_LANGUAGE='language'
KEY_COLLECTION_NAME='collection_name'
KEY_COLLECTION='collection'
VALUE_COLLECTIONS=r'collections'
VALUE_VOCABULARIES=r'vocabularies'
KEY_IMAGE='image'
MESSAGE_COLLECTION_EXIST='Collection already exist'
KEY_MEANING='meaning'
KEY_EXAMPLE='example'
KEY_PHONETIC='phonetic'
KEY_AUDIO='audio'
KEY_POS='pos'
KEY_LANGUAGE='language'
KEY_POS_EXTEND='pos_extend'
VALUE_MP3_EXTEND='.mp3'
VALUE_WAV_EXTEND='.wav'
MESSAGE_VALIDATION_AUDIO_EXTEND='Audio must be .mp3 or .wav'
VALUE_VALIDATION_WORD_MIN_LENGTH=3
VALUE_VALIDATION_WORD_MAX_LENGTH=50
MESSAGE_VALIDATION_WORD_MOST_CHAR='Word must be most {} characters'\
	.format(VALUE_VALIDATION_WORD_MAX_LENGTH)
MESSAGE_VALIDATION_WORD_LEAST_CHAR='Word must be least {} characters'\
	.format(VALUE_VALIDATION_WORD_MIN_LENGTH)
VALUE_DESCRIPTION_DEFAULT='No description'
VALUE_DESCRIPTION_AUTOMATIC='Created automatically'
MESSAGE_COLLECTION_NOT_EXIST='Collection not exist'
KEY_MEANINGS='meanings'
KEY_DEFINITION='definition'
KEY_DEFINITIONS='definitions'
VALUE_EMPTY_STRING=''
KEY_PART_OF_SPEECH='partOfSpeech'
VALUE_COMMA=','
VALUE_SPACE=' '
VALUE_NEW_LINE='\n'
KEY_PHONETICS='phonetics'
DICTIONARY_API_URL='https://api.dictionaryapi.dev/api/v2/entries/en/{}'
IMAGE_DEFAULT_FOLDER='images/'
VALUE_ANSWER_DEFAULT='No answer'
MESSAGE_VALIDATION_VOCABULARIES_IS_EMPTY='Vocabularies is empty'
KEY_ALLOW_NULL='allow_null'
KEY_MESSAGE='message'
