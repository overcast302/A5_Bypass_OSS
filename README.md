# hacktiv8 

hacktiv8(formerly A5_Bypass_OSS) is an open-source research project focused on analyzing and experimenting with the iOS activation process. It provides a one-click cross-platform solution for bypassing activation on legacy iOS devices without the need of pwning DFU.

## Disclaimer

This project is intended strictly for research and educational purposes.  
It is not designed for, and must not be used in, production environments or for unlawful activities.  
The authors and contributors take no responsibility for any misuse or damage caused to devices, data, or systems.

## Requirements

For the `itunesstored` exploit (iOS 9 - 10), both the host and target devices must be connected to Wi-Fi at all times during operation.  
Jailbroken devices works fully offline over USB, but requires a jailbroken target.

## Compatibility

- iOS 9.0 - 10.3.4, not jailbroken
- iOS 8.0 - 8.4.1, not jailbroken (Wi-Fi-only devices)
- iOS 4.0 - 8.4.1, jailbroken

## Backend Configuration

The backend URL can be configured via Settings dialog. When left empty, the defaults from [`exploits/itunesstored/itunesstored.py`](exploits/itunesstored/itunesstored.py#L13) are used.

Due to legacy iOS devices lacking trust for modern certificate authorities, the backend must either use HTTP, or serve an SSL certificate that chains to a root CA trusted by legacy iOS. Modern certificate authorities such as Let's Encrypt are not trusted on legacy iOS versions and will cause HTTPS connections to fail on target devices.

## Credits
- [pkkf5673](https://github.com/bablaerrr)
- [bl_sbx](https://github.com/hanakim3945/bl_sbx)
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

## License

Refer to the repository license file for licensing details.
