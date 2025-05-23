
# Audioset Downloader

A Python script to download audio clips from Google's AudioSet dataset.

## Table of Contents

* [Introduction](#introduction)
* [Folder Structure](#folder-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Features](#features)
* [Dependencies](#dependencies)
* [Configuration](#configuration)
* [Documentation](#documentation)
* [Examples](#examples)
* [Troubleshooting](#troubleshooting)
* [Contributors](#contributors)
* [License](#license)

## Introduction

This project provides scripts to download audio clips from Google's AudioSet dataset. It utilizes metadata CSV files to identify and retrieve specific audio segments.

## Folder Structure

The repository contains the following files:

* `balanced_train_loader.py`: Script to download audio clips from the balanced training set.
* `eval_loader.py`: Script to download audio clips from the evaluation set.
* `balanced_train_segments.csv`: Metadata for the balanced training set.
* `eval_segments.csv`: Metadata for the evaluation set.
* `class_labels_indices.csv`: Mapping of class labels to their corresponding indices.
* `requirements.txt` : consists of requirements 

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AnubhavSaha2006/Audioset_Downloader.git
   cd Audioset_Downloader
   ```



2. **Install Python dependencies:**

   Ensure you have Python 3 installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```




3. **Install FFmpeg:**

   FFmpeg is required for processing audio files. Download and install it from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/).

   Ensure FFmpeg is added to your system's PATH.

## Usage

1. **Download Balanced Training Set:**

   ```bash
   python balanced_train_loader.py
   ```



2. **Download Evaluation Set:**

   ```bash
   python eval_loader.py
   ```



\*Note: Ensure the corresponding CSV metadata files (`balanced_train_segments.csv` and `eval_segments.csv`) are present in the same directory as the scripts.\*

## Features

* Download audio clips from Google's AudioSet dataset.
* Utilize metadata CSV files for targeted downloads.
* Support for both balanced training and evaluation sets.

## Dependencies

* Python 3.x
* FFmpeg
* Additional Python packages as specified in `requirements.txt`

## Configuration

Currently, the scripts use hardcoded paths and settings. For enhanced flexibility, consider modifying the scripts to accept command-line arguments or configuration files.

## Documentation

For more information on Google's AudioSet dataset, visit the [AudioSet website](https://research.google.com/audioset/).

## Examples

To download the balanced training set:

```bash
python balanced_train_loader.py
```



To download the evaluation set:

```bash
python eval_loader.py
```



## Troubleshooting

* **FFmpeg not found:** Ensure FFmpeg is installed and added to your system's PATH.
* **Missing CSV files:** Ensure all necessary metadata CSV files are present in the directory.
* **Permission issues:** Run the scripts with appropriate permissions or adjust file permissions as needed.

## Contributors
* [AnubhavSaha2006](https://github.com/AnubhavSaha2006)

Please ensure all required files are present and paths are correctly set before running the scripts.
