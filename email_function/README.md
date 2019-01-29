### Introduction
* Proof of concept phase  
* Limitations: the service account running the function needs domain wide access in order to work. This limitation is due to the fact that service accounts can\'t send out emails by themselves and need to connect to a normal address to do that but for that they need permissions.   
* Google Cloud function triggered by a Pub/Sub event. Automatically sends out an email with the pusblished message to a predefined email address
