scp -r * ububtu@43.205.195.234:/home/ubuntu/PLANE/PLANE-DEV/cs-plane-api
# SSH into EC2 instance and run commands
ssh ubuntu@43.205.195.234 'cd /home/ubuntu/PLANE/PLANE-DEV/cs-plane-api && \
                            sudo pip3 install -r requirements.txt && \
                            sudo python3 manage.py migrate && \
                            sudo systemctl restart gunicorn.service'
