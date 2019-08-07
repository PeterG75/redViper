![Alt text](images/redviperlogo.PNG?raw=true "redViper")

**DISCLAIMER:** redViper is a proof of concept project that aims to demonstrate a potential challenge faced within the information security arena. I **do not condone** the use of this framework for anything other than research purposes or security testing.

MAKE SURE YOU RUN THE SETUP SCRIPT BEFORE TRYING TO RUN REDVIPER

For any questions, concerns or suggestions regarding redViper, feel free to contact me on twitter [@kindredsec](https://twitter.com/kindredsec).
****
**redViper** is a Proof-of-Concept Command & Control (C2) Framework that utilizes *Reddit* for client-server communications. redViper is built in such a way so that infected hosts never communicate directly with attacker controlled infastructure, just reddit and reddit alone. 

redViper is very much an early development, proof-of-concept project that **should be used in test environments only**. In particular, the implant code is loud, insecure and not in any way ready for real red team engagements. If this proof-of-concept gains any notable interest, I will certainly begin working on making a production-ready implant. 

Additionally, due to the proof-of-concept nature of this build, the feature set is very limited. RedViper is currently only designed to send command requests and receive command output. A far more extensive feature set will be built in the future. 

For anyone who finds this project interesting and wishes to get involved, I am more than open to contributions from the community. In particular, I could really used more experienced developers to help me in building more covert and scalable implants. If you think you could contribute in this manner, feel free to reach out to me on twitter. I'm also open to any other sort of contribution as well (server code, documentation, etc).

For those interested in the specifics of the framework, [here](https://www.youtube.com/watch?v=rk4EMhq30-M) is a very detailed and granular code/design analysis video for how redViper communicates.
****
## What are the advantages of a C2 like redViper over traditional C2s?
The primary advantage of using a public platform C2 like redViper is the natural innocuity of the communications. Your C2 traffic will be sent over an encrypted TLS connection to a legitimate, reputable HTTPS site, just like the vast majority of network traffic on the internet. From a defensive perspective, it is extremely difficult, and in the right conditions blatantly impossible, to flag P2C2 (Public Platform C2) traffic as malicious. The same can't be said for traditional C2s, which often uses either their own binary protocol on an arbitrary port, or communicate over HTTP to a suspicious site that blue teams could potentially spot. Additionally, using a P2C2 essentially nullifies egress traffic filtering, since blocking HTTPS traffic over port 443 is obviously infeasible. Finally, using a P2C2 essentially cloaks your attack infrastructure completely. Since compromised hosts never communicate directly with a command server, there is virtually no way for a blue team to footprint where you're operating from. Even if the infrastructure you're operating from is burned, however, your C2 communications can STILL proceed. All you'd have to do is setup shop somewhere else, hook up to the same public platform as you were before, and your campaign can continue unimpeded. 

## What are the disadvantages of redViper?
redViper's core weakness (especially this iteration) is the vulnerability that exists in a discovered implant. This of course, is a danger for all C2s, however the consequences could be far more extreme for redViper. Due to the connectionless nature of redViper, reddit credentials are hard-coded into the implant, which means discovery of the implant could grant attackers access to one of your controlled reddit accounts. This means blue teamers could sit and peruse all the communications occurring on a particular subreddit. However, redViper is built with the ASSUMPTION that this is the case; assuming you as an operator utilize redViper properly, redViper can withstand compromised reddit credentials via multiple means; It should, however, of course be avoided. 

One additional disadvantage with redViper is the account restrictions on creating private subreddits. In order for a reddit account to be able to make a subreddit, the account must be **30 days old** and have an **unknown amount of karma**. This means that, if you don't happen to have an account of this nature available, redViper is not going to work for you "out of the box." Additionally, the creation and maintainance of private subreddits cannot be automated, which means there is light manual labor involved in operating a redViper campaign. 

## Why did you write redViper?
I wrote redViper for two reasons: To practice building Command & Control frameworks, and to raise awareness for the potential of public platform C2s. In my opinion, P2C2s are one of the toughest issues to deal with in today's environment, and there has been verifiable proof that C2s like this are being utilized by real threat actors already. Filtering out malicious traffic from legitimate traffic is to this day one of the greatest challenges defenders face; if it's hard to do now, imagine how hard it will be when P2C2s begin gaining traction. Packet filtering will be ineffective since that would block almost all legitimate traffic as well; Application-Layer inspection would be largely ineffective as well, since all the traffic being sent across the wire appears legitimate. The solutions available for this kind of problem are in my view very limited, and I think this will become an evolving issue over time. RedViper is a barebones, proof-of-concept example showing HOW a C2 of this nature may operate. If your capabilities wouldn't be able to catch this very elementary and badly designed example of a P2C2, what kind of havoc could a legitimate one wreak on your network?
****
## Setup Guides / Walkthroughs
**Setting Up a Master Account:** [PDF guide](docs/redviper_masteraccount_steps.pdf)

**Setting Up a Zombie Account:** [PDF guide](docs/redviper_zombieaccount_steps.pdf)
****
## Short Demos
**redViper:**
[![asciicast](https://asciinema.org/a/261115.svg)](https://asciinema.org/a/261115)

**redViperBuild:**
[![asciicast](https://asciinema.org/a/261117.svg)](https://asciinema.org/a/261117)

## To-Do List
- [ ] Fix potential Denial of Service
- [ ] Don't hardcode ALL message type IDs; have implants get them from the server
- [ ] Cycle Session Keys
- [ ] Have the "kill" command actual terminate implant process
- [ ] Add a channel migration command
- [ ] Send fake data during fake send alives; there's no reason to send real data, even if its encrypted by a fake key.
- [ ] Make sure accounts can authenticate during process setup
- [ ] General code cleanup; constantize some integer literals
- [ ] Send occasional fake command requests to thwart meta analysis
- [ ] Add a shell command; spawning a reverse shell directly from a command request causes some issues 
- [ ] Obfuscate Implant code
