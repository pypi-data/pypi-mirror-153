[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7950853&assignment_repo_type=AssignmentRepo)
<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/dyte-submissions/dyte-vit-2022-aayush1607">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Version Manager</h3>

  <p align="center">
    A simple lightweight cli tool that checks and updates dependency versions on all your node js github repos.
    <br />
  </p>
</div>

### Built With

* [Python](https://www.python.org/)
* [Github API](https://docs.github.com/en/rest)

<p align="right">(<a href="#top">back to top</a>)</p>

## Setup:
#### Step-1 : Clone this repository and move to dist directory (recommended) or download exe file from [/dist/version_manager.exe](https://github.com/dyte-submissions/dyte-vit-2022-aayush1607/blob/main/dist/version_manager.exe)
```
            git clone https://github.com/dyte-submissions/dyte-vit-2022-aayush1607.git
            cd dyte-vit-2022-aayush1607/dist
```
#### STEP-2 : Start using the tool
  ###### Example 1: To check that all repos in repo.csv file has axios >= 0.23.0
```
            version_manager -i repo.csv axios@0.23.0
```
  ###### Example output 1:
  <img src="images/output1.jpg" alt="output of example 1">
  Output also gets saved in output.csv in current directory.

  ###### Example 2: To check that all repos in repo.csv file has axios >= 0.23.0 and if not satistfied update and create pull request
```
            version_manager -u -i repo.csv axios@0.23.0
```
  ###### Example output 2:
  <img src="images/output2.jpg" alt="output of example 1">
  Output also gets saved in output.csv in current directory.

That's all for the tutorial.

In case you 
<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

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
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
