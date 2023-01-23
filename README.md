# Flask_Kafka_MongoDB_Project
This is a project for Cloud Computing class. I will develop a system which reads articles from News API, retrieves some info about these articles in MediaWiki and the articles will appear to the users. Flask, Kafka and MongoDB will be used for this project

## To Run this App
- First of all you need to have kafka, Zookeeper and mongoDB installed in your system.
- Clone the repository in a directory in your filesystem.
- Run: docker-compose up -d in the terminal inside the directory in which you cloned the code.
- Open three different terminals and run the commands below.
- Run: ./run (starts the app.py and everything imported to it)
- Run: python3 kafkaProducer.py and wait for a moment. With this the producer will gather information from newsapi.org for the 8 topics we defined and send the data to Kafka in the form of messages, which are organized into topics.
- Run: python3 kafkaConsumer.py. With this the Kafka Consumer will subscribe to the Kafka topics, make the collections in the mongoDB and save the information in JSON format.

Go to http://localhost:5000/ to register and enjoy learning about the topics that interest you!
