FROM python:3.9
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

# COPY requirements.txt .
RUN poetry export -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt

COPY sfat/ ./sfat/
COPY app.py app.py ./

# WORKDIR sfat
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
