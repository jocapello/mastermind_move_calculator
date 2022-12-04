# project-docker
Docker file for developing the course project.

1. First, download Docker https://www.docker.com/get-started

2. Copy the Dockerfile in this directory to your project repo, and then go there on the command line.

3. We first have to build the course image. To do so use the command:
`docker build . -t cisc204`

4. Now that we have the image we can run the image as a container by using the command: `docker run -t -i -v C:\Users\brand\OneDrive\Documents\Code\204\mastermind_move_calculator:/PROJECT cisc204 /bin/bash`

    /modelProject can be replaced with the path of whatever folder you want to link to the container

    /PROJECT is the folder in the container that will be tied to your local directory

5. From there the two folders should be connected, everything you do in one automatically updates in the other. For the project you will write the code in your local directory and then run it through the docker command line. A quick test to see if they're working is to create a file in the folder on your computer then use the terminal to see if it also shows up in the docker container.
