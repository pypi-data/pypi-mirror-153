#!/usr/bin/env python

from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(name='openai-summarizer',
      version='0.1.5',
      description='Summarize text using OpenAI.',
      long_description=readme(),
      license='MIT',
      author='Aalekh Patel',
      author_email='hi@aalekhpatel.com',
      keywords='openai summarizer email text',
      url='https://www.github.com/aalekhpatel07/openai-summarizer',
      packages=['openai_summarizer'],
      install_requires=['openai'],
      entry_points = {
          'console_scripts': ['email-summarizer=openai_summarizer.email_summarizer.py:main']
      },
      include_package_data=True,
      zip_safe=True
     )
