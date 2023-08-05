# -*- coding: utf-8 -*-

import numpy as np
import librosa
try:
    import python_speech_features as psfeat
except ImportError:
    pass

from . import vocaltractlab as vtl
from . import log
from . utils import vtln
from . import distance as dist


LOGGER = log.getLogger("evl.core.features")


ORIG_FEATS = {
    "feature_type": "mfcc",
    "preemphasis": True,  # preem. coefficient is 0.97
    "win_length_s": 0.023,  # for the STFT
    "hop_length_s": 0.005,  # to sync with VTL (5 ms)
    "n_fft": 512,  # for the STFT
    "n_mels": 128,  # for Mel spectrogram
    "mel_fmax": 11025,  # max freq for Mel filter bank
    "n_mfcc": 40,  # for Mel spectrogram
    "lifter": False  # liftering coef is 2*n_mfcc
}


ASR_FEATS = {
    "feature_type": "mfcc",
    "preemphasis": True,  # preem. coefficient is 0.97
    "win_length_s": 0.025,  # for the STFT
    "hop_length_s": 0.005,  # to sync with VTL (5 ms)
    "n_fft": 1024,  # for the STFT
    "n_mels": 26,  # for Mel spectrogram
    "mel_fmax": 10e3,  # max freq for Mel filter bank
    "n_mfcc": 12,  # for Mel spectrogram
    "lifter": True  # liftering coef is 2*n_mfcc
}


OPTIM_FEATS = {
    "feature_type": "mfcc",
    "preemphasis": True,  # preem. coefficient is 0.97
    "win_length_s": 0.025,  # for the STFT
    "hop_length_s": 0.005,  # to sync with VTL (5 ms)
    "n_fft": 1024,  # for the STFT
    "n_mels": 26,  # for Mel spectrogram
    "mel_fmax": 10e3,  # max freq for Mel filter bank
    "n_mfcc": 22,  # for Mel spectrogram
    "lifter": True  # liftering coef is 2*n_mfcc
}


ENERGY_ENV_FEATS = {
    "feature_type": "energy_envelope",
    "win_length_s": None,  # Specified internally
    "hop_length_s": None,  # Specified internally
    "win_func": "boxcar",
    "center_frame": True,
    "pad_mode": "reflect"
}


AMP_ENV_FEATS = {
    "feature_type": "amp_envelope",
    "win_length_s": None,  # Specified internally
    "hop_length_s": None,  # Specified internally
    "win_func": "boxcar",
    "center_frame": True,
    "pad_mode": "reflect"
}


# This still comes from settings that worked well for DTW using the old
# Edinburgh Speech Tools library
EST_MFCC = {
    "winlen": 0.025,
    "winstep": 0.005,
    "numcep": 13,
    "nfilt": 24,
    "nfft": None,
    "lowfreq": 0,
    "highfreq": 11025,
    "preemph": 0.97,
    "ceplifter": 22,
    "appendEnergy": False,
    "winfunc": np.hamming
}


def get_features(
        y,
        sr_in=vtl.AUDIO_SAMPLERATE,
        center_frame=True,
        pad_mode="symmetric",
        win_func="hamming",
        warp_alpha=None,
        warp_func="symmetric",
        feature_type=ASR_FEATS["feature_type"],
        preemphasis=ASR_FEATS["preemphasis"],
        win_length_s=ASR_FEATS["win_length_s"],
        hop_length_s=ASR_FEATS["hop_length_s"],
        n_fft=ASR_FEATS["n_fft"],
        n_mels=ASR_FEATS["n_mels"],
        mel_fmax=ASR_FEATS["mel_fmax"],
        n_mfcc=ASR_FEATS["n_mfcc"],
        lifter=ASR_FEATS["lifter"],
        multiscale=None,
        ):
    """Calculate MFCCs

    The function takes sound file name or signal as input, returns MFCC
    Matrix for region of interest in the audio file

    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (2, n)] audio signal

    sr : int
        sampling rate of audio signal, or target sr for audio file

    feature_type : str
        type of features to extract:
            - 'amp_envelope' : amplitude envelope of signal
            - 'energy_envelope' : energy envelope of signal
            - 'spectrogram' : power spectrogram
            - 'log_spectrogram' : power spectrogram in dB
            - 'mel_spectrogram' : mel freq power spectrogram
            - 'log_mel_spectrogram' : mel freq power spectrogram in dB
            - 'mfcc' : mel freq cepstral coefs

    multiscale : list
        Extract features at different scales based on coefficients in list.
        Default None.

    n_fft : int
        Can be set to None to be calculated as the next pow2 of win_len

    Returns
    -------
    feature : np.ndarray [shape=(n_coefs, n_frames)]
        Feature of `feature_type`.

    log_spectrogram : np.ndarray [shape=(n_coefs, n_frames)]
        log_spectrogram for tracking progress.
    """
    sr = 22050
    win_length = int(sr * win_length_s) if win_length_s is not None else None
    hop_length = int(sr * hop_length_s) if hop_length_s is not None else None

    if sr_in != sr:
        y = librosa.resample(y, orig_sr=sr_in, target_sr=sr)

    # preemphasis
    if preemphasis:
        y = librosa.effects.preemphasis(y, zi=[y[1]])  # fix librosa glitch

    if n_fft is None:
        n_fft = int(2**np.ceil(np.log2(win_length)))

    n_ffts = [n_fft]
    win_lengths = [win_length]
    hop_lengths = [hop_length]
    if multiscale is not None:
        for scale in multiscale[1:]:
            n_ffts += [int(n_fft * scale)]
            win_lengths += [int(win_length * scale)]
            hop_lengths += [int(hop_length * scale)]

    # multiscale loop
    feats_mul = []
    log_spectrograms_mul = []
    for n_fft, win_length, hop_length in zip(n_ffts, win_lengths, hop_lengths):
        feats, log_spectrogram = calculate_features(
            y,
            win_func,
            center_frame,
            n_fft,
            win_length,
            hop_length,
            pad_mode,
            warp_alpha,
            warp_func,
            feature_type,
            n_mels,
            mel_fmax,
            n_mfcc,
            lifter,
            )
        feats_mul.append(feats)
        log_spectrograms_mul.append(log_spectrogram)

    if not multiscale:
        feats_mul = feats_mul[0]
        log_spectrograms_mul = log_spectrograms_mul[0]

    return feats_mul, log_spectrograms_mul


def calculate_features(
        y,
        win_func,
        center_frame,
        n_fft,
        win_length,
        hop_length,
        pad_mode,
        warp_alpha,
        warp_func,
        feature_type,
        n_mels,
        mel_fmax,
        n_mfcc,
        lifter,
        ):
    """Calculate feature called from `get_fetures`.
    """
    for __ in [0]:  # hack to avoid multiple returns
        if 'envelope' in feature_type:
            if 'amp' in feature_type:
                envelope_type = 'amplitude'
            elif 'energy' in feature_type:
                envelope_type = 'energy'
            x = calculate_envelope(
                y,
                win_length=(win_length or 2048),
                hop_length=(hop_length or None),
                window=win_func,
                center=center_frame,
                pad_mode=pad_mode,
                envelope_type=envelope_type,
                )
            log_spectrogram = None  # implement if needed
            continue
        else:
            x = librosa.stft(
                y,
                window=win_func,
                center=center_frame,
                n_fft=n_fft,
                win_length=win_length,
                hop_length=hop_length,
                pad_mode=pad_mode,
                )
            x = np.abs(x**2)
            if warp_alpha is not None:
                x = vtln(x.T, warp_function=warp_func, alpha=warp_alpha).T
            log_spectrogram = librosa.power_to_db(x, top_db=None)

            if feature_type in 'spectrogram':
                continue
            if feature_type in 'log_spectrogram':
                x = log_spectrogram
                continue

            # mel features
            x = librosa.feature.melspectrogram(
                S=x,
                n_mels=n_mels,
                fmin=0,
                fmax=mel_fmax,
                )
            if feature_type == 'mel_spectrogram':
                continue

            x = librosa.power_to_db(x, top_db=None)
            if feature_type == 'log_mel_spectrogram':
                continue

            # mfccs
            if feature_type == 'mfcc':
                if lifter:
                    lifter = 2 * n_mfcc
                else:
                    lifter = 0
                x = librosa.feature.mfcc(
                    S=x,
                    n_mfcc=n_mfcc,
                    lifter=lifter
                    )
            else:
                raise ValueError(f'feature type {feature_type} not supported!')
    return x, log_spectrogram


def calculate_envelope(
        y,
        win_length=2048,
        hop_length=None,
        window="boxcar",
        center=True,
        pad_mode="reflect",
        envelope_type="amplitude",
        ):
    """Calculate envelope of the signal.
    """
    # Set the default hop, if it's not already specified
    if hop_length is None:
        hop_length = int(win_length // 4)

    window = librosa.filters.get_window(window, win_length, fftbins=False)

    # Reshape so that the window can be broadcast
    window = window.reshape((-1, 1))

    # Check audio is valid
    librosa.util.valid_audio(y)

    # Pad the time series so that frames are centered
    if center:
        if win_length > y.shape[-1]:
            librosa.warnings.warn(
                "win_length={} is too small for input signal of length={}"
                .format(win_length, y.shape[-1])
            )

        y = np.pad(y, int(win_length // 2), mode=pad_mode)

    elif win_length > y.shape[-1]:
        raise librosa.util.exceptions.ParameterError(
            "win_length={} is too small for input signal of length={}".format(
                win_length, y.shape[-1]
            )
        )

    # Window the time series.
    y_frames = librosa.util.frame(
        y, frame_length=win_length, hop_length=hop_length
        )
    if envelope_type == "amplitude":
        envelope = np.max(np.abs(y_frames), axis=0)
    elif envelope_type == "energy":
        envelope = np.sum(y_frames**2, axis=0)
    else:
        raise librosa.util.exceptions.ParameterError(
            "Envelope type {} not recognized!".format(envelope_type)
            )
    return envelope


def get_multiscale_rois(
        target_muls,
        synth_muls,
        error_type,
        word,
        wav,
        multiscale,
        rois,
        roi_coeffs,
        hop_length_s,
        ):
    """Get time aligned features or ROIs at multiple scales.

    Time aligns synthesised audio with target using DTW and returns aligned
    versions.
    If multiscale features are input, time alignments are done at each scale.
    If roi_coeffs are specified ROIs are extracted from the alignments (at each
    scale).


    Parameters
    ----------
    target_muls: np.ndarray [shape=(n_coefs, n_frames)]
        Target (template) features.
    synth_muls: np.ndarray [shape=(n_coefs, n_frames)]
        Synthesised features.
    error_type: str
    multiscale : list(float)
        List of scales for multiscale features. Default None.
    rois : list(tuple)
        Start and stop tuples of ROIs. If None then no ROIs is assumed.
        Default None.
    hop_length_s: float
        Duration of hop used for feature extraction. Necessary for the time
        alignment of ROIs.

    Returns
    -------
         synth_muls_rois_align: np.ndarray, list(np.ndarray), list(list(np.ndarray))
             Returns aligned synth features if no multiscale or ROIs are
             specified. Returns a list of np.ndarrays if either multiscale or
             ROIs are specified. Returns list of lists of np.ndarrays if both
             are specified, in which the first is a list of scales, and the
             nested lists are the ROIs.
         target_muls_rois_align:
             ditto for the targets
    """

    if multiscale is None:
        # make them lists
        synth_muls = [synth_muls]
        target_muls = [target_muls]

    # dtw alignment
    synth_muls_rois_align = []
    target_muls_rois_align = []
    scales = [1] if multiscale is None else multiscale
    # alignment is different at each scale
    for i, (scale, target_mul, synth_mul) in enumerate(
            zip(scales, target_muls, synth_muls)
            ):
        d, target_is, synth_is = dist.dtw(target_mul.T, synth_mul.T)
        synth_align = synth_mul[:, synth_is]
        target_align = target_mul[:, target_is]  # linear if smaller
        # cut the aligned synths to ROIs
        if rois:
            # generate t vector
            hop_len = hop_length_s * scale
            t_target_frames = np.arange(target_mul.shape[1]) * hop_len
            synth_align_rois = []
            target_align_rois = []
            for start, stop in rois:
                start_frame_ind = np.where(t_target_frames >= start)[0][0]
                stop_frame_ind = np.where(t_target_frames <= stop)[0][-1]
                # find their projections in the alignment
                start_align_ind = np.where(target_is == start_frame_ind)[0][0]
                stop_align_ind = np.where(target_is == stop_frame_ind)[0][-1]
                # segment them
                synth_align_roi = synth_align[
                    :, start_align_ind: stop_align_ind
                    ]
                target_align_roi = target_align[
                    :, start_align_ind: stop_align_ind
                    ]
                # aggregate
                synth_align_rois.append(synth_align_roi)
                target_align_rois.append(target_align_roi)
        else:
            # no rois
            synth_align_rois = synth_align
            target_align_rois = target_align
        synth_muls_rois_align.append(synth_align_rois)
        target_muls_rois_align.append(target_align_rois)

    if multiscale is None:
        synth_muls_rois_align = synth_muls_rois_align[0]
        target_muls_rois_align = target_muls_rois_align[0]

    return synth_muls_rois_align, target_muls_rois_align


def get_error(
        synth,
        target,
        error_type="mse",
        feature_type=None,
        mfcc_norm=False,
        mfcc_stats=None,
        use_weighting=False,
        simple_mfcc_weight=None,
        weight_type=None,
        n_mels=None,
        roi_coeffs=None,
        rois_as_list=False,
        ):
    r"""Calculate error between two arrays based on a distance measure

    The function takes two arrays of spectral parameters, e.g. MFCCs or Mel
    Spectrograms, and calculates their mean squared difference. This measure is
    then weighted using a specified weighting extracted from the coefficients.

    Parameters
    ----------
    synth : np.ndarray [shape=(n_coefs, n_frames)]
        Spectral parameters extracted from the synthesised signal

    target : np.ndarray [shape=(n_coefs, n_frames)]
        Spectral parameters extracted from the target signal

    error_type : str
        type of distance to calculate:
            - 'l1' : L1 norm averaged by coefficient and then by frame
            - 'l2' : L2 norm averaged by coefficient and then by frame
            - 'ssq' : sum of squares
            - 'mse' : mean square error
            - 'cos' : cosine distance (for MFCCs)
            - 'ang' : angular distance (for MFCCs)
            - 'sc' : spectral convergence

    feature_type : str
        type of input features:
            - 'spectrogram' : power spectrogram
            - 'log_spectrogram' : power spectrogram in dB
            - 'mel_spectrogram' : mel freq power spectrogram
            - 'log_mel_spectrogram' : mel freq power spectrogram in dB
            - 'mfcc' : mel freq cepstral coefs

    use_weighting : bool
        Set to True to apply weighting.

    weight_type : str
        weighting parameter to use:
            - 'energy' : applies energy scaling
            - 'log_energy' : applies log energy scaling

    roi_coeffs : array like
        Coefficients to multiply the error from the different ROIs with. If
        None then no ROIs is assumed.

    rois_as_list : boolean
        Add the ROI errors as a list to the end of the return

    Returns
    -------
    mse : float
        Total MSE.

    Notes
    -----
    - ROIs:
        If ROIs are used then target and synth are lists of ROIs.

    - Multiscale:
        If multiscale is used then target and synth are lists of multiscale
        features. If ROIs are used then target and synth are lists of lists
        - the first being multiscales and its items lists of ROIs.

    - MSE:
        MSE is calculated as:

        .. math::
            mse = \frac{1}{N} \sum\limits_{n=0}^{N-1}
            \frac{1}{M} \sum\limits_{i=0}^{M-1}
            (A_i[n] - B_i[n])^2

        where :math:`M` is the number of coefficients, :math:`N` is the number
        of frames, and :math:`n` the frame number.

    - Cosine and angular distances:
        These are based on cosine similarity, defined on
        Wikipedia here: https://en.wikipedia.org/wiki/Cosine_similarity

        .. math::
            sim[n] = \frac{\sum\limits_{i=0}^{M-1}{A_i[n]  B_i[n]}}
            {\sqrt{\sum\limits_{i=0}^{M-1}{A_i[n]^2}}
            \sqrt{\sum\limits_{i=0}^{M-1}{B_i[n]^2}}}

        where :math:`M` is the number of coefficients, and :math:`n` the
        frame number.

        From here accroding to Gao (2019) the cosine distance is defined as:

        .. math::
            cos = \frac{1}{N} \sum\limits_{n=0}^{N-1} (1 - sim[n])

        and angular distance defined on Wikipedia as:
        https://en.wikipedia.org/wiki/Cosine_similarity#Angular_distance_and_similarity

        .. math::
            ang = \frac{1}{N} \sum\limits_{n=0}^{N-1}
            \frac{2 \cdot \cos^{-1}(sin[n])}{\pi}

        Gao Y, Stone S, Birkholz P. Articulatory Copy Synthesis Based on
        A Genetic Algorithm. Proc. Interspeech 2019. 2019:3770-4

    - Spectral Convergence
        This is defined as:

        .. math::
                 sc = \frac{|| A - B ||_F }
                 { || A ||_F}

        where :math:`|| ||_F` is the Frobenius Norm defined as:

        .. math::
            ||A||_F = \sqrt{
                \sum\limits_{i=0}^{M-1}\sum\limits_{j=0}^{N-1}|A_{i, j}|^2
                }

        where :math:`M` is the number of coefficients, and :math:`N` is the
        number of frames.

    - MFCC energy weighting:

        For MFCCs the following transformation (DCT Type II) is used:

        .. math::
            y[k] = 2\sum_{n=0}^{N-1} x[n]\cos\pi k \frac{2n+1}{2N},
                \quad 0 \leq k < N,

        where N is the number of Mel coefficients.
        This boils down to :math:`y[0] = 2 \sum x[n]`, for the 0th coeff.
        Thus to get energy we need to scale it with the number of mel spectrum
        coefficients.
    """
    if roi_coeffs is not None:
        # ROIs are input
        roi_coeffs = np.array(roi_coeffs)
        # check if target is a list of lists to see if multiscale is used too
        multiscale = isinstance(target[0], list)
        if multiscale:
            assert len(target[0]) == len(roi_coeffs), (
                "Number of coeffs doesn't match number of ROIs"
                )
        else:
            assert len(target) == len(roi_coeffs), (
                "Number of coeffs doesn't match number of ROIs"
                )

    else:
        multiscale = isinstance(target, list)
    if multiscale:
        targets = target
        synths = synth
    else:
        targets = [target]
        synths = [synth]

    # multiscale loop
    error_muls_rois = []
    if rois_as_list:
        error_muls_rois_lists = []

    for synth_mul, target_mul in zip(synths, targets):
        if roi_coeffs is not None:
            assert isinstance(target_mul, list), 'No ROIs passed in features!'
            synth_rois = synth_mul
            target_rois = target_mul
        else:
            synth_rois = [synth_mul]
            target_rois = [target_mul]

        # roi loop
        error_rois = []
        for synth, target in zip(synth_rois, target_rois):
            error = calculate_error(
                synth,
                target,
                feature_type,
                mfcc_norm,
                mfcc_stats,
                error_type,
                use_weighting,
                weight_type,
                simple_mfcc_weight,
                n_mels,
                )
            error_rois.append(error)

        if rois_as_list:
            error_muls_rois_lists.append(error_rois)

        if roi_coeffs is not None:
            error_rois = np.array(error_rois)
            error_rois_mean = weighted_mean(error_rois, roi_coeffs)
        else:
            error_rois_mean = error_rois[0]

        error_muls_rois.append(error_rois_mean)

    if multiscale:
        error_muls_rois = np.array(error_muls_rois)
        error_muls_rois_mean = np.mean(error_muls_rois)
        if rois_as_list:
            error_muls_rois_lists = np.array(error_muls_rois_lists)
            error_muls_rois_means = np.mean(error_muls_rois_lists, axis=0)
            assert np.allclose(
                error_muls_rois_mean,
                weighted_mean(error_muls_rois_means, roi_coeffs)
                ), "Means per ROI don't match total mean!"
    else:
        error_muls_rois_mean = error_muls_rois[0]
        if rois_as_list:
            error_muls_rois_means = error_muls_rois_lists[0]
            error_muls_rois_means = np.array(error_muls_rois_means)
            assert np.allclose(
                error_muls_rois_mean,
                weighted_mean(error_muls_rois_means, roi_coeffs)
                ), "Means per ROI don't match total mean!"
        else:
            error_muls_rois_mean = error_muls_rois[0]

    if rois_as_list:
        return error_muls_rois_mean, error_muls_rois_means
    else:
        return error_muls_rois_mean


def weighted_mean(xs, coeffs=None):
    assert len(coeffs) == len(xs), "Number of coeffs doesn't match xs"
    return np.sum(xs * coeffs) / np.sum(coeffs)


def calculate_error(
        synth,
        target,
        feature_type,
        mfcc_norm,
        mfcc_stats,
        error_type,
        use_weighting,
        weight_type,
        simple_mfcc_weight,
        n_mels,
        ):
    """Calculate error in the inner loop of `get_error`.
    """
    if feature_type == 'mfcc' and mfcc_norm:
        means, stds, mins, maxs = mfcc_stats
        # zero mean, unit std the rest
        target = np.transpose((target.T - means) / stds)
        synth = np.transpose((synth.T - means) / stds)

    # calculate error array (n_frames,)
    if error_type == 'l1':
        error = np.sum(np.abs(target - synth), axis=0)
    elif error_type == 'l2':
        error = np.sqrt(
            np.sum((target - synth)**2, axis=0)
            )
    elif error_type == 'ssq':
        error = np.sum((target - synth)**2, axis=0)
    elif error_type == 'mse':
        error = np.mean((target - synth)**2, axis=0)
    elif error_type in ['cos', 'ang']:
        # calculate similarity
        error = (
            np.sum(target.T * synth.T, axis=1)  # row wise multiplication
            / (
                np.sqrt(np.sum(target**2, axis=0))
                * np.sqrt(np.sum(synth**2, axis=0))
                )
            )
        if error_type == 'cos':
            error = 1 - error
        else:  # ang
            error = 2 * np.arccos(error) / np.pi
    elif error_type == 'sc':
        error = np.sum((target - synth)**2, axis=0)  # denominator

    else:
        raise ValueError(f'Error type {error_type} not supported!')

    # Weighting
    if use_weighting:
        if 'energy' in weight_type:
            # extract energy
            if 'spectrogram' in feature_type:
                if 'log' in feature_type:
                    target = 10**(target/10)
                weights = np.sum(target, axis=0)
                if 'log' in weight_type:
                    weights_max = np.max(weights)
                    weights = librosa.power_to_db(
                        weights, ref=weights_max, top_db=None
                        )
            # mfccs
            elif feature_type == 'mfcc':
                # 0th coeff gives summed log energy
                weights = target[0, :]
                if not simple_mfcc_weight:
                    if mfcc_norm:  # de norm
                        weights = weights * stds[0] + means[0]
                    # average log energy in dB per mel_spectrogram coeff
                    weights = weights / (2*n_mels)
                    weights = 10**(weights/10)  # avg mel coeff power
                    weights = weights * n_mels  # sum of power
                    if 'log' in weight_type:
                        weights_max = np.max(weights)
                        weights = librosa.power_to_db(
                            weights, ref=weights_max, top_db=None
                            )

        # set energy minimum in case there is no silence in target audio
        if feature_type == 'mfcc':
            if simple_mfcc_weight:
                if 'log' not in weight_type:
                    LOGGER.warning(
                        'get_error(): Simple MFCC energy weighting is log '
                        'energy based and weight type is set to energy.'
                        )
                if mfcc_norm:
                    e_min = (mins[0] - means[0]) / stds[0]
                else:
                    means, stds, mins, maxs = mfcc_stats
                    e_min = mins[0]
            else:
                e_min = mins[0] / (2*n_mels)
                e_min = 10**(e_min/10)  # min mel coeff power
                e_min = e_min * n_mels  # sum of mins
                if 'log' in weight_type:
                    e_min = librosa.power_to_db(
                        e_min, ref=weights_max, top_db=None
                        )

        elif 'log' in weight_type:
            e_min = -50  # dB - heuristically set
            # maybe a statistical analysis would be overkill
        else:
            e_min = 0
        # assuming target audio is not complete silence:
        e_max = np.max(weights)

        # normalise weights to 0 - 1
        weights = (weights - e_min)/(e_max - e_min)
        error = error * weights

    if error_type == 'ssq':
        error = np.sum(error)
    elif error_type in 'l1 l2 mse cos ang'.split():
        error = np.mean(error)
    elif error_type == 'sc':
        error = np.sqrt(np.sum(error))
        if use_weighting:
            error_nom = np.sqrt(
                np.sum(np.sum((target)**2, axis=0) * weights)
                )
        else:
            error_nom = np.sqrt(np.sum((target)**2))
        error = error / error_nom

    return error


def get_mfccs(pcm_samples,
              sr=vtl.AUDIO_SAMPLERATE,
              delta=True,
              accel=True,
              c0=True,
              winlen=EST_MFCC["winlen"],
              winstep=EST_MFCC["winstep"],
              numcep=EST_MFCC["numcep"],
              nfilt=EST_MFCC["nfilt"],
              nfft=EST_MFCC["nfft"],
              lowfreq=EST_MFCC["lowfreq"],
              highfreq=EST_MFCC["highfreq"],
              preemph=EST_MFCC["preemph"],
              ceplifter=EST_MFCC["ceplifter"],
              appendEnergy=EST_MFCC["appendEnergy"],
              winfunc=EST_MFCC["winfunc"]):
    if accel and not delta:
        raise ValueError("Cannot include accel without delta...")

    y = pcm_samples

    settings = {
        "winlen": winlen,
        "winstep": winstep,
        "numcep": numcep,
        "nfilt": nfilt,
        "nfft": nfft,
        "lowfreq": lowfreq,
        "highfreq": highfreq,
        "preemph": preemph,
        "ceplifter": ceplifter,
        "appendEnergy": appendEnergy,
        "winfunc": winfunc
    }

    feats = psfeat.mfcc(y, sr, **settings)

    if not c0:
        feats = feats[:, 1:]

    if delta:
        dfeats = psfeat.delta(feats, 2)
        if accel:
            afeats = psfeat.delta(dfeats, 2)
            dfeats = np.concatenate((dfeats, afeats), axis=1)
        feats = np.concatenate((feats, dfeats), axis=1)

    return feats
