#! /bin/bash

#If you don't change the FOLDER variable below, you will be pulling the files downloaded to EC2 in userdata from my public repo. 
#I pushed the same python, dockerfile and docker-compose.yml files to your repo. 
#If you replace BekirKocabas username in the FOLDER variable below with your own github username, 
#you will pull your own github files from your repo.

dnf update -y
hostnamectl set-hostname guess_play_server
dnf install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
curl -SL https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
mkdir -p /home/ec2-user/applicant-task-bekir/
mkdir -p /home/ec2-user/applicant-task-bekir/player/
mkdir -p /home/ec2-user/applicant-task-bekir/master/
dnf install git -y
cd /home/ec2-user
FOLDER="https://raw.githubusercontent.com/BekirKocabas/applicant-task-bekir/main/"
curl -s --create-dirs -o "/home/ec2-user/applicant-task-bekir/player/player.py" -L "$FOLDER"player/player.py
curl -s --create-dirs -o "/home/ec2-user/applicant-task-bekir/player/Dockerfile" -L "$FOLDER"player/Dockerfile
curl -s --create-dirs -o "/home/ec2-user/applicant-task-bekir/master/master.py" -L "$FOLDER"master/master.py
curl -s --create-dirs -o "/home/ec2-user/applicant-task-bekir/master/Dockerfile" -L "$FOLDER"master/Dockerfile
curl -s --create-dirs -o "/home/ec2-user/applicant-task-bekir/docker-compose.yml" -L "$FOLDER"docker-compose.yml
cd /home/ec2-user/applicant-task-bekir/
docker-compose up -d