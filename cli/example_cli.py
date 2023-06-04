# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/7/10 9:39 pm
# @File    : example_cli.py
# @Software: PyCharm
# description:
ref: https://click.palletsprojects.com/en/8.0.x/
"""
import click


@click.command(context_settings=dict(ignore_unknown_options=True,
                                     allow_extra_args=True
                                     ))
@click.option("--count", default=1)
@click.option('--name', default="hello world",
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


if __name__ == '__main__':
    hello()
