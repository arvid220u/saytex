python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

# SET UP SERVER
# 1: add nameservers and stuff in digitalocean
# 2: install nginx
apt-add-repository ppa:nginx/stable -y
apt-get update --assume-yes
apt-get install nginx --assume-yes

# 2: point nginx to gunicorn
cp flask_nginx.conf /etc/nginx/conf.d/flask-app.conf
sed -i 's/include \/etc\/nginx\/sites\-enabled\/\*;/#include \/etc\/nginx\/sites\-enabled\/\*;/' /etc/nginx/nginx.conf

# 3: install certbot for https
apt-get update
apt-get install software-properties-common
add-apt-repository universe -y
add-apt-repository ppa:certbot/certbot -y
apt-get update
apt-get install python-certbot-nginx --assume-yes

# 4: use certbot
certbot --nginx -d api.saytex.xyz
# autorenewal
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo '43 1,13 * * * certbot renew --post-hook "service nginx reload"' >> mycron
#install new cron file
crontab mycron
rm mycron

# 5: start nginx
fuser -k 80/tcp
service nginx restart
service nginx reload
