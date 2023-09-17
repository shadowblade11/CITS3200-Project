<!-- Using HTML markdown so as to not mess with auto table of contents generation. -->
<h1>CITS3200-Project</h1>  
**Scoring oral skills**  

<h2> Table of Contents </h2>  

- [Project Description](#project-description)
- [Setting up the Workspace](#setting-up-the-workspace)
  - [Windows](#windows)
  - [Linux/MacOS](#linuxmacos)
- [Running the App](#running-the-app)
- [Relevant links:](#relevant-links)

## Project Description
This project has a two-fold aim. On one hand, it aims at providing students of Italian from the beginners stream a way of monitoring their progress in the area of pronunciation and fluency. On the other, it is meant to provide data for the investigation of whether repetition of strings of words impacts the learning of pronunciation and fluency in Italian, and whether an innovative way of receiving feedback motivates students in their learning.  
The project involves the development of an application that will allow students to engage in the following sequence of tasks:  

students listen to authentic Italian audio  
students repeat what they hear  
students evaluate how close they think their input is to the original  
students are being scored through the use of audio similarity APIs to compute a similarity score, which can be compared with the students own evaluation.  

## Setting up the Workspace

Follow these instructions to set up the workspace for different platforms.  
> [Windows](#windows)  
> [Linux/MacOS](#linuxmacos)
---
### Windows

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

---

### Linux/MacOS

Ensure Python virtual environment is installed. If not, it can be installed using:

**For Linux:**
```bash
sudo apt install python-virtualenv
```
**For MacOS:**
```bash
sudo python3 -m pip install virtualenv
```

**Setting up your workspace:**

```bash
python3 -m venv .venv
source ./.venv/bin/activate
python -m pip install -r requirements.txt
```

> **Note:** The virtual environment initialization is successful if you see `(.venv)` to the left of the command line. You will need to restart the virtual environment every time you restart the project. This can be done by re-running `source ./.venv/bin/activate`. (Note: slightly different to Windows command)
> To deactivate venv, run `deactivate`

**Setting up the database**

Initialize the database with
```bash
flask db init
flask db migrate
flask db upgrade
```

---
## Running the App
Run app with  
```bash
flask --app app run
```
while within the virtual environment. (.venv)  

## Relevant links:
[Figma](https://www.figma.com/file/iRdR7IwBRmGQy51VEWec3x/Student-Login?type=design&node-id=0%3A1&mode=design&t=RxDeRqttoMxhIba1-1) (website design)

