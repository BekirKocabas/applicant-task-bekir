terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
  // access_key = ""
  //  secret_key = ""
  //  If you have entered your credentials in AWS CLI before, you do not need to use these arguments.
  // you can enter your credentials by typing "aws configure" in your terminal. or you can cancel the comment line above and enter your access key and secret key 
}

resource "aws_vpc" "guess_play_vpc" {
  cidr_block = "172.16.0.0/16"

  tags = {
    Name = "GuessPlayVPC" # The name of vpc
  }
}


resource "aws_internet_gateway" "guess_play_IGW" {
  vpc_id = aws_vpc.guess_play_vpc.id

  tags = {
    Name = "guess_play_IGW"
  }
}

resource "aws_subnet" "public1a" {
  vpc_id                  = aws_vpc.guess_play_vpc.id
  cidr_block              = "172.16.10.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "guessplayvpc-public-subnet-1A"
  }
}

resource "aws_route_table" "guess_play_public_RT" {
  vpc_id = aws_vpc.guess_play_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.guess_play_IGW.id # İnternet Gateway connection
  }

  tags = {
    Name = "guess_play_vpc-public-RT"
  }
}

resource "aws_route_table_association" "guess_play_RTA" {
  subnet_id      = aws_subnet.public1a.id
  route_table_id = aws_route_table.guess_play_public_RT.id
}

data "aws_ami" "amzn-linux-2023-ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_instance" "guess_play_server" {
  ami                    = data.aws_ami.amzn-linux-2023-ami.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public1a.id
  key_name               = var.mykey
  vpc_security_group_ids = [aws_security_group.guess_play-server-sg.id]
  user_data              = filebase64("guess_play_server-userdata.sh")


  tags = {
    Name = "guess-play-server"
  }
}

resource "aws_security_group" "guess_play-server-sg" {
  vpc_id = aws_vpc.guess_play_vpc.id
  name   = "guess_play_server_sec_gr"
  tags = {
    Name = "guess_play_server_sec_gr"
  }
  dynamic "ingress" {
    for_each = var.guess-play-server-ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

}

output "PlayerServerHealthControl" {
  value = "Player Server health control: http://${aws_instance.guess_play_server.public_ip}:5000/health"
}

output "PlayerServerHostname" {
  value = "Player Server hostname : http://${aws_instance.guess_play_server.public_ip}:5000/hostname"
}

output "PlayerServerPlayGame" {
  value = "Click to watch the #1 player play and refresh the page to see his next predictions. To watch the other players play, change the player id at the end. http://${aws_instance.guess_play_server.public_ip}:5000/play/1"
}
output "ResettheGame" {
  value = "To reset the game and new target number. http://${aws_instance.guess_play_server.public_ip}:5000/reset_play/1"
}
output "GameMasterServerGameResult" {
  value = "Click to see the #1 player's game result. To see the game result of the other players, change the player id at the end. http://${aws_instance.guess_play_server.public_ip}:5001/game_result/1"
}