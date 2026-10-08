import numpy as np
from generator import generate_white_noise


def test_correct_sample_count(tmp_path):
    output_file = tmp_path / "test.wav"

    noise = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file
    )

    expected_samples = 2 * 44100

    assert len(noise) == expected_samples

def test_target_rms(tmp_path):
    output_file = tmp_path / "test.wav"

    noise = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file
    )

    normalized_noise = noise.astype(np.float64) / 32767.0

    rms = np.sqrt(np.mean(normalized_noise ** 2))

    assert np.isclose(rms, 0.1, atol=0.002)

def test_reproducibility_with_seed(tmp_path):
    output_file_1 = tmp_path / "test1.wav"
    output_file_2 = tmp_path / "test2.wav"

    noise_1 = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file_1,
        seed=42
    )

    noise_2 = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file_2,
        seed=42
    )

    assert np.array_equal(noise_1, noise_2)

def test_stereo_output(tmp_path):
    output_file = tmp_path / "stereo.wav"

    noise = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file,
        channels=2
    )

    assert noise.shape == (88200, 2)

def test_no_clipping(tmp_path):
    output_file = tmp_path / "test.wav"

    noise = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file
    )

    assert np.max(np.abs(noise)) < 32767

def test_mono_output(tmp_path):
    output_file = tmp_path / "mono.wav"

    noise = generate_white_noise(
        duration=2,
        sample_rate=44100,
        target_dbfs=-20,
        output_file=output_file,
        channels=1
    )

    assert noise.shape == (88200,)