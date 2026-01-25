# A5_Bypass_OSS

A5_Bypass_OSS is an open-source research project focused on analyzing and experimenting with legacy iOS devices based on the Apple A5 SoC.

## Disclaimer

This project is intended strictly for research and educational purposes.  
It is not designed for, and must not be used in, production environments or for unlawful activities.  
The authors and contributors take no responsibility for misuse or for any damage caused to devices, data, or systems.

## Requirements

- The target device must be connected to Wi-Fi at all times during operation.  
  Network connectivity is mandatory for the application workflow to function correctly.

## Compatibility

The tool is compatible with all A5 devices running **iOS 9.3.6** and **iOS 9.3.5**

Support for **iOS 8.4.1** was introduced in [v1.0.1](https://github.com/overcast302/A5_Bypass_OSS/releases/tag/v1.0.1). However, it is currently broken on cellular devices (see [#7](https://github.com/overcast302/A5_Bypass_OSS/issues/7)). Wi-Fi models are fully supported.

No support for other iOS versions is planned yet.

## Backend Configuration

The backend URL is stored inside the payload SQLite database.

To modify it:
- Open the payload SQLite database.
- Locate the table named `asset`.
- Edit the `url` field containing the backend URL.
- Write database changes before running the application.

The PC client is fully offline.

## Credits
- [pkkf5673](https://github.com/bablaerrr)
- [bl_sbx](https://github.com/hanakim3945/bl_sbx)
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

## License

Refer to the repository license file for licensing details.
