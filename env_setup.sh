#!/bin/bash

# Update the system
dnf update -y

# Install Nginx and Git
dnf install -y nginx git gcc make zlib-devel bzip2-devel readline-devel libffi-devel openssl-devel xz-devel postgresql-devel sqlite-devel

# Configure Nginx to reverse proxy /resizer to the local app server running at port 8000
cat > /etc/nginx/conf.d/resizer.conf << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start Nginx and enable it to start on boot
systemctl start nginx
systemctl enable nginx

# Open port 80 for HTTP traffic using firewalld
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload