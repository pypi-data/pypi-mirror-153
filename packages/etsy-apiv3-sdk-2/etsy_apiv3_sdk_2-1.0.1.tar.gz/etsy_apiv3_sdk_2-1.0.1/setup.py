import setuptools
 
 
setuptools.setup(
    name="etsy_apiv3_sdk_2",  
    version="1.0.1",
    author="Esat Yılmaz",
    author_email="esatyilmaz3500@gmail.com",
    description="Etsy APIV3 SDK",
    packages=["models", "resources", "utils"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.5',
    install_requires=[
        "pydantic", "requests", "requests_oauthlib"
    ]
)