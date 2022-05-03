# playlist_org

Organize an audio playlist optimized for [SanDisk Clip Jam MP3 Player](./docs/clipjam.pdf)

## Table of Contents
1. [The Problem](#the-Problem)
2. [The Solution](#the-solution)
3. [Community](#community)
4. [Runbook](#runbook)
5. [Local Development](#local-development)

## The Problem

I own a lot of audio books on CDs. Audio books always come with multiple CDs. Each CD typically has a dozen or so MP3s. I want to listen to those MP3s on my audio player. When I rip the CD using Windows Media Player it will create a folder and place the tracks on that CD into the folder. In the below example I have burned three CDs; each CD generates its own folder and each track in that folder starts at track 1 through track n.

![Data Input](./docs/problem.png "Data Input")

However, this is not ideal. The MP3 player expects one folder with all tracks in sequential order.

![MP3 Player expectation](./docs/solution.png "MP3 Player expectation")

One additional problem is that the player can, at most, have 128 tracks in a single folder.

## The Solution

This program, [audio.py](./organizer/audio.py), will address the problems outlined above. First and foresmost a little setup is needed. This [configuration file](./organizer/config.py) must specify the source MP3s directory, the directory where the generated MP3s should be placed, and the maximum number of tracks allowed (again this specific player has a maxium of 128).
Once this one-time setup is complete we can run our program which will move/rename files (using a transient file for bookkeeping) from their source directory into the destination directory resulting in the following:

![Data Transition](./docs/transition.png "Data Transition")

If necessary the tracks will need to be combined if there are more than the maximum limit specified in the configuration file. For instance if there are 130 MP3s in our destination folder, combine tracks #1 and #2 together, then tracks #3 and #4, and so on for a new, acceptable total of 75 tracks.

Once completed, copy the folder onto the device via usb cable and enjoy the audio book!

## Community

 * [Code of Conduct](CODE_OF_CONDUCT.md)
 * [Contribute](CONTRIBUTING.md)
 * [To submit a bug](./CONTRIBUTING.md#reporting-bugs)
 * [To submit a feature](./CONTRIBUTING.md#suggesting-enhancements)
 * [To ask questions, comment, etc](https://github.com/ruddycase/playlist_org/discussions)

## Runbook

### Prerequistes

[python3](https://www.python.org/downloads/) and configure [configuration file](./organizer/config.py) properly

### Execution

```bash
cd organizer
python audio.py
```
## Local Development

### Setup

Install development project dependencies
```bash
pip install -r requirements_dev.txt
```

### Testing

The unittest module is used for all testing purposes.

#### Execute all tests

```bash
cd organizer
python -m unittest discover
```

#### Execute singular test

```bash
python -m unittest tests.test_basic
```

### Continuous Integration

#### Github Actions

[Github Actions](https://github.com/features/actions) is triggered on every push to run all unit test and lint all python files.

Github Actions History - https://github.com/ruddycase/playlist_org/actions
