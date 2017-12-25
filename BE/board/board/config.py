wenzhi_info = {
    'SecretId': 'AKID1CC0byI4nJbfW95jgPvEKAk36sOdjLo0',
    'SecretKey': '6xXrvkNmxvfBTXN0PaXGl25vXv51jDUa',
}
db = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'db_big',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },

    }
}