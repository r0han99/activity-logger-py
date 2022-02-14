# Activity-Logger.***py***

*Basic Activity Logging Script*

---

## Briefing

_**Actlogger** command-line tool that can be used to establish records of your sequential day-to-day works in a log. This tool integrates well with projects like 50 and 100 days of code. Users can keep track of their work at the end of the day into this log to keep track of everything they learn over the course._

---

## Installation V1.0

step-1: ``requirements``

```bash
$ pip install -r requirements.txt
```

step-2: ``clone repo``

```bash
$ git clone https://github.com/r0han99/activity-logger-py.git
```

step-3: ``setup.sh``

```bash
$ cd into-repo
$ chmod +x setup.sh
$ ./setup.sh
```

~ _Execlusive only to MacOS, Linux based OS_

---

## Usage

- **$** ``Establish``

  ```bash
  $ actlogger --init
  ```
  <img width="616" alt="image-20220214112615681" src="https://user-images.githubusercontent.com/45916202/153812852-1d1a5786-5369-4a62-8f2d-9202fa015c64.png">


* **$** ``Functionalities``

  ```bash
  $ actlogger --tasks constructors-classes-objects
  ```
  <img width="528" alt="image-20220214112959474" src="https://user-images.githubusercontent.com/45916202/153813027-ec9fe36e-186f-44f8-916a-d55906cb7f83.png">



   ```
  $ actlogger --tasks constructors-classes-objects --info y
   ```

  <img width="1225" alt="image-20220214113454224" src="https://user-images.githubusercontent.com/45916202/153813139-9eb26b44-4333-40c3-91c3-74e0a82b3f7b.png">


* $ ``backup``

  ```bash
  $ actlogger --backup partial 
  ```

* **$** ``summary``

  ```bash
  $ actlogger --summary
  ```

  <img width="329" alt="image-20220214121803942" src="https://user-images.githubusercontent.com/45916202/153814416-397e849b-6f45-4900-a77a-bb60a31876cc.png">

 

---

#### Prospective Features

* ``--restore`` : Functionality to take the latest backedup Archive and Restore the logging setup, if the assets are deleted accidentally.
* ``--amend`` : Functionality to edit a particular ;og line.
* ``--visualise`` | ``--stats`` : Functionality to visualise statistics of logs. 
  * Topic or Concepts Mentioned more number of times.
  * Average Time Taken?
* ``--synch`` : Functionality to synch inconsistent records.
* A pip package? -- *Only time will tell.*

---

