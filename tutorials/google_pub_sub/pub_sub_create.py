from google.cloud import pubsub_v1


# TODO(developer)
project_id = "outreacher24"
topic_id = "oureacher24gmailPushesTopic"

#CREDS
key='04108d6d45d657d333bca6f843eed6a4699f6a4a'
service_email='gmailpushes@outreacher24.iam.gserviceaccount.com'
u_id='103733334042987399764'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

response = publisher.list_topic_subscriptions(request={"topic": topic_path})
for subscription in response:
    print(subscription)

