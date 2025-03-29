FROM ubuntu:latest
LABEL authors="zack"

ENTRYPOINT ["top", "-b"]