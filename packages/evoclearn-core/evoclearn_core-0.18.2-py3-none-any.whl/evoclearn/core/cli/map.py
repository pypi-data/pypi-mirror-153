# -*- coding: utf-8 -*-

import sys
import functools
import itertools
import json
from os import path
import multiprocessing

import pandas as pd
import librosa
import click

from .. import Sequences, Sequence
from .. import io
from .. import log
from .. import mappings
from .. import vocaltractlab as vtl
from .. import features


@click.group()
def main():
    pass


@main.command()
@click.option("--lower",
              type=float,
              default=-1.0,
              show_default=True,
              help="Lower limit of new range")
@click.option("--upper",
              type=float,
              default=1.0,
              show_default=True,
              help="Upper limit of new range")
@click.argument("boundsfile", type=click.File("r"))
def norm_minmax(boundsfile, upper, lower):
    logger = log.getLogger("evl.cli.map.norm_minmax")
    bounds = io.load_bounds(boundsfile)
    normf = functools.partial(mappings.normalise_minmax,
                              bounds=bounds,
                              lb=lower,
                              ub=upper)
    seqs = map(Sequence.from_json, sys.stdin)
    lines = Sequences.from_iter(map(normf, seqs)).to_jsonlines()
    for i, line in enumerate(lines):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        sys.stdout.write(line)


@main.command()
@click.argument("statsfile", type=click.File("r"))
def norm_std(statsfile):
    logger = log.getLogger("evl.cli.map.norm_std")
    stats = json.load(statsfile)
    normf = functools.partial(mappings.normalise_standard, stats=stats)
    seqs = map(Sequence.from_json, sys.stdin)
    lines = Sequences.from_iter(map(normf, seqs)).to_jsonlines()
    for i, line in enumerate(lines):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        sys.stdout.write(line)


@main.command()
@click.argument("alignfile",
                type=click.Path(exists=True))
@click.option("--index",
              type=int,
              default=0,
              show_default=True,
              help="Starting index from alignment file")
@click.option("--tier",
              type=str,
              default="1",
              show_default=True,
              help="TextGrid tier to read from alignment file")
def qta(alignfile, index, tier):
    logger = log.getLogger("evl.cli.map.qta")
    durations = io.read_durations_from_textgrid(alignfile, tier)
    logger.debug("DURATIONS: %s", durations)
    seqs = map(Sequence.from_json, sys.stdin)
    for i, seq in enumerate(seqs):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        seqdurs = durations[index:index + len(seq)]
        vtl_curves = mappings.vtl_curves_from_targets(seq, seqdurs)
        sys.stdout.write(vtl_curves.to_json() + "\n")


@main.command()
@click.argument("durations",
                nargs=-1,
                type=float)
def qta2(durations):
    logger = log.getLogger("evl.cli.map.qta2")
    logger.debug("DURATIONS: %s", durations)
    seqs = map(Sequence.from_json, sys.stdin)
    for i, seq in enumerate(seqs):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        vtl_curves = mappings.vtl_curves_from_targets(seq, durations)
        sys.stdout.write(vtl_curves.to_json() + "\n")


def synth_save_seq(args):
    seq, idx, wavoutpath = args
    audio = vtl.synthesise(seq)
    if wavoutpath is not None:
        io.wav_write(audio, path.join(wavoutpath, "{}.wav".format(idx)))
    return audio

def audio_to_jsonline(audio):
    return pd.DataFrame(audio)[0].to_json(orient="values") + "\n"


@main.command()
@click.option("--wavoutpath", type=click.Path(exists=True))
@click.option("--skipstdout", is_flag=True)
@click.option("--n_procs", type=int, show_default=True, default=None)
@click.argument("speakerfile", type=click.Path(exists=True))
def synth(speakerfile, wavoutpath, skipstdout, n_procs):
    logger = log.getLogger("evl.cli.map.synth")
    vtl.initialise(speakerfile)
    seqs = map(Sequence.from_json, sys.stdin)
    if n_procs is None:
        for i, seq in enumerate(seqs):
            if (i + 1) % 100 == 0:
                logger.info("Processed %s lines..." % (i + 1))
            audio = synth_save_seq((seq, i, wavoutpath))
            if not skipstdout:
                sys.stdout.write(audio_to_jsonline(audio))
        return
    else:
        with multiprocessing.Pool(n_procs) as procpool:
            batchsize = n_procs
            idx = 0
            while True:
                seqbatch = itertools.islice(seqs, batchsize)
                idxs = range(idx, idx + batchsize)
                argss = ((seq, i, wavoutpath) for i, seq in zip(idxs,
                                                                seqbatch))
                audios = procpool.map(synth_save_seq, argss)
                if len(audios) == 0:
                    break
                idx += len(audios)
                if not skipstdout:
                    for audio in audios:
                        sys.stdout.write(audio_to_jsonline(audio))


@main.command()
@click.option("--feattype",
              type=click.Choice(["ORIGINAL", "ASR", "OPTIMAL"],
                                case_sensitive=False),
              default="ORIGINAL",
              show_default=True)
def feats(feattype):
    logger = log.getLogger("evl.cli.map.feats")
    audios = (df.to_numpy().flatten()
              for df
              in map(pd.DataFrame, map(json.loads, sys.stdin)))
    settings = {"ORIGINAL": features.ORIG_FEATS,
                "ASR": features.ASR_FEATS,
                "OPTIMAL": features.OPTIM_FEATS}[feattype.upper()]
    for i, audio in enumerate(audios):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        feats = mappings.get_features(audio, **settings)
        sys.stdout.write(pd.DataFrame(feats).to_json() + "\n")


@main.command()
@click.option("--feattype",
              type=click.Choice(["ORIGINAL", "ASR", "OPTIMAL"],
                                case_sensitive=False),
              default="ORIGINAL",
              show_default=True)
@click.option("--alignfile",
              type=click.Path(exists=True))
@click.option("--indices",
              type=str,
              help="Comma-separated indices to use from alignfile")
@click.option("--tier",
              type=str,
              default="1",
              show_default=True,
              help="TextGrid tier to read from alignment file")
@click.argument("reffile",
                type=click.Path(exists=True))
def featerr(feattype, alignfile, indices, tier, reffile):
    logger = log.getLogger("evl.cli.map.featerr")
    feats = (df.to_numpy()
             for df
             in map(pd.DataFrame, map(json.loads, sys.stdin)))
    settings = {"ORIGINAL": features.ORIG_FEATS,
                "ASR": features.ASR_FEATS,
                "OPTIMAL": features.OPTIM_FEATS}[feattype.upper()]
    ref_audio, __ = librosa.load(reffile)
    settings["roi"] = None
    if alignfile is not None:
        if indices is None:
            raise click.UsageError("--alignfile must be accompanied"
                                   " by --indices")
        indices = list(map(int, indices.split(",")))
        intervals = io.read_intervals_from_textgrid(alignfile, tier)
        settings["roi"] = [intervals[i] for i in indices]
    ref_feat = mappings.get_features(ref_audio, **settings)
    for i, feat in enumerate(feats):
        if (i + 1) % 100 == 0:
            logger.info("Written %s lines to stdout..." % (i + 1))
        error = mappings.get_error(feat, ref_feat)
        sys.stdout.write(str(error) + "\n")
