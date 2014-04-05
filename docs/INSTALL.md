#INSTALL EasyBoardPlatform

1) Copy to /user/bin the os_scripts/eb.sh file:

	sudo cp bash/eb.sh /usr/bin/eb.sh

2) change permissions:

	sudo chmod +x /usr/bin/eb.sh

3) Configure de local_settings vars.

4) sync the database

5) run celery in background as a daemon  or run in terminal:
	
	EasyBoardPlatform$ celery -A EB worker -l info

6) run server or configure its nginx

7) Enjoy it!

##Warinig

Be sure to have a CNAME with * to use subdomains

Eg: *.@
Eg: *.easyboard.co


With love,

[Mauricio Aizaga](http://twitter.com/MaoAiz), [@MaoAiz](https://github.com/MaoAiz)
Daiech Team