# Notes: WWB (Wireless Workbench)

## What is Wireless Workbench?

WWB enables users to:


- **Coordinate frequencies**
	- Scan the RF environment to identify available frequencies
	- Automatically assign compatible frequencies to all devices
	- Avoid interference and optimize spectrum usage
    - Can grab frequency coordination data from previous shows by others

- **Configure devices**
	- Remotely set up and adjust wireless transmitters and receivers
	- Push configuration changes to multiple devices at once

- **Monitor in real time**
	- Track RF signal strength, battery status, and audio levels
	- Receive alerts for dropouts, low battery, or interference
	- Log and review performance data during events

- **Frequency cordination**
    - The noise floor is generated during a scan and the goal will be to find frequencies that do not have additional signal on them above the noise floor.
    - Calculate and deploy the frequencies
        - Consider if there are tv chanel regulation or licencing requirments for the area
    - Insert exlusion zones on tv channels that have obious rf broadcasts happening to ensure that workbench does not add frequencies even if the noise is below the exclusion threshold
    - Any devices above scan peak threshold are assumed to be other transmitters and intermodulation is accounted for (can be altered via the diamond)

- **Ad600**
    - It can perform continuous detailed scans, identify sources of interference, and help optimize frequency coordination.
    - Does not allow for transmitter wirless updates, but will be able to instantly identify new interference sources during a show and give solution frequencies

- **Frequency Spacing**
    - How much space is needed between rf frequencies to operate correctly
    - Intermodulation spacing
        - 3rd order- First harmonic (most energy)
        - 5th order- Second harmonic
        - Thrid transmitter 3rd order harmonic (large energy)
    - larger space between frequency often gives more reliability.
    - Spacing math can be switched in compatability screen of frequency cordination
Create different inclusion groups for robust, standard and more mic spacing. Put main mics into the robust to protect their rf and the less important mics into standard or more to fit a higher channel count into the space.
    - Experiment with the frequency cordination to get the best solution for the specific show needs and scan data.

Axient ADX tranmitters can be remote controlled by show link and an ad600 alowing 0 interferience