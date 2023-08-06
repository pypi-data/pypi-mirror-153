# dvadmin_celery_backend

#### 介绍
dvadmin-celery是集成django-celery-beat、tenant-schemas-celery、django-redis、django-celery-results 的一个前后端插件，
安装可快速使用异步任务，包含在线添加任务、任务记录等

## 安装包

使用pip安装软件包：

~~~python
pip install dvadmin-celery
~~~
### 方式一: 一键导入注册配置
在 application / settings.py 插件配置中下导入默认配置
```python
...
from dvadmin_celery.settings import *
```
### 方式二: 手动配置
在INSTALLED_APPS 中注册app

~~~python
INSTALLED_APPS = [
    ...
    'django_celery_beat',
    'django_celery_results',
    'dvadmin_celery',
]
~~~

在 application / urls.py 中注册url地址

~~~python
urlpatterns = [
    ...
    re_path(r'api/dvadmin_celery/', include('dvadmin_celery.urls')),
]
~~~

如果没有系统redis，请启动redis并添加配置 (conf / env.example.py 及 conf / env.py中添加如下配置)

~~~python
# redis 配置
REDIS_PASSWORD = ''
REDIS_HOST = '127.0.0.1'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6379'

~~~

在 application / settings.py 下添加配置

~~~python
...
CACHES = { # 配置缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{REDIS_URL}/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
BROKER_URL = f'{REDIS_URL}/2'  
CELERY_RESULT_BACKEND = 'django-db' # celery结果存储到数据库中
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'  # Backend数据库
~~~

进行迁移及初始化
```python
python3 manage.py makemigrations 
python3 manage.py migrate 
# 注意备份初始化信息
python3 manage.py init -y 
```

其他配置请参考 django_celery_beat 文档及celery 文档

#### 使用说明

~~~ python
mac/linux:
celery -A application.celery worker -B --loglevel=info
win:
需要安装: pip install eventlet
celery -A application.celery worker -P eventlet --loglevel=info
~~~
