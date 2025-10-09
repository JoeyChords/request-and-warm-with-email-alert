requestAndWarm.py is a simple solution for overcoming the 15 minute uptime
limitation Render.com has for web services that don't get much traffic, or for
eliminating cold starts from other serverless solutions. Cold starts on Render 
could mean around 1 minute of waiting for a simple website to load. Start this 
application, leave it running, and it will request your site every 14 minutes to
be sure that it is always available instantly. 

This version also uses Resend to send an email alert when something is wrong 
with the your site. You will need a Resend.com account and API key to use it. 
Resend has a free tier. 

Instructions:

Create a .env file and add COLD_URL=example.com, replacing example.com with the 
web address for the site you wish to keep running without cold starts. You will
also need to add EMAIL_FROM, EMAIL_TO, and RESEND_API_KEY.

Install requirements from requirements.txt.