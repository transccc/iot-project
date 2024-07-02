// Headers for the HTTP request. Content type json
msg.headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_token"
};
msg.payload = {
    "active": true,
    "iden": "your_token",
    "created": (new Date()).getTime() / 1000,
    "modified": (new Date()).getTime() / 1000,
    "type": "note",
    "dismissed": false,
    "direction": "self",
    "sender_iden": "your_id",
    "sender_email": "your_mail@gmail.com",
    "sender_email_normalized": "your_mail@gmail.com",
    "sender_name": "your_name",
    "receiver_iden": "your_id",
    "receiver_email": "your_mail@gmail.com",
    "receiver_email_normalized": "your_mail@gmail.com",
    "title": "Door Status Notification",
    "body": "Door is open"
};
return msg;
