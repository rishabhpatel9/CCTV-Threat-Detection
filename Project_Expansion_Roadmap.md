# Project Expansion Roadmap

This document outlines the sequential phases and features required to transform this project into a production ready, local first security solution for home and office environments. These enhancements focus on streamlining the initial setup, improving detection intelligence, and providing a unified monitoring experience.

## Phase 1: Docker Image and Build Optimization

Efficient containerization is critical for both the deployment speed and the storage footprint on local edge servers.

1. **Docker Ignore Pattern Implementation**
   Define a strict `.dockerignore` to exclude large training datasets, git history, and local caches from the build context, ensuring a lean image.
2. **Selective File Selection in Dockerfiles**
   Refactor Dockerfiles to use specific `COPY` commands for only necessary source files (e.g., separating backend weights from frontend code), preventing cross service bloat.
3. **External Model Weight Management**
   Transition from baking weights into the image to using volume mounts or a runtime download script, decoupling large binaries from the portable code image.
4. **Multi-Stage Build Architecture**
   Implement multi-stage Docker builds to ensure that build-time dependencies are discarded in the final production runtime image.

## Phase 2: Streamlined Onboarding and Installation


To achieve an "it just works" experience, the barrier to entry must be lowered. The current manual steps involve multiple dependencies and large file downloads that are prone to failure.

1. **Integrated Model Manager**
   Provide a startup script that automatically checks for the existence of required weights in the `Notebooks/` directory. If missing, it should download them from a cloud source like Google Drive or Hugging Face. This eliminates the dependency on Git LFS for end users.
2. **Concurrent Multi Stream Support**
   Re-engineer the backend to ingest and process multiple live video feeds simultaneously. This includes managing independent per camera buffers and ensuring that the inference engine can handle concurrent requests without bottlenecking.
3. **Graphic Configuration Wizard**
   Replace the `.env` manual editing process with a first run configuration UI in Streamlit. This wizard should help users set their camera source, sensitivity thresholds, and notification credentials without touching code.
4. **Multi Camera Discovery (ONVIF/RTSP)**
   Add a utility to scan the local network for IP cameras supporting the ONVIF protocol. This allows users to import multiple camera feeds simply by clicking "Add Found Camera" rather than manually typing long RTSP URLs.

## Phase 3: Core ML Intelligence and Privacy


Current models detect general threats but lack the nuance needed for a private home or office.

1. **Face Recognition (Whitelisting)**
   Integrate a lightweight face recognition module (like FaceNet or dlib) to distinguish between regular residents or employees and unknown individuals. This allows the system to suppress alerts when a known family member walks through the living room, significantly reducing alert fatigue.
2. **Privacy Zones and Exclusion Masking**
   Implement a UI feature that allows users to "paint" or draw polygons over the camera feed. Areas like a busy sidewalk or an oscillating fan should be masked out to prevent them from triggering false anomaly detections.
3. **Object Tracking and Temporal Persistence**
   Currently, the system analyzes frames in relative isolation. Integrating a tracker like BoT-SORT will allow the system to count how long a person has been in a specific area. This enables features like loitering detection (alert if someone stands near the door for more than 5 minutes).
4. **Geofencing and Virtual Tripwires**
   Allow users to define virtual lines across a doorway or driveway. Instead of alerting on any movement, the system only triggers if an object crosses the line in a specific direction (such as someone entering the house).

## Phase 4: Unified Management and Event History


The current interface is built for real time demos. A security system needs historical context.

1. **Unified NVR Dashboard**
   Create a centralized dashboard that supports a grid view (2x2 or 3x3) of multiple camera streams. The interface should allow clicking on a specific stream to maximize it and view live metrics.
2. **Local Event Database (SQLite/DuckDB)**
   Log every detection event into a local database. Each entry should include a timestamp, threat category, confidence score, and a reference to the saved snapshot image or 5 second video clip.
3. **Event Timeline and Search**
   Provide a searchable history page with filters for time, camera ID, and threat level. Users should be able to quickly find all violence alerts from a specific camera without scrolling through raw logs.
4. **Circular Clip Storage**
   Manage local storage by implementing a cleanup policy. For example, keep high confidence threat clips for 30 days and safe clips for only 24 hours, automatically deleting the oldest data when the disk reaches 90 percent capacity.

## Phase 5: Notifications and Connectivity


Security is only useful if the user can be notified immediately when away from the console.

1. **Universal Push Notifications**
   Integrate support for free, open source notification services like Ntfy or Gotify, in addition to Firebase Cloud Messaging. This allows users to receive instant mobile alerts with preview images without a paid SMS subscription.
2. **Mobile Web Application (PWA)**
   Optimize the Streamlit frontend for mobile browsers or convert it into a Progressive Web App (PWA). This ensures the dashboard is easily accessible on a smartphone with a native app feel.
3. **Discord and Telegram Integration**
   Add bots that can post snapshots directly into a private Discord or Telegram channel. This is often the preferred way for families or small teams to coordinate security responses.
4. **Home Automation Hooks (MQTT/Webhooks)**
   Expose an MQTT broker interface or outbound webhooks. This allows the system to trigger external actions, such as turning on the porch lights if a weapon is detected or locking smart doors if a significant anomaly is flagged.

## Phase 6: Hardware Acceleration and Portability


To run continuously, the system must be efficient and portable.

1. **Edge Device Support (TPU/NPU)**
   Optimize models for specialized hardware like the Coral Edge TPU (using TensorFlow Lite) or Intel Myriad X (using OpenVINO). This allows the system to run on a Raspberry Pi at high frame rates while consuming very little power.
2. **Sliding Window Inference for Long Videos**
   The current API takes 16 frames and returns one score. For long running camera streams, implement a rolling buffer that performs inference every few seconds, ensuring that a quick 1 second threat (like drawing a weapon) isn't missed because it happened between sample windows.
3. **Audio Anomaly Detection**
   Use the microphone feed (if available) to detect specialized sounds like glass breaking, shouting, or gunshots. Combining audio with visual data provides a much more robust fusion layer for high stakes security.

## Phase 7: Specialized Safety Features


Beyond crime detection, the system can provide value for safety and wellness.

1. **Fall and Inactivity Detection**
   Implement human pose estimation with a specific focus on falls or long periods of inactivity. This is a high value feature for elderly care in home environments or for monitoring lone workers in office warehouses.
2. **Smoke and Fire Detection**
   Train or integrate a dedicated model to identify early signs of smoke or flames. This provides an additional layer of safety that traditional smoke detectors might miss if they are not in the direct vicinity of the fire.
3. **Package and Delivery Detection**
   Add a specific classification head to YOLO for identifying boxes and mail. The system can send a package delivered notification and continue to monitor the package until a known family member retrieves it.

## Implementation Sequence Summary

1. **Optimization**: Implement Docker ignore patterns, selective copying, and multi-stage builds (Phase 1).
2. **Foundation**: Build the Model Manager, Multi-Stream Support, and Configuration Wizard (Phase 2).
3. **Dashboard**: Establish the Database and Unified NVR UI (Phase 4).
4. **Intelligence**: Add Tracking, Geofencing, and Whitelisting (Phase 3).
5. **Alerts**: Implement Push Notifications and Mobile PWA (Phase 5).
6. **Efficiency**: Port to Edge Devices and add Sliding Window logic (Phase 6).
7. **Safety**: Deploy Fall Detection and Audio Anomalies (Phase 7).

