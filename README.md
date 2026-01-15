# A5_Bypass_OSS

A5_Bypass_OSS is an open-source research project focused on analyzing and experimenting with legacy iOS devices based on the Apple A5 SoC.

## Disclaimer

This project is intended strictly for research and educational purposes.  
It is not designed for, and must not be used in, production environments or for unlawful activities.  
The authors and contributors take no responsibility for misuse or for any damage caused to devices, data, or systems.

## Requirements

- The target device must be connected to Wi-Fi at all times during operation.  
  Network connectivity is mandatory for the application workflow to function correctly.

## Backend Configuration

The backend URL is stored inside the payload SQLite database.

To modify it:
- Open the payload SQLite database.
- Locate the table named `asset`.
- Edit the field containing the backend URL accordingly.
- Save the database before redeploying or running the application.

No other configuration files are used for backend URL resolution.

## Developers

Brought to you by:
- overcast302
- pkkf5773

## Credits
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

## License

Refer to the repository license file for licensing details.
