FROM ubuntu
SHELL ["/bin/bash", "-c"]
ENV NVM_DIR /usr/local/.nvm
ENV NODE_VERSION v18.16
RUN mkdir $NVM_DIR
RUN cat /etc/resolv.conf
RUN apt-get update && apt-get -y install curl
RUN curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
ENV NODE_PATH $NVM_DIR/$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN echo "source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default" | bash
WORKDIR /app
COPY package*.json ./
RUN source $NVM_DIR/nvm.sh && npm install
COPY . .
CMD source $NVM_DIR/nvm.sh && node_modules/.bin/ng serve --host 0.0.0.0