<!-- Using HTML markdown so as to not mess with auto table of contents generation. -->
<h1 style="text-align:center">CITS3200 PROJECT: SCORING ORAL SKILLS</h1>

<h2> TABLE OF CONTENTS </h2>  

- [PROJECT DESCRIPTION](#project-description)
- [SETTING UP THE WORKSPACE](#setting-up-the-workspace)
  - [WINDOWS](#windows)
  - [LINUX / MACOS](#linux--macos)
- [EXTRA SOFTWARE](#extra-required-software)
  - [WINDOWS](#for-windows)
  - [LINUX](#for-linux)
  - [MACOS](#for-macos)
- [RUNNING THE APP](#running-the-app)
- [RELEVANT LINKS](#relevant-links)

## PROJECT DESCRIPTION
This project has a two-fold aim. On the one hand, it aims to provide students of Italian from the beginner stream a way of improving their pronunciation and fluency. On the other, it is meant to provide data for investigating whether repetition of strings of words impacts the learning of pronunciation and fluency in Italian and whether an innovative way of receiving feedback motivates students in their learning.  

The project involves the development of an application that will allow students to engage in the following sequence of tasks:  
<p>&ensp;- Students listen to authentic Italian audio clips.</p>  
<p>&ensp;- Students repeat to the best of their ability what they heard.</p>  
<p>&ensp;- Students self-evaluate how close their selected attempt is to the original clip.</p> 
<p>&ensp;- Students scored using an audio similarity function, and the score generated is compared with their self-evaluation score.</p>

## SETTING UP THE WORKSPACE

Follow these instructions to set up the workspace for different platforms.  
[WINDOWS](#windows)  
[LINUX / MACOS](#linux--macos)

### WINDOWS

Ensure Python virtual environment is installed. If not, it can be installed using:

```bash
python3 -m pip install virtualenv
```

To set up your workspace:

```bash
python3 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

> **Note:** The virtual environment initialization is successful if you see `(.venv)` to the left of the command line. You will need to restart the virtual environment every time you restart the project. This can be done by re-running `.\.venv\Scripts\activate`. (Note: slightly different to MacOS/Linux command)
> To deactivate venv, run `deactivate`

### LINUX / MACOS

Ensure Python virtual environment is installed. If not, it can be installed using:

**For Linux:**
```bash
sudo apt install python-virtualenv
```
---
**For MacOS:**
```bash
sudo python3 -m pip install virtualenv
```
---
**Setting up your workspace:**

```bash
python3 -m venv .venv
source ./.venv/bin/activate
python -m pip install -r requirements.txt
```

> **Note:** The virtual environment initialization is successful if you see `(.venv)` to the left of the command line. You will need to restart the virtual environment every time you restart the project. This can be done by re-running `source ./.venv/bin/activate`. (Note: slightly different to Windows command)
> To deactivate venv, run `deactivate`
---
**Setting up the database:**

Initialize the database with
```bash
flask db init
flask db migrate
flask db upgrade
```

## EXTRA REQUIRED SOFTWARE
**FFmpeg** is a powerful multimedia framework that can be used to record, convert, and stream audio and video. It's an essential tool for handling multimedia files in various applications and is required for this project to work.

Follow these instructions to set up the workspace for different platforms.  
[WINDOWS](#for-windows)   
[LINUX](#for-linux)   
[MACOS](#for-macos) 

### INSTALLATION
---
#### For Windows:

Head to [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) and download the latest **fullbuild** 7zip file.

Extract the content from the zip file using your choice of software (Suggested: [ezy7zip](https://www.ezyzip.com/unzip-7z-files.html) as you can just download the file you need).

Drag the **ffmpeg.exe** file into the project folder (the **ffmpeg.exe** should be located in ffmpeg-X.X-full_build/bin unless using the suggested website to download the exe file individually).

Below is an image of where ffmpeg.exe should be located.

![image depicting where ffmpeg.exe should be located](readmeImages\Capture.PNG)

---
#### For Linux:

Update the package list first
```bash
sudo apt update
```

Then, run the following command
```bash
sudo apt install ffmpeg
```
---
#### For MacOS:

Please ensure that **brew** is installed.

Update brew
```bash
brew update
```

Then, run the following command
```bash
brew install ffmpeg
```

## RUNNING THE APP
Run the app with  
```bash
flask --app app run
```
while within the virtual environment. (.venv)  

## RELEVANT LINKS
[Figma](https://www.figma.com/file/iRdR7IwBRmGQy51VEWec3x/Student-Login?type=design&node-id=0%3A1&mode=design&t=RxDeRqttoMxhIba1-1) (website design)

[Flask](https://flask.palletsprojects.com/en/2.3.x/) (Python Framework)

