# Website_BE

# 1. Send Activity Status (Test)

example json-response :

```json
{
  "auth_key": "<auth_key>",
  "response": "Test complete! All systems are active.",
}
```
- other reference:
```json
{
  "auth_key": "<auth_key>",
  "response": "Test complete! Some systems are inactive.",
  "inactive_subsystems": ["Temperature Sensor", "Motor Controller"] // Example of detailed inactive system information
}

```

# 2. Request Activity Status (Test)

example json-response :

```json
{
  "device_id": "<device_id>",
  "is_active": true,
  "timestamp": "2024-06-06T16:18:23Z" // Optional field for timestamp
}

```

# 3  Send Driver & Vehicle Data (Hardware to Firebase)

example json-response :

```json
{
  "entry_id": "<entry_id>", // Unique identifier for the entry in Firebase
  "device_id": "<device_id>", // ID of the device that sent the data
  "frame_id": "<frame_id>", // Unique identifier for the frame (if applicable)
  "timestamp": "<timestamp>", // Timestamp of data capture
  "is_anomaly": <boolean>, // Indicates if the data is associated with an anomaly
  "confidence": <number> (optional), // Confidence score for anomaly detection (0.0 to 1.0)
  "anomaly_type": "<string>" (optional) // Specific anomaly type detected (e.g., "Drowsiness", "Distraction")
}
```

# 4. Upload Driver Frame (Hardware to Firebase)

example json-response :

```json
{
  "frame_id": "<frame_id>",
  "metadata": {
    "width": <width>, // Optional: Width of the frame
    "height": <height>, // Optional: Height of the frame
    "timestamp": "<timestamp>", // Optional: Timestamp of frame capture
    "compression": "<compression>" // Optional: Compression type used (e.g., "jpeg")
  }
}
```

# 5. Append Confirmed Anomaly Video (Cloud Model to Firestore)
**Used within the “Append Confirmed Anomaly Video (Cloud Model to Firestore)”**

Method: POST

url :
 ```
api/append-confirmed-anomaly-video
```

example json-response :

```json
{
  "status": 200,
  "anomaly_detail": {// Optional: Additional details about the anomaly
   "Type": // <Type of anomaly (e.g., drowsiness, distraction)>
  }
  "message": "Confirmed anomaly video appended successfully."
}

```

# 6. Append Confirmed Anomaly Data (Cloud Model to MySQL)
**Used within the “Append Confirmed Anomaly Data (Cloud Model to MySQL)”**

Method: POST

url:
```
api/append-confirmed-anomaly-data
```

example json-response :

```json
{
  "timestamp": "<Timestamp of the anomaly detection>",
  "model": "<Name of the cloud model that detected the anomaly>",
  "data": { // Object containing details about the anomaly
    // Specific fields will depend on your anomaly data structure
    // Examples:
    "type": "<Type of anomaly (e.g., drowsiness, distraction)>",
    "confidence": <Confidence score for anomaly detection (0.0 to 1.0)>,
    "sensor_data": { // Optional: Sensor readings associated with the anomaly
      "sensor_1": <value>,
      "sensor_2": <value>,
      // ...
    },
    "video_url": "<URL of an associated video (optional)>" // Optional field
  }
}
```
# 7. Request Confirmed Anomaly Video (Firestore to Website)
Method : POST

url : 

```
api/req-confirmed-anomaly-video
```

example json-response :

```json
{
  "status": 200,
  "data": {
    "video_url": "https://example.com/confirmed_anomaly_video.mp4",
    "timestamp": "2024-06-07T12:00:00Z",
    "location": "Mine Site A"
  }
}
```

# 8. Request Confirmed Anomaly Data (MySQL to Website)

Method : POST

url :
```
api/req-confirmed-anomaly-data
```

example json-response :

```json
{
  "status": 200,
  "data": [
    {
      "anomaly_id": "123456",
      "timestamp": "2024-06-07T12:00:00Z",
      "location": "Mine Site C",
      "type": "drowsiness",
    },
    {
      "anomaly_id": "789012",
      "timestamp": "2024-06-07T13:00:00Z",
      "location": "Mine Site A",
      "type": "Gas Leak",
    }
  ]
}

```

# 9. Append Activity Data (Hardware to MySQL)

Method : POST

url
```
api/append-activity-data-hardware
```

example json-response :

```json
{
  "status": 200,
  "message": "Activity data appended successfully."
}
```

# 10. Request Activity Data (MySQL to Website)

Method : POST

url
```
api/append-activity-data-web
```

example json-response :

```json
{
  "status": 200,
  "data": [
    {
      "activity_id": "1",
      "timestamp": "2024-06-07T12:00:00Z",
      "driver_id": "123",
      "activity_type": "Speeding",
      "location": "Mine Site A",
      "speed": 85
    },
    {
      "activity_id": "2",
      "timestamp": "2024-06-07T13:00:00Z",
      "driver_id": "456",
      "activity_type": "Smoking",
      "location": "Mine Site B",
      "speed": 20
    }
  ]
}

```