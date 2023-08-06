import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvadmin-celery",
    version="1.0.2",
    author="DVAdmin",
    author_email="liqiang@django-vue-admin.com",
    description="适用用 django-vue-admin 的celery异步插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/huge-dream/dvadmin-celery",
    packages=setuptools.find_packages(),
    python_requires='>=3.7, <4',
    install_requires=["django-celery-beat>=2.2.1",
                      "tenant-schemas-celery>=1.0.1",
                      "django-redis>=5.0.0",
                      "django-celery-results>=2.2.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
