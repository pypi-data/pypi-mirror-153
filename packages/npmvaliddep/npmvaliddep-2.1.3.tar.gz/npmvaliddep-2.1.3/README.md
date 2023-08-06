<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">NPMVALIDDEP</h1>
  <p align="center">
    CLI tool made in python to check and update the npm package dependencies in github repositories
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/dyte-submissions/dyte-vit-2022-Akshat1903">View Demo</a>
    ·
    <a href="https://github.com/dyte-submissions/dyte-vit-2022-Akshat1903/issues">Report Bug</a>
    ·
    <a href="https://github.com/dyte-submissions/dyte-vit-2022-Akshat1903/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

NPMVALIDDEP is a cli tool made in python used to check the version of NPM packages in a github repository of NodeJs project. You can specify multiple packages to check and also specify if you want to raise a PR in case the packages are not up-to-date. It works for public as well as private repositories (provided that you are authorised to access the repository), in case you are the owner of the repository then instead of raising a PR it will directly commit to the repository main brach.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Below listed are the detailed steps to install the package with the prereqisites required.

### Prerequisites

You need to have following things installed: 
1. [Pip (Package Installer for python)](https://pypi.org/project/pip/)
2. [Git](https://git-scm.com/downloads)
3. [Node and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

### Installation

Create a python virtual environment and install the npmvaliddep package using pip [project_url](https://pypi.org/project/npmvaliddep/)
```sh
pip install npmvaliddep
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

In order to ensure that you can access the private repositories, you need to add your github username and [authentication token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) (Don't worry we store your token locally and never reveal it even to you :sunglasses:)

### To check your cofigured github username and password:
```sh
npmvaliddep --getgithubcreds
```

### To configure your cofigured github username and password:
```sh
npmvaliddep --setgithubcreds
```

### To check if the stored password matched your password:
```sh
npmvaliddep --matchgithubpass
```

### To perform dependency check of multiple github repositories and packages:
1. (Required) Create a csv file with the following headers and enter the rows accordingly.
![image](https://user-images.githubusercontent.com/54977399/171396466-a8a00438-fda5-41c5-916e-23fefbc16b8f.png)

2. (Required) Specify the path to the csv using --check flag
```sh
npmvaliddep --check '/home/user/checkrepos.csv'
```

3. (Required) Specify the dependencies you need to check using the --deps flag
```sh
npmvaliddep --check '/home/user/checkrepos.csv' --deps axios@0.23.0 cookie-parser@1.4.6
```

4. (Optional) By default the output csv will be generated in the user home directory but if you want to change that you can specify the path using --output flag
```sh
npmvaliddep --check '/home/user/checkrepos.csv' --deps axios@0.23.0 cookie-parser@1.4.6 --output '/home/user/Downloads/output.csv'
```
![image](https://user-images.githubusercontent.com/54977399/171396643-7d5ef471-cf3a-4fbe-8405-e9a99cc5ca9b.png)

5. (Optional) If you waant to generate a PR to update the dependencies then you can pass a --createpr flag
```sh
npmvaliddep --check '/home/user/checkrepos.csv' --deps axios@0.23.0 cookie-parser@1.4.6 --output '/home/user/Downloads/output.csv' --createpr
```
![image](https://user-images.githubusercontent.com/54977399/171396761-42f91003-5feb-42c3-beaf-e2bc48394a6b.png)
**Note -** In the above image you can notice that the last repository belongs to me i.e. the user of the CLI, in this case the tool will not create a PR but will directly commit the changes to the main branch of the repository. Also note that if a repository is private and the user is not authorised to access it then the tool will skip that repository.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Akshat Gupta - [@linkedin_handle](https://www.linkedin.com/in/akshat-g-1903/) - [Mail me](mailto:akshatgupta1903@gmail.com)

Project Link: [https://github.com/dyte-submissions/dyte-vit-2022-Akshat1903](https://github.com/dyte-submissions/dyte-vit-2022-Akshat1903)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
- I would like to thank dyte recruitment team to give this challenging task and focusing on the other half of the students who don't only crave for DSA :wink:

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/akshat-g-1903
[product-screenshot]: images/screenshot.png
