from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Vinay Kumar',
    author_email='vinayykumar93@gmail.com',
    install_requirements=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_community"],
    packages=find_packages()
)