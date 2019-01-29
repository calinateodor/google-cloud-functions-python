from google.cloud import pubsub_v1


class PublishTopic(object):
    def publisher(self, project_id, topic_name, message_data):
        """Publishes a message to Google Pub/Sub

        Args:
            project_id (str): Google Cloud project.
            topic_name (str): Pub/Sub topic name
            message_data (str): Message to be published
        Returns:
            response (Future): An object conforming to the concurrent.futures.Future interface.
        """
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)

        # Data must be a bytestring
        data = message_data.encode('utf-8')

        #Publish
        response = publisher.publish(topic_path, data)

        return response
