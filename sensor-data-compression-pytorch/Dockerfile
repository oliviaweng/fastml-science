FROM pytorch/pytorch

#Install dependencies
RUN apt-get update && apt-get install -y git 
RUN apt-get update && \
    apt-get install -y \
    python-setuptools \
    python-dev 
RUN apt-get update && \
    apt-get install -y \
    vim tmux htop
RUN apt-get update && apt-get install -y gcc g++ 
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get update && apt-get install -y --no-install-recommends libopencv-dev libturbojpeg-dev
RUN cp -f /usr/lib/x86_64-linux-gnu/pkgconfig/opencv.pc /usr/lib/x86_64-linux-gnu/pkgconfig/opencv4.pc
RUN pwd; ls
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install -r /app/requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 1000 --disabled-password --gecos "" --shell /bin/bash appuser && \
    chown -R appuser /app/
USER appuser

CMD [ "bash", "-c", "cd /app; sleep infinity" ]