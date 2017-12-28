#!/bin/bash
PWD=${0%/*}
printf "\t      [Virtual Domain Manager]      \n"
sudo echo

# dependency check
function pkg_check(){
	pkg=$1;
	printf "[PENDING]\t%s " $pkg
	sudo apt-get install -y $pkg 1> /dev/null
	if [[ $? -ne 0 ]]; then
		printf "[apt-get]\t%s fail.\n" $pkg
	 	exit -1
	fi
	printf "\r[INSTALLED]\t%s\n" $pkg
}

function pip_check(){
	pkg=$1;
	printf "[PENDING]\tpython-%s " $pkg
	sudo pip install $pkg 1> /dev/null
	if [[ $? -ne 0 ]]; then
		printf "[pip]\t%s fail.\n" $pkg
	 	exit -1
	fi
	printf "\r[INSTALLED]\tpython-%s\n" $pkg
}

function grep_json_item(){
	data=`(cat $PWD/config.json)|grep $1|awk -F ":" '{print $2}'`
	data=${data%\",*}
	echo ${data#\"*}
}

printf "\t======== Dependency Check ========\n"
pkg_check "rsync"
pkg_check "python-pip"
pkg_check "python-wnck"
pkg_check "python-dbus"
pip_check 'termcolor'
pip_check 'crcmod'
pip_check 'greenlet'
echo

printf "\t======== Compile & Build ========\n"
# make in bin/
# run python compile
rm -rf $PWD/build && mkdir $PWD/build
rsync -rq --exclude-from $PWD'/exclude.rsync' $PWD/* $PWD/build
echo

printf "\t========   Installation   ========\n"
read -p "Press Enter to continue..."
# python setup.py install
item=`grep_json_item "install-dir"`
# install to config.install_dir
sudo mkdir -p $item && sudo cp -rf $PWD/build/* $item
# add install_dir to path
if [[ ! $PATH =~ $item ]]; then
	echo "export PATH=\$PATH:$item" >> ~/.bashrc
	source ~/.bashrc
fi
echo

printf "\t========     Complete!    ========\n"