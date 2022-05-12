from pollux import settings
import os

DATABASES = {
	"default": {
		'ENGINE': 'django.contrib.gis.db.backends.postgis',
		'USER': os.getenv('SQL_USER_NAME'),
		'PASSWORD': os.getenv('SQL_PASSWORD'),
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
}
