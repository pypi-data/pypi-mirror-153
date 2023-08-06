#!/usr/bin/env python

from setuptools import setup

setup(name='openai-summarizer',
      version='0.1.3',
      description='Summarize text using OpenAI.',
      license='MIT',
      author='Aalekh Patel',
      author_email='hi@aalekhpatel.com',
      url='https://www.github.com/aalekhpatel07/openai-summarizer',
      packages=['openai_summarizer'],
      install_requires=['openai'],
      scripts=['bin/email-summarizer']
     )
