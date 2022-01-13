# Client
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/nus-ncl/Client">
    <img src="images/logo.jpg" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Client</h3>

  <p align="center">
    An awesome tool to make your access to your machines on NCL easily!
    <br />
    <a href="https://github.com/nus-ncl/Client"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nus-ncl/Client">View Demo</a>
    ·
    <a href="https://github.com/nus-ncl/Client/issues">Report Bug</a>
    ·
    <a href="https://github.com/nus-ncl/Client/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Issues](#Issues)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)
* [Contributors](#Contributors)



<!-- ABOUT THE PROJECT -->
## About The Project

Configurating SSH tunnel and rdesktop to the remote machine(on NCL) is a kind of boring and tedious process. That's what this tool 'Client' aims to solve.
It provides a clean GUI to automate the procedure of SSH tunneling, port binding & unbinding and rdesktop to make your life easier :)






<!-- GETTING STARTED -->
## Getting Started

### Select Platform
* [MacOS](#get-started-from-macos)
* [Windows](#get-started-from-windows)
* [Ubuntu](#get-started-from-ubuntu)

### Get started from MacOS
#### [Step1: git clone/download this repository]

* git:
  ```sh
  $ git clone https://github.com/nus-ncl/Client.git
  ```
* Download from the url below:

  [Client-master](https://github.com/nus-ncl/Client/archive/refs/heads/master.zip)


#### [Step2: install python3.9]
* [python3.9](https://www.python.org/downloads/release/python-399/)
  ```shell
  # check in the terminal if python3.9 installed successfully
  $ python3.9 -V
  Python 3.9.9
  ```

#### [Step3: create a python virtual environment]
  ```shell
  # Enter main folder
  $ cd Client # or 'cd Client-master'
  $ python3.9 -m pip install virtualenv 
  $ python3.9 -m virtualenv venv
  ```

#### [Step4: enter the python virtual environment & install dependencies]
  ```shell
  $ source venv/bin/activate
  (venv)$ pip install -r requirements.txt
  ```
#### [Step5: run it]
  ```shell
  (venv)$ python main.py
  ```

### Get started from Windows
#### [Step1: git clone/download this repository]

* git:
  ```sh
  $ git clone https://github.com/nus-ncl/Client.git
  ```
* Download from the url below:

  [Client-master](https://github.com/nus-ncl/Client/archive/refs/heads/master.zip)


#### [Step2: install python3.9 & vncviewer]
* [python3.9](https://www.python.org/downloads/release/python-399/)
  ```shell
  # check in the terminal if python3.9 installed successfully
  $ python3.9 -V
  Python 3.9.9
  ```
* [vncviewer](https://www.realvnc.com/en/connect/download/viewer/windows/)

#### [Step3: configure vncviewer]
* search installed vncviewer file location
![search_vncviewer]
###
* right-click > properties > copy 'Target'
![find_target]
###
* add an entry to the Environment Variable 'Path'
![search_env]
![find_env_path]
###
* in my case, 'Target' is 'C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe', so add 'C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe' to Path
![add_path]
###
* now can invoke it by 'vncviewer' in Command Prompt
```shell
$ vncviewer
```
![check_vncviewer]

#### [Step4: create a python virtual environment]
  ```shell
  # Enter main folder
  $ cd Client # or 'cd Client-master'
  $ python3.9 -m pip install virtualenv 
  $ python3.9 -m virtualenv venv
  ```

#### [Step5: enter the python virtual environment & install dependencies]
  ```shell
  $ venv\Scripts\activate
  (venv)$ pip install -r requirements.txt
  ```
#### [Step6: run it]
  ```shell
  (venv)$ python main.py
  ```

### Get started from Ubuntu
#### [Step1: git clone/download this repository]

* git:
  ```sh
  $ git clone https://github.com/nus-ncl/Client.git
  ```
* Download from the url below:

  [Client-master](https://github.com/nus-ncl/Client/archive/refs/heads/master.zip)


#### [Step2: install python3.9 & vncviewer]
* [python3.9](https://www.python.org/downloads/release/python-399/)
  ```shell
  # check in the terminal if python3.9 installed successfully
  $ python3.9 -V
  Python 3.9.9
  ```
* [vncviewer](https://www.realvnc.com/en/connect/download/viewer/linux/)
  
#### [Step3: create a python virtual environment]
  ```shell
  # Enter main folder
  $ cd Client # or 'cd Client-master'
  $ python3.9 -m pip install virtualenv 
  $ python3.9 -m virtualenv venv
  ```

#### [Step4: enter the python virtual environment & install dependencies]
  ```shell
  $ source venv/bin/activate
  (venv)$ pip install -r requirements.txt
  ```
#### [Step5: run it]
  ```shell
  (venv)$ python main.py
  ```

<!-- USAGE EXAMPLES -->
## Usage

![mainwindow]

1. Input your NCL Testbed Username into ``Username`` blank.

   *caution*
      - If you use Username `nologin` that we provide, no more further operations 
      - If you use your own NCL Testbed Username(e.g. `joedoe`)
        - put your private key to the `private_key` folder and name it as `<Username>.pem`(e.g. `joedoe.pem`)
        - (not applicable for Windows) change the file mode of the private key to `400` by `chmod 400 <Username>.pem`
   
2. Click the ``Choose XML ...`` button and choose your client xml file.
3. Click 'Confirm' button to show your remote machines on NCL Testbed
4. Select your local platform
5. Select your method to access to the machine
   - 'Console': access with GUI
   - 'SSH': access without GUI via web browser
6. Double-click the machine entry to access it
7. Click 'Tutorial' button to show a window of the relavant documentation
8. Click 'Reset' button if 'Console' accessing method ALWAYS failed

   *caution*
   - single-click to select the machine you want to reset before clicking 'Reset'
10. 'Nothing' Button is a future function button, to be continued...




<!-- ISSUES -->
## Issues

See the [open issues](https://github.com/nus-ncl/Client/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Huang Kang - [dcshka@nus.edu.sg]

Project Link: [https://github.com/nus-ncl/Client](https://github.com/nus-ncl/Client)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [NCL](https://ncl.sg/)

<!--  CONTRIBUTORS -->
## Contributors
* Huang Kang

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-1-brightgreen
[contributors-url]: https://github.com/nus-ncl/Client/graphs/contributors
[forks-shield]: https://img.shields.io/badge/forks-0-blue
[forks-url]: https://github.com/nus-ncl/Client/network/members
[stars-shield]: https://img.shields.io/badge/stars-0-orange
[stars-url]: https://github.com/nus-ncl/Client/stargazers
[issues-shield]: https://img.shields.io/badge/issues-0-red
[issues-url]: https://github.com/nus-ncl/Client/issues
[license-shield]: https://img.shields.io/badge/license-MIT-blueviolet
[license-url]: https://github.com/nus-ncl/Client/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/
[mainwindow]: images/mainwindow.png
[add_path]: images/add_path.jpg
[check_vncviewer]: images/check_vncviewer.jpg
[find_env_path]: images/find_env_path.jpg
[find_target]: images/find_target.jpg
[search_env]: images/search_env.jpg
[search_vncviewer]: images/search_vncviewer.jpg

