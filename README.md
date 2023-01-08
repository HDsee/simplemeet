# [simplemeet](https://hd.simplemeet.website/)

It's an instant messenger website that provides a live transmission of text messages to friends.

## Demo

Website URL : https://hd.simplemeet.website/

Test account:
* User : 123@outlook.com
* Password : 123

## Real-time chat

User can chat with friends in real-time or leave a message.
![test](https://user-images.githubusercontent.com/93437400/210403985-9515af54-e18e-4e3f-b613-829f60cc2584.gif)
![test (1)](https://user-images.githubusercontent.com/93437400/211186767-ec4a994c-3d4e-4421-ab0f-a2d4b238b381.gif)

## Main Features

* Store user profile image in AWS S3 and use Cloud Front as CDN.
* Use AWS RDS as Database and set index to optimize query.
* Use Socket IO for real-time chat.
* Use AWS ElastiCache to improve loading speed for user's friend list.
* Convert domain name to IP with AWS Route 53.
* Use Nginx to redirect HTTP to HTTPS.

## System Architecture
![system](https://user-images.githubusercontent.com/93437400/210485986-de26db95-f66b-47b8-bd03-c1f834e46520.png)


## Backend Technique

### Deployment
* Docker

### Environment
* Python Flask

### Database
* MySQL
* Redis(cache)

### Cloud Service (AWS)
* EC2
* S3, CloudFront
* RDS
* ElastiCache

### Networking
* HTTP & HTTPS
* Domain Name System
* NGINX
* SSL

### Version Control
* Git/GitHub

### Design Pattern
* MVC

### Front-End Technique
* HTML
* CSS
* JavaScript

### Contact

👨🏻‍💻 蔡懷德 Huai De Tsai

📬 Email : huaide_tasi@outlook.com
