# -*- coding: utf-8 -*-

import sys

import click

from .. import Sequences, Sequence
from .. import log
from ..filters import discard_by_constraints

@click.group()
def main():
    pass


@main.command()
def constraints():
    logger = log.getLogger("evl.cli.filter.constraints")
    seqs = map(Sequence.from_json, sys.stdin)
    lines = Sequences.from_iter(discard_by_constraints(seqs)).to_jsonlines()
    for i, line in enumerate(lines):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        sys.stdout.write(line)
