# Final Project
![Web App CI/CD](https://github.com/software-students-fall2024/5-final-sg/actions/workflows/build.yml/badge.svg)

# Description

My Calendar helps you keep track of your events on a calendar! You can add, delete, and edit events on your calendar by clicking on the event on the calendar. Optionally, you can also drag the events around on the calendar to update the time of the event.

# Links to Container Images

[Web App](https://hub.docker.com/repository/docker/lucia0313/5-final-sg-app/general)
[Database](https://hub.docker.com/repository/docker/lucia0313/mongo/general)

# Team Members

[Lucia Song](https://github.com/lys7942) <br>
[Chelsea Hodgson](https://github.com/Chelsea-Hodgson) <br>
[Yeshni Savadatti](https://github.com/yeshnii) <br>
[Alan Zhao](https://github.com/Alan3562) <br>

# How to Run the Application

1. Make sure to install, run, and login to Docker Destop on your local machine. You can do so with this [link](https://www.docker.com/products/docker-desktop/). <br>

2. Make sure to have docker-compose installed. <br>

3. Clone the repository by using the command: <br>
```git clone git@github.com:software-students-fall2024/5-final-sg.git``` <br>

4. Navigate into the project root folder.

5. To run the app, use the command: <br>
```docker-compose up --build``` <br>

Or run in detatched mode: <br>
```docker-compose up -d``` <br>

6. To view the app, go to http://localhost:3000/. <br>

7. To shut down the containers, run the command: <br>
```docker-compose down``` <br>

# How to Run Tests the Web Application
1. Navigate into root directory of the app.

2. Set up a virtual environment, by using the commands:
```pip3 install pipenv OR pip install pipenv``` <br>

3. Activate the virtual environment: <br>
```pipenv shell``` <br>

4. To run tests, use the command:
```pytest```

# How to Contribute to the Project
We welcome contributions! Here’s how you can help:
1. **Fork the Repository**: Start by forking the repository and cloning your fork to your local machine.
2. **Create and Set up Virtual Environment**: Set up a virtual environment with pipenv, using: <br>
```pip install pipenv OR pip3 install pipenv``` <br>
and then: <br>
```pipenv shell``` <br>
3. **Install Dependencies**: Make sure you have the necessary dependencies installed if pipenv was not used: <br>
```pip install -r requirements.txt OR pip3 install -r requirements.txt``` <br>
4. **Create a New Branch**: Create a branch for your feature or bug fix.
5. **Make Changes and Write Tests**: Make your changes, ensuring that you add or update tests as needed in the tests directory. To run tests, use the command: <br>
```pytest``` <br>
6. **Commit and Push Your Changes**: After finishing your work on local machine, commit and push your changes to git.
7. **Create a Pull Request**: Go to the original repository and create a pull request for your changes.

Please ensure your codes come with meaningful commit messages and follow the PEP 8 standard, which can be found in detail [here](https://peps.python.org/pep-0008/).
