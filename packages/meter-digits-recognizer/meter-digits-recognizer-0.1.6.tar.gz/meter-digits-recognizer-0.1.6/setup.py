from setuptools import setup

setup(name="meter-digits-recognizer", 
    version="0.1.6",
    url="https://github.com/ardiloot/meter-digits-recognizer",
    author="Ardi Loot",
    author_email="ardi.loot@outlook.com",
    packages=["meter_digits_recognizer"],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Pillow",
        "opencv-python",
    ]
)