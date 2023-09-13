variable "mykey" {
  default = ""
}

variable "ami" {
  description = "amazon linux 2023 ami"
  default     = "ami-0889a44b331db0194"
}

variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "guess-play-server-ports" {
  type        = list(number)
  description = "guess-play-server-sec-gr-inbound-rules"
  default     = [22, 80, 5000, 5001]
}



