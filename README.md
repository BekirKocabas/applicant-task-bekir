# itdesign GmbH - Cloud Operations Applicant Task

Thank you for applying for a position on our team. As Cloud Operations Engineers, one of our technical basics is to make code that we have written ourselves or by others, run in a standardized environment and ensure its operation. This assignment should give you a small picture of what we deal with on a daily basis and show us a small sample of your skills. It is important for us that you do the task yourself.

## Information

What do we expect?

 1. Actual working programs and containers
 1. Show us your best side

Stuck or need more information? Don't hesitate to contact us.

Once you are done, please notify us, so we can check your work. We will get in touch with you as soon as possible.

## Part 1 - Python

We desperately need two Python servers that have nothing better to do than play number-guessing with each other. The first server serves as the "player" and the second as the "game master". Their common language is HTTP requests. We, as outsiders, can start a new round and watch how the two play with each other. The numbers are between 1 and 1000, but should be configurable.

Keep in mind, that these two servers are supposed to run in a Cloud-Environment.

### Player

The Player is a standalone python server that tries to find the number as fast as possible and plays with the Game Master without any interaction. We are just outsiders watching them play.

| Endpoint  | Response |
|---|---|
| /health | 200 - "healthy" |
| /hostname | 200 - \<server hostname\>  |
| /play | 200 - Result and history of the game |

If you need additional endpoints, feel free to implement them.

### Game Master

This is where you can get creative. We need a game master server, that is capable of playing multiple game sessions at once. The game master is picks a random number inside the range and answers with
- "higher" if the guessed number is too low
- "lower" if the guessed number is too high
- "won" if this is the number

## Part 2 - Docker
Dockerize your application and provide us with informations on how to build and run your docker images.
You can attach your documentation to this readme.

--I wrote dockerfiles for both servers and in docker-compose.yml I specified the relative path of the dockerfiles with "build context dockerfile" and ran the build process this way. I could have written the build process for both dockerfiles with "docker build -t bekirkocabas/player-server:latest . " and "docker build -t bekirkocabas/master-server:latest ." and push it to the dockerhub repository, then I could have written bekirkocabas/player_server:latest and bekirkocabas/master_server:latest image in the image section of docker-compose.yml, but in this project I chose the first option.


## Part 3 - Docker-Compose
--Provide us with a docker-compose file for your game. It should contain healthchecks and any configuration your game requires.
After writing the docker-compose.yml file, I wrote "docker-compose up" in the guess_player_server-userdata.sh file that I used to start my Amazon Linux 2023 EC2 instance. You can see this guess_player_server.userdata.sh on the Githubrepo under terraform-files_userdata_for_Amazon_Linux_2023 folder