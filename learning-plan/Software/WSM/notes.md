# Notes: WSM



Questions
- device configuration
    - Clock speed - do we want the clock speed to be external dante or its own clock speed and run at the same speed of the board?
    - What is rf mode lr and ld
    - I am seeing multi machine remote access, is that what we run for our mic racks?
        - I am not seeing an ip menue like on wwb, how do we configure remote access?

Possible Answers
- **Device configuration**
    - **Clock speed:**
        - If you are using Dante, set the clock source to external Dante to ensure all devices are synchronized on the same network clock.
        - If not using Dante, use the internal clock at the same sample rate as all other devices
    - **RF mode LR and LD:**
        - LR (Long Range): Optimized for maximum range and reliability
            - Typically used in challenging RF environments or for distant transmitters.
        - LD (Low Density): Allows more channels in the same spectrum, but with reduced range and possibly less robust performance.
    - **Multi machine remote access:**
        - Yes, WSM supports multi-machine remote access, which is often used for managing multiple mic racks from a single control point.
        - Unlike WWB, WSM may not have a dedicated IP menu; remote access is typically configured by ensuring all devices and computers are on the same network and using the correct IP addresses/subnets.
        - You may need to manually enter device IPs or use network discovery features within WSM to connect to remote devices.