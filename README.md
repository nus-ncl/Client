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
  <a href="https://github.com/hkwany/Client">
    <img src="images/logo.jpg" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Client</h3>

  <p align="center">
    An awesome tool to make your access to your machines on NCL easily!
    <br />
    <a href="https://github.com/hkwany/Client"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hkwany/Client">View Demo</a>
    ·
    <a href="https://github.com/hkwany/Client/issues">Report Bug</a>
    ·
    <a href="https://github.com/hkwany/Client/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Running Platform](#Running-Platform)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Run](#Run)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)
* [Contributors](#Contributors)



<!-- ABOUT THE PROJECT -->
## About The Project

Configurating SSH tunnel and rdesktop to the remote machine(on NCL) is a kind of boring and tedious process. That's what this tool 'Client' aims to solve.
It provides a clean GUI to automate the procedure of SSH tunneling, port binding & unbinding and rdesktop to make your life easier :)


### Running Platform
* [Ubuntu](https://ubuntu.com/)




<!-- GETTING STARTED -->
## Getting Started

This is an instruction of how you to install prerequisites and run the Client tool locally successfully.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* qt5
```sh
sudo apt-get install qt5-default
```

* python3 & pip3
```sh
sudo apt-get install python3 python3-pip
```

* PySide2
```sh
# 'requirements.txt' is at root directory of this repository 
pip3 install -r requirements.txt
```

* rdesktop
```sh
sudo apt-get install rdesktop
```

### Run

1. Clone the repo
```sh
git clone git@github.com:hkwany/Client.git
```
2. Require your client.xml file of your remote machine.
```sh
# client.xml file is generated from Conductor #
# But I have provided a template client.xml in this repo which you can try #
```
3. Run
```sh
python3 main.py
```


<!-- USAGE EXAMPLES -->
## Usage

[![Product Name Screen Shot][product-screenshot]](https://example.com)  

1. Input your NCL username into ``user`` blank.
2. Select your client.xml file by clicking the ```xml``` button.
3. Double-click the entry listed in the UI, go back to the command line and then input your NCL password.
4. The Rdesktop GUI window has come out!!!
5. For quitting, just close the Rdesktop GUI window and the port will be unbinded automatically.(<font color=Blue>_We also print binded port in command line, so you can unbind the process binded to that port by using 'kill' manually in case_</font>)

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/hkwany/Client/issues) for a list of proposed features (and known issues).



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

Project Link: [https://github.com/hkwany/Client](https://github.com/hkwany/Client)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [NCL](https://ncl.sg/)

<!--  CONTRIBUTORS -->
## Contributors
* Huang Kang

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-1-brightgreen
[contributors-url]: https://github.com/hkwany/Client/graphs/contributors
[forks-shield]: https://img.shields.io/badge/forks-0-blue
[forks-url]: https://github.com/hkwany/Client/network/members
[stars-shield]: https://img.shields.io/badge/stars-0-orange
[stars-url]: https://github.com/hkwany/Client/stargazers
[issues-shield]: https://img.shields.io/badge/issues-0-red
[issues-url]: https://github.com/hkwany/Client/issues
[license-shield]: https://img.shields.io/badge/license-MIT-blueviolet
[license-url]: https://github.com/hkwany/Client/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/
[product-screenshot]: images/client-screenshot.png

