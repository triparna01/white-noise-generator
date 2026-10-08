# 🔊 White Noise Generator

A Python-based white noise generation and analysis application that generates Gaussian white noise, controls its audio parameters, analyzes its signal properties, and provides the resulting WAV file for playback and download.


🌐 **[Live Demo](https://white-noise-generator-111.streamlit.app/)**

Generate, visualize, analyze, and download white noise using Python.

The project was developed with a research-oriented approach and is inspired by the study:

> Egeland J, Lund O, Kowalik-Gran I, Aarlien AK, Söderlund GBW (2023).
> *Effects of auditory white noise stimulation on sustained attention and response time variability.*

---

## 📌 Project Overview

White noise is a signal containing a broad range of frequencies with approximately equal power across the frequency spectrum.

This project provides an interactive Streamlit application for:

* Generating Gaussian white noise
* Controlling duration and sampling rate
* Controlling RMS level in dBFS
* Generating mono or stereo audio
* Applying fade-in and fade-out
* Measuring RMS level
* Measuring peak level
* Detecting clipping
* Visualizing the waveform
* Analyzing the Power Spectral Density (PSD)
* Measuring spectral flatness
* Playing the generated audio
* Downloading the generated WAV file

The goal is not only to generate audio but also to **validate whether the generated signal behaves as expected for white noise**.

---

## 🧠 Research Context

The project is inspired by research investigating the effects of auditory white noise stimulation on sustained attention and response-time variability.

The application therefore focuses specifically on **white noise generation and signal analysis** rather than providing multiple types of noise.

The research context motivated the inclusion of measurable signal properties such as:

* RMS level
* dBFS level
* Peak amplitude
* Power Spectral Density
* Spectral flatness
* Clipping detection

These measurements help verify the characteristics of the generated stimulus.

---

## ⚙️ How It Works

The application follows this pipeline:

```text
User Parameters
       ↓
Gaussian Random Noise
       ↓
Fade In / Fade Out
       ↓
RMS Normalization
       ↓
Peak / Clipping Check
       ↓
16-bit PCM Conversion
       ↓
WAV File
       ↓
Signal Analysis
       ↓
Waveform + PSD + Spectral Flatness
```

### 1. White Noise Generation

Gaussian random samples are generated using NumPy.

```python
rng.normal(
    loc=0.0,
    scale=1.0,
    size=num_samples
)
```

The samples are then processed to produce the desired audio signal.

### 2. RMS Level Control

The target RMS level is specified in dBFS.

The conversion from dBFS to linear RMS is:

```text
RMS = 10^(dBFS / 20)
```

For example:

```text
-20 dBFS → RMS = 0.1
```

### 3. Fade Processing

Optional fade-in and fade-out envelopes can be applied to reduce abrupt transitions at the beginning and end of the signal.

### 4. Clipping Protection

The generated signal is checked for excessive peak amplitude.

If the peak exceeds the safe threshold, the signal is scaled down before conversion to 16-bit PCM.

### 5. Signal Analysis

The application calculates:

**RMS**

Measures the effective amplitude of the signal.

**Peak Level**

Measures the maximum absolute amplitude.

**Clipping**

Checks whether the signal reaches the limits of 16-bit PCM.

**Power Spectral Density**

Uses Welch's method to analyze how signal power is distributed across frequencies.

**Spectral Flatness**

Measures how evenly power is distributed across the frequency spectrum.

A value closer to 1 indicates a flatter spectrum.

---

## 🖥️ Application Features

### Audio Parameters

The user can configure:

| Parameter      | Description                            |
| -------------- | -------------------------------------- |
| Duration       | Length of generated audio              |
| Sampling Rate  | Number of samples generated per second |
| Target Level   | Desired RMS level in dBFS              |
| Audio Channels | Mono or stereo                         |
| Fade In        | Optional fade-in duration              |
| Fade Out       | Optional fade-out duration             |
| Random Seed    | Optional reproducible generation       |

### Signal Validation

The application displays:

* Duration
* Sampling rate
* Number of samples
* RMS
* RMS level
* Peak level
* Clipping status

### Visualization

The application provides:

* Time-domain waveform
* Power Spectral Density plot
* Spectral flatness measurement

### Audio Output

The generated signal can be:

* Played directly in the application
* Downloaded as a `.wav` file

---

## 🧪 Testing

The project includes automated tests using `pytest`.

The test suite verifies:

* Correct sample count
* Target RMS level
* Reproducibility using a fixed random seed
* Stereo output shape
* Mono output shape
* Absence of clipping

Run the tests with:

```bash
pytest -v
```

Current test suite:

```text
6 tests passed
```

---

## 🛠️ Technologies Used

### Python

Core programming language.

### NumPy

Used for:

* Random noise generation
* Array operations
* RMS calculations
* Signal scaling

### SciPy

Used for:

* WAV file generation
* Power Spectral Density analysis
* Welch's method

### Matplotlib

Used for:

* Waveform visualization
* PSD visualization

### Streamlit

Used to create the interactive web application.

### Pytest

Used for automated testing.

---

## 📁 Project Structure

```text
white-noise-generator/
│
├── .venv/
│
├── output/
│   └── white_noise.wav
│
├── app.py
├── generator.py
├── test_generator.py
├── requirements.txt
└── README.md
```

### `generator.py`

Contains the core white-noise generation logic.

### `app.py`

Contains the Streamlit user interface and signal analysis.

### `test_generator.py`

Contains automated tests for the generator.

### `requirements.txt`

Contains the Python dependencies required to run the project.

### `output/`

Stores generated WAV files.

---

## 🚀 Installation

Clone the repository and navigate into the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit application with:

```bash
python -m streamlit run app.py
```

Streamlit will open the application in your browser.

---

## 🔬 Example Validation Result

For a typical configuration:

```text
Duration:          10 seconds
Sampling Rate:     44100 Hz
Target Level:      -20 dBFS
Channels:          Mono
```

The generated signal can be validated through its measured RMS level, peak level, waveform, PSD, and spectral flatness.

For example, a generated signal may produce a spectral flatness value around:

```text
0.99+
```

A value close to 1 indicates a highly flat spectrum, which is consistent with the expected spectral characteristics of white noise.

---

## 🎯 Learning Objectives

This project demonstrates practical understanding of:

* Python programming
* NumPy arrays
* Random signal generation
* Digital audio representation
* Sampling rate
* RMS amplitude
* dBFS
* Signal normalization
* Clipping
* WAV/PCM audio
* Time-domain analysis
* Frequency-domain analysis
* Power Spectral Density
* Spectral flatness
* Automated testing
* Streamlit application development

---

## 🔮 Future Improvements

Possible future improvements include:

* Improved experimental controls for research use
* More detailed statistical signal analysis
* Saving analysis results alongside generated audio
* Automated experiment/session logging
* Additional validation against predefined signal-quality criteria

---

## 📚 Reference

Egeland J, Lund O, Kowalik-Gran I, Aarlien AK, Söderlund GBW (2023).

*Effects of auditory white noise stimulation on sustained attention and response time variability.*

---

## 👩‍💻 Author

Developed as a Python signal
