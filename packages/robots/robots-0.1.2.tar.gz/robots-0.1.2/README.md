# Robots
A lightweight automation tool.


## How to use
### Android Bot
* Initialize the robot and connect the device:
```python
from robots import AndroidBot

robot = AndroidBot("device_serial_number")
```

* Open a page(activity) within the app:
```python
robot.open("app_url_scheme")
```

* Extract UI rendered content using xpath:
```python
robot.xpath("xpath_expression")
```
