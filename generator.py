import numpy as np
from scipy.io import wavfile


def generate_white_noise(
    duration,
    sample_rate,
    target_dbfs,
    output_file,
    seed=None,
    channels=1,
    fade_in=0,
    fade_out=0
):
    """
    Generate Gaussian white noise at a target RMS level.

    Parameters:
        duration (float): Duration in seconds.
        sample_rate (int): Sampling frequency in Hz.
        target_dbfs (float): Desired RMS level in dBFS.
        output_file (str): WAV output path.
        seed (int or None): Random seed for reproducibility.
        channels (int): Number of audio channels.
        fade_in (float): Fade-in duration in seconds.
        fade_out (float): Fade-out duration in seconds.

    Returns:
        numpy.ndarray: Generated 16-bit audio signal.
    """

    # Calculate number of samples
    num_samples = int(duration * sample_rate)

    # Create random number generator
    rng = np.random.default_rng(seed)

    # Generate Gaussian white noise
    if channels == 1:
        noise = rng.normal(
            loc=0.0,
            scale=1.0,
            size=num_samples
        )
    else:
        noise = rng.normal(
            loc=0.0,
            scale=1.0,
            size=(num_samples, channels)
        )

    # Create amplitude envelope
    envelope = np.ones(num_samples)

    # Apply fade-in
    if fade_in > 0:
        fade_in_samples = int(fade_in * sample_rate)
        fade_in_samples = min(fade_in_samples, num_samples)

        envelope[:fade_in_samples] = np.linspace(
            0,
            1,
            fade_in_samples
        )

    # Apply fade-out
    if fade_out > 0:
        fade_out_samples = int(fade_out * sample_rate)
        fade_out_samples = min(fade_out_samples, num_samples)

        envelope[-fade_out_samples:] = np.linspace(
            1,
            0,
            fade_out_samples
        )

    # Apply fade envelope
    if channels > 1:
        noise = noise * envelope[:, np.newaxis]
    else:
        noise = noise * envelope

    # Calculate RMS after applying fade
    current_rms = np.sqrt(
        np.mean(noise ** 2)
    )

    # Convert target dBFS to linear RMS
    target_rms = 10 ** (target_dbfs / 20)

    # Scale signal to target RMS
    noise = noise * (target_rms / current_rms)

    # Check for potential clipping
    peak = np.max(np.abs(noise))

    # Reduce the entire signal if the peak is too high
    if peak > 0.99:
        noise = noise * (0.99 / peak)

    # Convert to 16-bit PCM
    noise_16bit = np.int16(
        noise * 32767
    )

    # Save WAV file
    wavfile.write(
        output_file,
        sample_rate,
        noise_16bit
    )

    return noise_16bit