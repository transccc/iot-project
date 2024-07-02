var temperature = parseFloat(msg.payload.temperature);
var humidity = parseFloat(msg.payload.humidity);
var reed_status = parseFloat(msg.payload.reed_status); 

if (isNaN(temperature) || isNaN(humidity)) {
    node.error("Payload is missing required numerical fields", msg);
    return null;
}

msg.payload = {
    temperature: temperature,
    humidity: humidity,
    reed_status: reed_status  
};

msg.measurement = "sensor_data";
return msg;
