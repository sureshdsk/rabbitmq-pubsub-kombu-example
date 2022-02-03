# Rabbitmq Pubsub example using kombu

## Start rabbitmq
```
docker-compose up
```

## Install dependencies
```
pip install kombu==5.2.3
```

## Start Subscribers
```
# send email on user invited
python subscriber.py example-topic app.user.invited

# send sms on user invited
python subscriber.py example-topic2 app.user.invited

# update Sales CRM
python subscriber.py example-topic3 app.user.made_admin

# listen to all user events for Audit
python subscriber.py example-topic4 "app.user.*"
```

## Start Publisher and send message
```
python publish.py
```