import setuptools

setuptools.setup(
    name="text-highlighter",
    version="0.0.3",
    author="K.M.J. Jacobs",
    author_email="mail@kevinjacobs.nl",
    description="Streamlit component for text highlighting",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
