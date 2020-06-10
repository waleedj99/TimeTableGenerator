# TimeTableGenerator
Automatic Timetable generation using a genetic algorithm. Made with Flask and React.

### Hard constraints:
1. Each teacher should be able to teach only one section at a time
2. Subjects should have a required number of classes per week
3. Certain teachers can teach only certain subjects, for a given section 

### Soft constraints:
1. Minimize gaps between classes
2. Minimize variance in the number of classes handled on different days(the number of classes each day should be uniform throughout the week)

### Setup
    git clone https://github.com/waleedj99/TimeTableGen_FE.git
    cd TimeTableGen_FE/TimetableFE/time-table
    npm install
    npm run build
    cd ../../..
    python main.py
    
### Screenshots
<img src="https://github.com/waleedj99/TimeTableGenerator/blob/master/screenshots/ss1.png" alt="screenshot 1" width="450">
<img src="https://github.com/waleedj99/TimeTableGenerator/blob/master/screenshots/ss2.png" alt="screenshot 2" width="450">


