# [simplemeet](https://hd.simplemeet.website/)

It's an instant messenger website that provides a live transmission of text messages to friends.

## Demo

Website URL : https://hd.simplemeet.website/

Test account:
* User : 123@outlook.com
* Password : 123

## Real-time chat

User can chat with friends in real-time or leave a message.
![hacyn-rhni3](https://user-images.githubusercontent.com/93437400/211187622-d2695e6f-f2e5-41b3-bdbe-619bfc2a4a5a.gif)


## Main Features

* Supported historical messages and emoji emoticons
* Stored user profile image in AWS S3 and use Cloud Front as CDN.
* Created AWS RDS as Database and set index to optimize query.
* Used Socket IO for real-time chat.
* Increased loading speed by friend list through AWS ElastiCache.
* Converted domain name to IP with AWS Route 53.
* Utilized Nginx to redirect HTTP to HTTPS.

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
* Auto Scaling
* Load Balance
* Cloud Watch

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
