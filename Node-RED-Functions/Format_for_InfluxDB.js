// Convert payload data into floats
var temperature = parseFloat(msg.payload.temperature); 
var humidity = parseFloat(msg.payload.humidity);
var reed_status = parseFloat(msg.payload.reed_status); 
// Check if data valid
if (isNaN(temperature) || isNaN(humidity)) {
    node.error("Payload is missing required numerical fields", msg);
    return null;
}
// Create a new payload object with converted float values
msg.payload = {
    temperature: temperature,
    humidity: humidity,
    reed_status: reed_status  
};
//Set the measurement name for InfluxDB
msg.measurement = "sensor_data";
return msg;
