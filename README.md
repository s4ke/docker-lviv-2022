# docker-lviv-2022

This repository contains the code for the workshop at Lviv AI Summer School 2022.

# A REST API for an AI

The following makes havy use of utility bash scripts. This is good practice
when developing large applications as we don't have to remember commands by heart.
For the sake of this workshop, whenever there is a `*.sh` file mentioned
in a code snippet, study the contents of it to familiarize yourself with the
actual commands that run under the hood.

## Set up the development environment (outside of docker)

On your command line, switch to the application directory.
Next, we have to setup our development environment. For this we run the following:

```bash
bash create_venv.sh
source venv/bin/activate
pip3 install -r requirements.txt
```

## Train the AI

In order for our API to have proper weights, we have to first generate the weights.
For the purpose of this workshop, we already have a MLP defined which we are going to train
for 30 epochs which should be enough for the MNIST case we are solving.

To train the AI, we simply run:

```
source venv/bin/activate
python3 train_ai.py
```

## Test the API with the development server

Inside your application folder, we can start the Flask Dev Server with:

```
source venv/bin/activate
bash runDev.sh
```

Then, on another shell, switch to the test directory, and run a sample request against the AI:

```
bash run_request.sh img/8.bmp
```

This should print something like this on your shell:

```
(venv) martinb@ubuntu:~/github/docker-lviv-2022/test$ bash run_request.sh img/8.bmp
+ curl -F image=@img/8.bmp localhost:4000/classify
{"class":"8"}
```

This means that you have a flask app successfully running in dev mode with all weights properly there.
We can now stop the Test server by hitting `CTRL-C` on our keyboard.

## Test the API with the gunicorn production server

As we can not use the flask dev server in production, we also have an already prepared gunicorn based run script.
To start this instead of the dev server, we simply run:

```
source venv/bin/activate
bash run.sh
```

Then, on another shell, we can run the test request in side the `test` directory again:

```
bash run_request.sh img/8.bmp
```

This should again something like this on your shell:

```
(venv) martinb@ubuntu:~/github/docker-lviv-2022/test$ bash run_request.sh img/8.bmp
+ curl -F image=@img/8.bmp localhost:4000/classify
{"class":"8"}
```

# Docker

## Install Docker on your machine

The following requires Docker to be installed on your machine.
If not done already, follow the tutorial at https://docs.docker.com/engine/install/ubuntu/

## Taking Docker for a spin

## Build the docker image

As we want a self contained docker image for our AI based REST service, we have to
build a docker image. To do so, inside the `application` folder we run:

```
bash build.sh
```

This will run the appropriate docker cli command to build a docker image with our
AI.

## Test the docker image

Inside the `test` folder, we have a script `start_test_docker.sh`. We run it with:

```bash
bash start_test_docker.sh
```

Then, on another shell, we can run the test request in side the `test` directory again:

```
bash run_request.sh img/8.bmp
```

This should again something like this on your shell:

```
(venv) martinb@ubuntu:~/github/docker-lviv-2022/test$ bash run_request.sh img/8.bmp
+ curl -F image=@img/8.bmp localhost:4000/classify
{"class":"8"}
```

When you are done testing, don't forget to stop the docker container by hitting `CTRL-C`.

# Self-Study Questions

1. What is the purpose of the Flask DEV Server?
2. What is the purpose of gunicorn in this application?
3. What is the purpose of .dockerignore?

# Further questions

The following questions are for advanced learners. To answer them, you must familiarize yourself
with docker concepts like volumes, image layer caching in Docker, ...

1. How could we replace the weights of the application in production without rebuilding the whole container?
2. Why do we `COPY` the requirements.txt before the rest of the application?
3. How could we remove the sklearn dependency in production that we only need for training the AI?
4. How could we use docker even during development? (Hint: development containers, docker-compose)

# Additional resources

Youtube Video: [Learn Docker in 7 Easy Steps - Full Beginner's Tutorial](https://www.youtube.com/watch?v=gAkwW2tuIqE)