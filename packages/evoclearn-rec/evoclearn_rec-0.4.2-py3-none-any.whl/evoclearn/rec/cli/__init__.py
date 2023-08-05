# -*- coding: utf-8 -*-

import click

from .. import collect
from .. import train
from .. import compile_model
from .. import ac2vec


@click.group()
def main():
    pass


main.add_command(collect.main, name="collect")
main.add_command(train.main, name="train")
main.add_command(compile_model.main, name="compile")
main.add_command(ac2vec.main, name="ac2vec")
