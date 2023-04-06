# docker-lviv-2022

This repository contains the code for the workshop at Lviv AI Summer School 2022 by [NeuroForge](https://neuroforge.de/)

# Prerequisites

## Optional: On your local machine: Install VSCode for remote development

Install VSCode:

https://code.visualstudio.com/

Install the SSH Remote Development plugin:

https://code.visualstudio.com/docs/remote/ssh

## On your remote machine: Install Docker

https://docs.docker.com/engine/install/ubuntu/

# Notes

First, check if Python is installed on your system:

```bash
python3 --version
```

If you don't have Python installed, you can install it with this command on Ubuntu:

```
apt-get update && apt-get install -y python3.8-venv
```

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
git clone https://github.com/s4ke/docker-lviv-2022
cd docker-lviv-2022/application
bash create_venv.sh
source venv/bin/activate
pip3 install -r requirements.txt --no-cache-dir
```

## Build the AI

In the file `application/ai/model.py`, build an AI using the keras library.
You can adapt this file to your liking, but the existing model works okay.

See https://keras.io/api/layers/ for more documentation on the available layers.

You can go to the next step to see how we can train the AI for evaluation of whether
we are doing a good job.

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

Note: if you get a permission denied error during this workshop, check if the command works with a `sudo` in front of it.
This is due to Docker by default only working for the root user for security reasons. The only alternative would
be creating a new user group `docker` on the machine and adding your user to that group. For the sake
of brevity in this workshop, using `sudo` is fine, though.

## Install Docker on your machine

The following requires Docker to be installed on your machine.
If not done already, follow the tutorial at https://docs.docker.com/engine/install/ubuntu/

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

# Docker Swarm

This is not a full Docker Swarm tutorial. This is just here to give an idea
of how to scale out Docker services. Real production clusters need an ingress (e.g. Traefik),
possibly encrypted ingress networks, and are usually not managed via
cli, but instead via stack files.

## Create the Cluster

To scale out our deployment of the AI service, we use Docker Swarm - a built-in
clustering technology in Docker.

First, we initialize our single node swarm:

```bash
docker swarm init
```

This will initialize a docker swarm. In production you would now add more nodes to the cluster,
but for the sake of this tutorial, we don't need more nodes. The commands will all be the same.

## Create a service

We can now create our AI service in the Docker swarm.

```bash
docker service create --name myai_service --publish 4000:4000 ghcr.io/s4ke/docker-lviv-2022:main
```

By default, this creates a service with 1 replica. We can again test it via another shell in the `test` directory:

```bash
bash run_request.sh img/8.bmp
```

To see the logs, we can run:

```bash
docker service logs myai_service
```

If for whatever reason the single application can not handle all the requests, we could scale out our application by running:

```bash
docker service scale myai_service=3
```

This will create two extra replicas of our service. Load will be shared among all replicas via Docker Swarm's built in
load balancing. In a multinode environment Docker Swarm would also try to spread the containers across all nodes of the cluster.
Because of Docker Swarms routing, it does not even matter which Node things are running on. Any physical node
is able to serve requests on port 4000, even if no replica ended up on the node.


Note: In production, we would not use a locally built image. For this,
we would `docker push` the image after building. This is however not part of this
tutorial. As we are running the service creation on the same node we built the image on,
the service will be created successfully nonetheless.

## Cleanup

Once finished, we can force leave the swarm with (This will destroy your single node swarm):

```bash
docker swarm leave -f
```

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
5. How does load balancing work in Docker Swarm?

# Additional resources

Youtube Video: [Learn Docker in 7 Easy Steps - Full Beginner's Tutorial](https://www.youtube.com/watch?v=gAkwW2tuIqE)
