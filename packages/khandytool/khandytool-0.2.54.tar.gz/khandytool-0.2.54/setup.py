import setuptools
import platform



with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="khandytool",
    version="0.2.54",
    author="Ou Peng",
    author_email="kevin72500@qq.com",
    description="khandytool, handy core in testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevin72500/khandytool",
    packages=setuptools.find_packages(),
    package_data={'core.bladeTest': ['xmindStructure.jpg']},
    include_package_data=True,
    install_requires=['jsonpath==0.82','xmltodict==0.13.0','flashtext','fabric==2.6.0','pytest==6.2.5','pywebio==1.4.0','requests==2.26.0','loguru==0.5.3','jinja2==3.0.2','openpyxl==3.0.9','xmindparser==1.0.9','jmespath==0.10.0','pymysql==1.0.2','swaggerjmx==1.0.9','faker==8.12.1','websockets==10.1','pywebio==1.4.0','kafka-python==2.0.2','flask==2.0.2','Werkzeug==2.0.2','paho-mqtt==1.5.1','msgpack==1.0.3','redis==4.1.3','python-dotenv==0.19.2','jsonschema',"pycryptodome==3.12.0; platform_system=='Windows'","pycrypto==2.6.1; platform_system=='Linux'","pycrypto==2.6.1; platform_system=='Darwin'","tenacity","wget"],
    # data_files=[
    #     ('jmx',["apache-jmeter-5.4.1.zip"]),
    # ],
    # extras_requires={
    #     "pycryptodome==3.12.0; sys_platform=='Windows'",
    #     "pycrypto==2.6; sys_platform=='Linux'",
    #     "pycrypto==2.6; sys_platform=='Darwin'"
    # },
    entry_points={
        'console_scripts': [
            'khandytool=khandytool:core'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

