from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 

setup(
    name="WebhookSender_py",

    version="1.0.0",

    description=""" Discord Webhhook Sender   """,

    long_description_content_type="text/markdown",

    long_description=open('README.txt').read(),

    url="",

    author="0xjohn",

    classifiers=["License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.9"],

    packages = find_packages(),
    
    install_requires=['discord_webhook'],
    
    include_package_data=True
)
