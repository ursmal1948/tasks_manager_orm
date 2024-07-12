FROM python:3.12

# Means Python wont try to write .pyc files which we also do not desire
# nasza apliakcja w wyniku budowania, kompilowania ma pewne pliki posrednie, ktore przechowuja pewna posac
# bytecodowa, plii ktore sa potrzebne w wyniku budowania aplikacji python. Te pliki nie sa nam potrzebne
# szcegolnie w kontenrze.


# When you run a single python process in the container, which does not spawn other python
# processes itself during its lifetime, then there is no "risk" in doing that.

# Storing byte code on disk is used to compile python into byte code just upon the first invocation of
# a program and its dependent libraries to save that step upon the following invocations. In a container
# the process runs just once, therefore setting this option makes sense.
ENV PYTHONDONTWRITEBYTECODE 1

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to terminal
# (e.g. your container log) without being first buffered and that you can see the output of your
# application (e.g. django logs) in real time.

# PYTHON BUFFERED. Mowi o tym ze od razu wszystko co wyypluwa twoja aplikacja pythonowa bylo wypluwane na
# terminal kontnera. Dzieki czemu bedziemy mogli widziec wszystkie logi tutaj na localhoscie.

# This also ensures that no partial output is held in a buffer somewhere and never written in case
# the python application crashes.
ENV PYTHONUNBUFERED 1

WORKDIR /webapp


COPY Pipfile Pipfile.lock /webapp/

# Pipenv will look for a virtual environment in which to install any package, but since we’re within Docker now,
# technically there isn’t any virtual environment. In a way, the Docker container is our virtual environment and more.
# So we must use the --system flag to ensure our packages are available throughout all of Docker for us.

# pipenv install --system will install the contents of an existing Pipfile into your global pip environment.
# Using the --system option, it won't allow you to specify a specific package.


RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY . /webapp/
COPY .env /webapp/
