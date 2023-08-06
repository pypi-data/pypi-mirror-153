FROM python:3.9-slim

ENV APP_NAME mcl_python_package_template
ENV WD /opt/${APP_NAME}

# Setup working directory
RUN mkdir -p ${WD}
WORKDIR ${WD}

# RUN pip install --user pipenv
RUN pip install pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --deploy --clear


# Copy app files
COPY ./${APP_NAME}/ ${WD}/${APP_NAME}/
COPY tests ./tests
COPY entrypoint.bash\
    *.yaml\
    *.json\
    ./


ENV PORT 3000
EXPOSE $PORT

ENTRYPOINT pipenv run ./entrypoint.bash
