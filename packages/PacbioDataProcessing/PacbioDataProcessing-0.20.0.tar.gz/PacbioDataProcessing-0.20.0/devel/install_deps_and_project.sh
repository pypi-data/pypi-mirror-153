# Script to be sourced within a "python:3.9" container to prepare it
# to run the tests in a local docker container simulating the pipelines
apt-get update -qq -y
apt-get install -qq -y build-essential gcc make apt-utils
apt-get install -y software-properties-common xvfb libgtk2.0-0 libnotify4 freeglut3 libsdl1.2debian pkg-config
add-apt-repository -y -r ppa:deadsnakes/ppa
apt-get update -qq -y
apt-get install -qq -y libbz2-dev zlib1g-dev libncurses5-dev libncursesw5-dev liblzma-dev libgtk-3-dev dpkg-dev libjpeg-dev libtiff-dev libsdl1.2-dev libnotify-dev freeglut3 freeglut3-dev libghc-gtk3-dev libwxgtk3.0-gtk3-dev libgtk-3-0 libwebkit2gtk-4.0 libwebkit2gtk-4.0-dev
apt-get install -qq -y samtools
pip install pip --upgrade
pip install flit
pip install git+https://github.com/PacificBiosciences/pbcore.git
pip install git+https://github.com/PacificBiosciences/pbcommand.git
pip install git+https://github.com/PacificBiosciences/kineticsTools.git
git clone https://gitlab.com/dvelazquez/pacbio-data-processing.git
cd pacbio-data-processing/
pip install ../wxPython-4.1.1-cp39-cp39-linux_x86_64.whl 
FLIT_ROOT_INSTALL=1 flit install --deps=all
