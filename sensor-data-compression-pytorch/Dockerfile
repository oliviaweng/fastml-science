FROM pytorch/pytorch

#Install dependencies
RUN apt-get update && apt-get install -y git 
RUN apt-get update && \
    apt-get install -y \
    python-setuptools \
    python-dev 
RUN apt-get update && \
    apt-get install -y \
    vim tmux htop apt-utils
RUN apt-get update && apt-get install -y gcc g++ ninja-build build-essential
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get update && apt-get install -y --no-install-recommends libopencv-dev libturbojpeg-dev
# cuda specific to individual machine setup
# RUN cp -f /usr/lib/x86_64-linux-gnu/pkgconfig/opencv.pc /usr/lib/x86_64-linux-gnu/pkgconfig/opencv4.pc
RUN conda install --freeze-installed cupy -c conda-forge
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install -r /app/requirements.txt
# cuda specific to individual machine setup
# RUN ln -s /opt/conda/lib/libcudart.so /usr/lib/libcudart.so
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 50075597 --disabled-password --gecos "" --shell /bin/bash appuser && \
    chown -R appuser /app/
USER appuser

CMD [ "bash", "-c", "cd /app; sleep infinity" ]