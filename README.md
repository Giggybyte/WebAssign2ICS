## WebAssign2ICS
This Python script takes a WebAssign login as input and exports a list of your current/upcoming assignments to an .ics (calendar) file.

## Usage
![Usage](https://i.imgur.com/fkP3r5v.png)  
Download the source code and run `main.py` from the command line. Make sure `dateparse.py` is in the same folder.
Once your .ics file is created, you are free to import it into a program that supports it, like Google Calendar. 

## What's WebAssign?
WebAssign is a website used by college math professors to assign homework to their students. 

## Why'd you make this?
As a college student, it's important to stay organized and have a general idea of what's next on the to-do list, but it's tedious to pop open a browser and check the website -- this program basically just saves time.

## When did you make this?
I wrote this on a weekend as a freshman at VT that quickly got fed up with not having all of my assignments in one place.

## What's next?
- Automation
  - Let users have the option to log in with their user/pass defined in an external file, so this script could be run automatically with something like `cron`.
