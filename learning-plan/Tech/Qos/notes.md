# Notes: Qos

# What is QoS (Quality of Service)?

Quality of Service (QoS) refers to a set of technologies and techniques used to manage network resources and prioritize certain types of traffic. The goal is to ensure that critical or time-sensitive data (such as voice, video, or control signals) is delivered reliably, even when the network is congested.

## Why is QoS Important?
- **Prevents congestion:** Ensures important data is not delayed or dropped when the network is busy.
- **Prioritizes critical traffic:** For example, a main phone line or real-time audio (like Dante audio signals) can be prioritized over less critical traffic (such as web browsing or file downloads).
- **Improves reliability:** Essential for applications that require low latency and minimal packet loss (e.g., VoIP, live audio/video, control systems).

## How Does QoS Work?
- **Classification:** Network devices identify and categorize traffic (e.g., voice, video, data).
- **Prioritization:** Higher priority is given to critical traffic using methods like traffic shaping, queuing, and scheduling.
- **Traffic Shaping:** Controls the flow of data to prevent bottlenecks.
- **Policing:** Drops or re-marks packets that exceed allowed rates.

## Real-World Examples
- **Phone Systems:** The main phone line is prioritized over customer or guest phones to ensure emergency calls always go through.
- **Audio Networks (Dante):** Dante audio signals are prioritized over general internet traffic to prevent audio dropouts during live events.
- **Video Conferencing:** Video and audio streams are prioritized over background data transfers.

## Key QoS Techniques
- **DiffServ (Differentiated Services):** Uses DSCP markings in IP headers to classify and manage traffic.
- **802.1p:** Layer 2 prioritization for Ethernet frames.
- **Queuing Algorithms:** Such as FIFO, Weighted Fair Queuing (WFQ), and Low Latency Queuing (LLQ).

## Best Practices
- Identify critical applications and traffic types in your network.
- Apply QoS policies at network entry points (switches, routers).
- Monitor and adjust policies as network usage changes.

---
**References:**
- Cisco: [Quality of Service Overview](https://www.cisco.com/c/en/us/solutions/enterprise-networks/quality-of-service-qos/index.html)
- Audinate (Dante): [Dante Networking Basics](https://www.audinate.com/learning/faqs/dante-networking-basics)