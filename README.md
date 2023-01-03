# simplemeet

It's an instant messenger website that provides a live transmission of text messages to friends.

## Demo

Website URL : https://hd.simplemeet.website/chat

Test account:
* User : 123@outlook.com
* Password : 123

## Real-time chat

User can chat with friends in real-time or leave a message.
![test](https://user-images.githubusercontent.com/93437400/210403985-9515af54-e18e-4e3f-b613-829f60cc2584.gif)

## Main Features

* Store user profile image in AWS S3 and use Cloud Front as CDN.
* Use AWS RDS as Database and set index to optimize query.
* Use Socket IO for real-time chat.
* Use AWS ElastiCache to improve loading speed for user's friend list.
* Convert domain name to IP with AWS Route 53.
* Use Nginx to redirect HTTP to HTTPS.
