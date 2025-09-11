FROM python:3.11

LABEL name="project-template"
LABEL version="0.1.0"
LABEL description="This is my project template."

WORKDIR /app

ADD . ./

# CMD ["python"]