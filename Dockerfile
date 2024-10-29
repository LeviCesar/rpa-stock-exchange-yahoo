# Use the latest Debian base image
FROM debian:latest

LABEL maintainer='levilimadev@gmail.com'

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    sudo \
    git \
    wget \
    xfce4 \
    xfce4-terminal \
    faenza-icon-theme \
    bash \
    python3 \
    python3-pip \
    tigervnc-standalone-server \
    tigervnc-common \
    dbus-x11 \
    && adduser --disabled-password --gecos '' common \
    && echo "common:common" | chpasswd \
    && echo 'common ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && git clone https://github.com/novnc/noVNC /opt/noVNC \
    && git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify 

# Install firefox
RUN sudo install -d -m 0755 /etc/apt/keyrings
RUN wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
RUN gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); if($0 == "35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3") print "\nThe key fingerprint matches ("$0").\n"; else print "\nVerification failed: the fingerprint ("$0") does not match the expected one.\n"}'
RUN echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
RUN echo 'Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000' | sudo tee /etc/apt/preferences.d/mozilla
RUN sudo apt-get update && sudo apt-get install firefox -y

# Install chromium 
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb
RUN sudo apt-get update && sudo apt-get install ./google-chrome-stable_current_amd64.deb -y

# Switch to root user to install Python packages
USER root

# Install Python packages
COPY ./src/requirements.txt /home/common/requirements.txt
RUN python3 -m pip install --break-system-packages -r /home/common/requirements.txt

# Set up VNC server
RUN mkdir -p /home/common/.vnc \
    && echo -e "#!/bin/bash\nstartxfce4 &" > /home/common/.vnc/xstartup \
    && chmod +x /home/common/.vnc/xstartup \
    && echo "common\ncommon\nn\n" | vncpasswd

# Copy entry script
COPY entry.sh /home/common/entry.sh

# Set the entry point
CMD [ "/bin/bash", "/home/common/entry.sh" ]
