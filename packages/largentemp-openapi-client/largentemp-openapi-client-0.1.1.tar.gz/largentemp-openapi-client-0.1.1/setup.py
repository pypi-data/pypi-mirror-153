'''setup.py
Innehåller inställningsfiler till paketet.
'''
import setuptools

VERSION = "0.1.1"
#Ladda lång beskrivning
long_description = open("README.md", "r", encoding="UTF-8").read()

#Ladda moduler som krävs
required_modules = open("requirements.txt", "r", encoding="UTF-8").read()

setuptools.setup(
    name="largentemp-openapi-client",
    version=VERSION,
    author="LargenTemp",
    author_email="largentemp@gmail.com",
    url="https://largentemp.pythonanywhere.com/static/templates/apiinfo.html",
    description="API-klient för LargenTemps öppna API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["src"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    py_modules=["largentemp-openapi-client"],
    install_requires=required_modules
)
