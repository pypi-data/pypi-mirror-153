# -*- coding: utf-8 -*-

import sys
import itertools

import click

from .. import Sequences, io, DEFAULT_VARIABLE_PARAMS
from .. import samplers
from .. import log


@click.group()
def main():
    pass


@main.command()
@click.option("--params",
              type=str,
              default=",".join(DEFAULT_VARIABLE_PARAMS),
              help="Comma-separated list of params to include")
@click.option("--labels",
              type=str,
              help="Comma-separated labels (also determines sequence length)")
@click.option("--seed",
              type=int)
@click.option("--maxsamples",
              type=int,
              default=None,
              help="Maximum number of samples to draw")
@click.option("--outputpath",
              type=click.Path(),
              help="Output to NetCDF format")
@click.option("--slurp",
              is_flag=True,
              help="Do in-memory (faster if possible)")
@click.argument("boundsfile",
                type=click.File("r"))
def uniform(boundsfile,
            params,
            labels,
            seed,
            maxsamples,
            outputpath,
            slurp):
    logger = log.getLogger("evl.cli.sample.uniform")
    params = [param.strip() for param in params.split(",")]
    bounds = io.load_bounds(boundsfile, params)
    labs = labels.split(",") if labels else None
    sampler = samplers.Uniform(bounds, labs, seed)
    # Generate all sequences in-memory or one-by-one:
    if slurp:
        if maxsamples is None:
            raise click.UsageError("Cannot --slurp without --maxsamples")
        seqs = sampler.sequences(maxsamples)
    else:
        if maxsamples is not None:
            sampler = itertools.islice(sampler, maxsamples)
        seqs = Sequences.from_iter(sampler)
    # Output to NetCDF file/dir or stdout JSON lines:
    message_maxsamples = "unlimited" if maxsamples is None else maxsamples
    if outputpath is not None:
        message_files = "single file" if slurp else "multiple files"
        logger.info("Writing %s sequences to NetCDF (%s)"
                    % (message_maxsamples, message_files))
        seqs.to_netcdf(outputpath)
    else:
        logger.info("Writing %s JSON lines" % message_maxsamples)
        for i, line in enumerate(seqs.to_jsonlines()):
            if (i + 1) % 100 == 0:
                logger.info("Written %s lines to stdout..." % (i + 1))
            sys.stdout.write(line)


@main.command()
@click.option("--consonants",
              type=str,
              help="Comma-separated consonant symbols "
              "(determines C control params)")
@click.option("--seed",
              type=int)
@click.option("--maxsamples",
              type=int,
              default=None,
              help="Maximum number of samples to draw")
@click.option("--outputpath",
              type=click.Path(),
              help="Output to NetCDF format")
@click.option("--slurp",
              is_flag=True,
              help="Do in-memory (dump to file is faster)")
@click.argument("boundsfile",
                type=click.File("r"))
def uniform_problink(boundsfile,
                     consonants,
                     seed,
                     maxsamples,
                     outputpath,
                     slurp):
    logger = log.getLogger("evl.cli.sample.uniform_problink")
    bounds = io.load_bounds(boundsfile)
    consnts = consonants.split(",") if consonants else None
    sampler = samplers.UniformProbLink(bounds, consnts, seed)
    # Generate all sequences to memory or one-by-one:
    if slurp:
        if maxsamples is None:
            raise click.UsageError("Cowardly refusing to --slurp "
                                   "without --maxsamples")
        seqs = sampler.sequences(maxsamples)
    else:
        if maxsamples is not None:
            sampler = itertools.islice(sampler, maxsamples)
        seqs = Sequences.from_iter(sampler)
    # Output to NetCDF file/dir or stdout JSON lines:
    message_maxsamples = "unlimited" if maxsamples is None else maxsamples
    if outputpath is not None:
        message_files = "single file" if slurp else "multiple files"
        logger.info("Writing %s sequences to NetCDF (%s)"
                    % (message_maxsamples, message_files))
        seqs.to_netcdf(outputpath)
    else:
        logger.info("Writing %s JSON lines" % message_maxsamples)
        for i, line in enumerate(seqs.to_jsonlines()):
            if (i + 1) % 100 == 0:
                logger.info("Written %s lines to stdout..." % (i + 1))
            sys.stdout.write(line)
