PREP = prep
GIT_ROOT = $(shell git rev-parse --show-toplevel)
DISTRO_VAL = $(shell lsb_release -r | egrep -o '[0-9]{2}.[0-9]{2}')
DISTRO =  $(strip $(DISTRO_VAL))
$(PREP):
	#First time run requires update to install pkgs
	sudo apt-get update
	#Install pbuilder and copy the conf file
	if [ -d "/var/cache/pbuilder" ]; then \
		@echo "Folder found"; \
		cp utils/.pbuilderrc ~/; \
	else \
		@echo "Folder not found"; \
		sudo apt-get install pbuilder debootstrap devscripts; \
		sudo cp utils/.pbuilderrc ~/; \
		sudo pbuilder create; \
	fi; \
	sudo pbuilder update
	mkdir -p $(GIT_ROOT)/../build

kazoo:$(PREP)
	#Copy the kazoo debian directory to build dir and prepare a .orig file
	cp -R kazoo/kazoo-1.3.1 $(GIT_ROOT)/../build/
	(cd $(GIT_ROOT)/../build ; rm -rf kazoo-1.3.1/debian/)
	(cd $(GIT_ROOT)/../build; tar -zcvf kazoo_1.3.1.orig.tar.gz kazoo-1.3.1)
	cp -Rf kazoo/kazoo-1.3.1 $(GIT_ROOT)/../build/
	#Build the kazoo from the BUILD dir
	(cd $(GIT_ROOT)/../build/kazoo-1.3.1; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

docker-py:$(PREP)
	(cd $(GIT_ROOT)/../build; wget https://pypi.python.org/packages/source/d/docker-py/docker-py-0.6.0.tar.gz)
	(cd $(GIT_ROOT)/../build; tar -xvzf $(GIT_ROOT)/../build/docker-py-0.6.0.tar.gz)
	(cd $(GIT_ROOT)/../build; cp docker-py-0.6.0.tar.gz docker-py_0.6.0.orig.tar.gz)
	cp -Rf docker-py/debian $(GIT_ROOT)/../build/docker-py-0.6.0
	#Build the docker-py from the BUILD dir	
	(cd $(GIT_ROOT)/../build/docker-py-0.6.0; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

libipfix:$(PREP)
	#copy the libipfix debian directory to build dir and prepare a .orig file
	cp -Rf libipfix/libipfix_110209 $(GIT_ROOT)/../build/libipfix_110209-1
	#Run configure once to setup the prefix path and
	# then prepare the orig.tar.gz
	(cd $(GIT_ROOT)/../build/libipfix_110209-1/; ./configure --prefix=/home/ubuntu/build/libipfix_110209-1/debian/tmp/usr)
	(cd $(GIT_ROOT)/../build ; rm -rf libipfix_110209-1/debian/)
	(cd $(GIT_ROOT)/../build; tar -zcvf libipfix_110209-1.orig.tar.gz libipfix_110209-1)
	(cd $(GIT_ROOT)/../build; rm -rf libipfix_110209-1)
	cp -Rf libipfix/libipfix_110209 $(GIT_ROOT)/../build/libipfix_110209-1
	#Change the changelog to include distro information
	(cd $(GIT_ROOT)/../build/libipfix_110209-1/; sed -i 's/(110209-1)/(110209-1-0ubuntu0.$(DISTRO))/g' debian/changelog)
	#Build the liibpfix from the BUILD dir
	(cd $(GIT_ROOT)/../build/libipfix_110209-1; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

expat:$(PREP)
	#Copy the expat debian directory to build dir and prepare a .orig file
	cp -R expat/ $(GIT_ROOT)/../build/
	(cd $(GIT_ROOT)/../build/expat;bash $(GIT_ROOT)/upstream/debian/utils/get-sources.sh)
	#Build the expat from the BUILD dir
	(cd $(GIT_ROOT)/../build/expat; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

kafka:$(PREP)
	#Get the kafka binary pkg
	(cd $(GIT_ROOT)/../build/; wget http://mirror.olnevhost.net/pub/apache/kafka/0.8.1.1/kafka_2.9.2-0.8.1.1.tgz)
	#untar the gz
	(cd $(GIT_ROOT)/../build; tar -xvzf $(GIT_ROOT)/../build/kafka_2.9.2-0.8.1.1.tgz)
	#Rename the gz file to orig.tar.gz
	(cd $(GIT_ROOT)/../build; cp kafka_2.9.2-0.8.1.1.tgz kafka_2.9.2-0.8.1.1.orig.tar.gz)
	#copy the debian  to build dir
	cp -Rf kafka*/debian $(GIT_ROOT)/../build/kafka_2.9.2-0.8.1.1
	#Build the kafka from the BUILD dir
	(cd $(GIT_ROOT)/../build/kafka_2.9.2-0.8.1.1; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

lxml:$(PREP)
	#Copy the lxml debian directory to build dir and prepare a .orig file
	cp -R lxml/ $(GIT_ROOT)/../build/
	(cd $(GIT_ROOT)/../build/lxml;bash $(GIT_ROOT)/upstream/debian/utils/get-sources.sh)
	#Build the lxml from the BUILD dir
	(cd $(GIT_ROOT)/../build/lxml; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

nodejs:$(PREP)
	#Copy the nodejs debian directory to build dir and prepare a .orig file
	cp -R nodejs/ $(GIT_ROOT)/../build/
	(cd $(GIT_ROOT)/../build/nodejs;bash $(GIT_ROOT)/upstream/debian/utils/get-sources.sh)
	#Build the nodejs from the BUILD dir
	#(cd $(GIT_ROOT)/../build/nodejs; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)
	(cd $(GIT_ROOT)/../build/nodejs; sbuild -A)

librdkafka:$(PREP)
	#copy the 0.8.5 orig.tar.gz file to build
	(cd $(GIT_ROOT)/../build; wget https://launchpad.net/ubuntu/+archive/primary/+files/librdkafka_0.8.5.orig.tar.gz)
	#copy the debian file to build
	(cd $(GIT_ROOT)/../build; tar -xvzf $(GIT_ROOT)/../build/librdkafka_0.8.5.orig.tar.gz)
	(cd $(GIT_ROOT)/../build; mv librdkafka-0.8.5 librdkafka-0.8.5-2)
	(cd $(GIT_ROOT)/../build; mv librdkafka_0.8.5.orig.tar.gz librdkafka_0.8.5-2.orig.tar.gz)
	#untar the .debian.gz file inside the untarred location
	cp -rf librdkafka*/debian $(GIT_ROOT)/../build/librdkafka*/
	#Issue pdebuild inside the source
	(cd $(GIT_ROOT)/../build/librdkafka*; sudo pdebuild --use-pdebuild-internal --debbuildopts -tc)

# Pls keep sorted (reduce merge issues)
all:$(PREP) \
	docker-py \
	expat \
	kafka \
	kazoo \
	libipfix \
	nodejs \
	librdkafka \
	lxml 
