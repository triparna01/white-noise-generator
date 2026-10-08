import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from generator import generate_white_noise


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="White Noise Generator",
    page_icon="🔊",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🔊 White Noise Generator")

st.write(
    "Generate, visualize, analyze, and download "
    "white noise using Python."
)


# ==========================================
# SIDEBAR - NOISE PARAMETERS
# ==========================================

st.sidebar.header("Noise Parameters")


duration = st.sidebar.number_input(
    "Duration (seconds)",
    min_value=1,
    max_value=60,
    value=10
)


sample_rate = st.sidebar.selectbox(
    "Sampling Rate (Hz)",
    [8000, 16000, 22050, 44100, 48000],
    index=3
)


channels = st.sidebar.selectbox(
    "Audio Channels",
    ["Mono", "Stereo"]
)

channel_count = 1 if channels == "Mono" else 2


target_dbfs = st.sidebar.slider(
    "Target Level (dBFS)",
    min_value=-40.0,
    max_value=-1.0,
    value=-20.0,
    step=1.0
)


fade_in = st.sidebar.slider(
    "Fade In (seconds)",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.5
)


fade_out = st.sidebar.slider(
    "Fade Out (seconds)",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.5
)


use_seed = st.sidebar.checkbox(
    "Use fixed random seed",
    value=False
)


seed = st.sidebar.number_input(
    "Random Seed",
    min_value=0,
    value=42,
    step=1
)


# ==========================================
# GENERATE BUTTON
# ==========================================

generate_button = st.button(
    "🎵 Generate White Noise",
    type="primary"
)


# ==========================================
# GENERATION
# ==========================================

if generate_button:

    with st.spinner("Generating white noise..."):

        output_file = "output/white_noise.wav"

        noise = generate_white_noise(
            duration=duration,
            sample_rate=sample_rate,
            target_dbfs=target_dbfs,
            output_file=output_file,
            seed=seed if use_seed else None,
            channels=channel_count,
            fade_in=fade_in,
            fade_out=fade_out
        )


    st.success("White noise generated successfully! 🎉")


    # ======================================
    # SIGNAL ANALYSIS
    # ======================================

    # Convert 16-bit PCM to normalized amplitude
    normalized_noise = noise.astype(np.float64) / 32767.0


    # Calculate RMS
    rms = np.sqrt(
        np.mean(normalized_noise ** 2)
    )


    # Convert RMS to dBFS
    dbfs = 20 * np.log10(rms)


    # Calculate peak amplitude
    peak = np.max(
        np.abs(normalized_noise)
    )


    # Convert peak to dBFS
    peak_dbfs = 20 * np.log10(peak)


    # Detect clipping
    clipped = np.any(
        np.abs(noise) >= 32767
    )


    # ======================================
    # SIGNAL VALIDATION
    # ======================================

    st.subheader("🔬 Signal Validation")

    col1, col2, col3, col4, col5, col6 = st.columns(6)


    col1.metric(
        "Duration",
        f"{duration} sec"
    )


    col2.metric(
        "Sampling Rate",
        f"{sample_rate} Hz"
    )


    col3.metric(
        "Samples",
        f"{len(noise):,}"
    )


    col4.metric(
        "RMS",
        f"{rms:.4f}"
    )


    col5.metric(
        "RMS Level",
        f"{dbfs:.2f} dBFS"
    )


    col6.metric(
        "Peak Level",
        f"{peak_dbfs:.2f} dBFS"
    )


    if clipped:
        st.warning(
            "⚠️ Clipping detected in the audio."
        )
    else:
        st.success(
            "✅ No clipping detected."
        )


    # ======================================
    # AUDIO PLAYER
    # ======================================

    st.subheader("🔊 Generated Audio")


    with open(output_file, "rb") as audio_file:
        audio_bytes = audio_file.read()


    st.audio(
        audio_bytes,
        format="audio/wav"
    )


    # ======================================
    # WAVEFORM
    # ======================================

    st.subheader("📈 Waveform")


    time = np.arange(
        len(noise)
    ) / sample_rate


    fig, ax = plt.subplots(
        figsize=(12, 4)
    )


    ax.plot(
        time,
        noise
    )


    ax.set_xlabel(
        "Time (seconds)"
    )

    ax.set_ylabel(
        "Amplitude"
    )

    ax.set_title(
        "White Noise Waveform"
    )

    ax.grid(True)


    st.pyplot(fig)

    plt.close(fig)


    # ======================================
    # POWER SPECTRAL DENSITY
    # ======================================

    st.subheader("📊 Power Spectral Density")


    frequencies, power = signal.welch(
        noise,
        fs=sample_rate,
        nperseg=4096,
        axis=0
    )


    # ======================================
    # SPECTRAL FLATNESS
    # ======================================

    if channel_count == 1:
        power_for_flatness = power
    else:
        power_for_flatness = np.mean(
            power,
            axis=1
        )


    # Prevent log(0)
    power_for_flatness = np.maximum(
        power_for_flatness,
        np.finfo(float).eps
    )


    geometric_mean = np.exp(
        np.mean(
            np.log(power_for_flatness)
        )
    )


    arithmetic_mean = np.mean(
        power_for_flatness
    )


    spectral_flatness = (
        geometric_mean / arithmetic_mean
    )


    st.metric(
        "Spectral Flatness",
        f"{spectral_flatness:.4f}"
    )


    if spectral_flatness >= 0.95:

        st.success(
            "✅ Spectrum is highly flat and "
            "consistent with white noise."
        )

    else:

        st.warning(
            "⚠️ Spectrum is less flat than "
            "expected for ideal white noise."
        )


    # ======================================
    # PSD PLOT
    # ======================================

    fig, ax = plt.subplots(
        figsize=(12, 4)
    )


    if channel_count == 1:

        ax.semilogy(
            frequencies,
            power
        )

    else:

        ax.semilogy(
            frequencies,
            power[:, 0],
            label="Left"
        )

        ax.semilogy(
            frequencies,
            power[:, 1],
            label="Right"
        )

        ax.legend()


    ax.set_xlabel(
        "Frequency (Hz)"
    )

    ax.set_ylabel(
        "Power / Hz"
    )

    ax.set_title(
        "White Noise Power Spectral Density"
    )

    ax.grid(True)


    st.pyplot(fig)

    plt.close(fig)


    # ======================================
    # DOWNLOAD
    # ======================================

    st.subheader("💾 Download")


    st.download_button(
        label="⬇️ Download WAV File",
        data=audio_bytes,
        file_name="white_noise.wav",
        mime="audio/wav"
    )
