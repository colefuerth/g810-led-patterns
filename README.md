# g810-led-patterns

Uses python and g810-led to do dynamic patterns on Logitech keyboards

**Currently only supports the 'echo' effect**

## Requirements

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install g810-led python3 python3-pip
sudo python3 -m pip install -r requirements.txt
```

## Usage

- Available colors are [here](https://www.webucator.com/article/python-color-constants-module/)
- run as root, ensure g810-led is installed

## Systemd

- Copy the service file (edited) in examples/ to `/etc/systemd/system/g810-led-patterns.service`
  - you just have to change the WorkingDirectory to the path of the repo
- run `sudo systemctl start g810-led-patterns.service` to start the service
- run `sudo systemctl enable g810-led-patterns.service` to enable the service on boot
- run `sudo systemctl status g810-led-patterns.service` to check that the service is running