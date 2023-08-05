## Part 1 - Installing ds-framework and creating a new project {#quick_start1}

This quick start tutorial will guide you through the minimum steps you need to take to be up and running.

&nbsp;
### Step 1 - Installing the ds-framework
The first step is to install the dsframework package using the following command:

    pip install dsframework

&nbsp;
### Step 2 - Generating a new project

**This step is not required if you received a ready project.**

&nbsp;
####Prerequisite:
Before generating a new project, create a github repository under 
[https://git.zoominfo.com/dozi](https://git.zoominfo.com/dozi), name it for example <strong><my-new-project></strong>, 
and use this name to create the project.

&nbsp;
####Generate project:
Change directory to where you want to create your new project and use the following dsf-cli command to generate 
project, name it the same as the repo: **my-new-project**: 

    dsf-cli generate project my-new-project


<br />
This process generates a new project locally, stores it in **my-new-project** folder and pushes it to your newly 
created GitHub repository.

&nbsp;
### Step 3 - Install requirements
To install the requirements we will need first to create a **virtual environment** (venv).

There are two recommended ways to create a virtual environment, select one:
1. Create a new project.
2. Open existing project.

#### 1. Create new project:
- Open pycharm
- Create a new project
- Change the 'Location' to your newly created project folder **my-new-project**
- Click 'Create'
- Click 'Create from Existing Sources'

#### 2. Open existing project:
Open the newly created project in PyCharm and add an interpreter for python 3.8, it will add a venv folder: 

    PyCharm > Preferences > Project > Python Interpreter - then click on the configure button and select 'Add'

In python terminal make sure you see (venv) in the command prefix, if not then run activate using the following:

    source venv/bin/activate

#### Install requirements:
After venv is ready we can install the requirements using the following:

    pip install -r requirements_docker.txt

&nbsp;
####Additional steps
There are additional steps that needs to be done with DevOps to open an AWS/GCP service for your project, those steps 
are **not required** for you to start working. 

For the full information about generating your own project see the following 
confluence page [here - MLOps project template](https://discoverorg.atlassian.net/wiki/spaces/ZE/pages/20356565807/MLOps+project+template)




