sudo apt install make
sudo apt install texlive
sudo apt install texlive-latex-extra
sudo apt install texlive-xetex
sudo apt install texlive-extra-utils
sudo apt install git
sudo apt install python-pip

dpkg -i pandoc-2.7.3-1-amd64.deb

pip install jinja2
git clone https://github.com/epw/consensus.git
cd consensus
makedir ~/.fonts
cp -a /fonts/. ~/.fonts
fc-cache -f -v


