# Website_BE

# 1. Send Activity Status (Test)
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

```json
{
  "device_id": "<device_id>",
  "is_active": true,
  "timestamp": "2024-06-06T16:18:23Z" // Optional field for timestamp
}

```

# 3  Send Driver & Vehicle Data (Hardware to Firebase)

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

```json
{
  "video_url": "<URL of the confirmed anomaly video>",
  "model": "<Name of the cloud model that detected the anomaly>",
  "timestamp": "<Timestamp of the anomaly detection>",
  "anomaly_details": { // Optional: Additional details about the anomaly
    "type": "<Type of anomaly (e.g., drowsiness, distraction)>",
    "confidence": <Confidence score for anomaly detection (0.0 to 1.0)>,
    "bounding_box": { // Optional: Bounding box of the anomaly in the video
      "x": <X-coordinate>,
      "y": <Y-coordinate>,
      "width": <Width>,
      "height": <Height>
    }
  }
}
```

# 6. Append Confirmed Anomaly Data (Cloud Model to MySQL)

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
```json 
{
  "deletions": [
    10,
    11,
    40
  ],
  "version": "5"
}
```
