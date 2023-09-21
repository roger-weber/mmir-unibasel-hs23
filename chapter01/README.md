# Chapter 01: Introduction

Here are a few links to get us ready for the course. 

## Slides

- [Introduction](https://dmi.unibas.ch/fileadmin/user_upload/dmi/Studium/Computer_Science/Vorlesungen_HS23/Multimedia_Retrieval/01_Introduction.pdf)
- Notes (tbd)

## Helpful software

1. **Installers**
   - [Chocolatey for Windows](https://chocolatey.org/install)
     [Chocolatey package search](https://community.chocolatey.org/packages)
   - [brew for macOS](https://brew.sh/)
     [homebrew formuale](https://formulae.brew.sh/)

2. **Python**
    - **[Download Python](https://www.python.org/downloads/)**
      choco: ```choco install python```
      macOS: ```brew install python```
      Check the version:

      ```bash
        python --version
      ```
  
    - **Set a symlink** for ```python``` to ```python3``` (if it does not exist; or: always use python3 and pip3)

    - **Upgrade pip**

      ```bash
        python -m pip install --upgrade pip
      ```

    - **Best practice**: create a vritual python environment to prevent package version conflicts

      ```bash
        python -m venv .venv

        windows> .venv\Scripts\activate
        macOS> source .venv/bin/activate
      ```

      This also works with jupyter notebooks (select the .venv python kernel)
      Deactivate the environment with

      ```bash
        windows> deactivate
        macOS> deactivate
      ```

    - **Keep track of dependencies** with ```requirements.txt``` then use pip to install

      ```bash
        pip install -r requirements.txt
      ```

      Example for ```requirements.txt```:

      ```text
        ###### Requirements without Version Specifiers ######
        nose
        nose-cov
        beautifulsoup4

        ###### Requirements with Version Specifiers ######
        docopt == 0.6.1             # Version Matching. Must be version 0.6.1
        keyring >= 4.1.1            # Minimum version 4.1.1
        coverage != 3.5             # Version Exclusion. Anything except version 3.5
        Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
      ```

    - **[Finding packages (PyPI)](https://pypi.org/)**

3. **Jupyter notebooks**

    - Install Jupyter Notebook, and run from current folder (with *.ipynb files)

      ```bash
        pip install notebook
        jupyter notebook
      ```

    - Optional: install JupyterLab, and run from current folder (with *.ipynb files)

      ```bash
        pip install notebook
        jupyter notebook
      ```

    - Optional: install additional kernels for jupyter
        - [Ganymede](https://github.com/allen-ball/ganymede): JShell Kernel for notebooks
          download the jar `ganymede-nnn.jar`
          install the new kernel `java -jar ganymede-nnn.jar -i`
          restart jupyter notebook / VSCode
          open notebook and select ganymede kernel
          use `%%pom` to load 3rd party libraries

            ```pom
                %%pom
                dependencies:
                - org.apache.lucene:lucene-core:LATEST
                - org.apache.lucene:lucene-analyzers-common:LATEST
                - org.apache.lucene:lucene-queryparser:LATEST
            ```

        - [iRuby](https://github.com/sciruby/iruby#macos)

            ```bash
                gem install iruby
                iruby register --force
            ```

        - [more kernels for other languages](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels)

4. **IDE**

    - [VSCode](https://code.visualstudio.com/)
        Install the following extensions

        ```bash
            Python
            Pylance
            Jupyter
            Java Language Support
            Gradle for Java
            AWS Toolkit
        ```

        [Sign-up for Amazon CodeWhisperer (free)](https://docs.aws.amazon.com/codewhisperer/latest/userguide/whisper-setup-indv-devs.html)
        (this requires an AWS Builder ID; usage is for free for individual tier; no AWS account required)

    - [PyCharm](https://www.jetbrains.com/pycharm/)
        [Install Amazon CodeWhisperer](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/setup-toolkit.html)
        (this requires an AWS Builder ID; usage is for free for individual tier; no AWS account required)

## Documentation, tutorials, cheat sheets

- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
- [Python Documentation](https://docs.python.org/3/index.html)
- [Quickstart with Python](https://docs.python.org/3/tutorial/index.html)
- [Python Cheat Sheets](https://www.pythoncheatsheet.org/)

## Links

- [Web Site Course (Uni Basel)](https://dmi.unibas.ch/de/studium/computer-science-informatik/lehrangebot-hs23/lecture-multimedia-retrieval/)
- [Link to Adam (Students only)](https://adam.unibas.ch/goto_adam_crs_1547405.html)
