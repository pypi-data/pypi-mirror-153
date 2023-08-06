# Web Status Checker
A health checker for a website with a is-healthy route.

> This is mostly intended to be used in my projects.

## Usage
It is expected that the server url you are querying will return a "🆗" with a 200 status code for a response. Sending anything else will result in the server signalling an error.

To run the program from CLI the following is the help dialogue:

```
usage: web_health_checker [-h] [--timeout TIMEOUT] url

Health check website

positional arguments:
  url                url to query for status

optional arguments:
  -h, --help          show this help message and exit
  --timeout TIMEOUT   timeout before connection fail
  --allow-unverified  allows for invalid self-signed certificates to be valid
```

Example:

```
python -m web_health_checker http://localhost:8080/is-healthy
```

After the command has been run depending on the state of the server different results will be output. These are shown below. The output will be sent to stdout if there is no error and stderr if there is an error.

| Output                             | Why                                                 | Is Error |
| :--------------------------------- | :-------------------------------------------------- | :------- |
| `🆗`                                | Everything is fine                                  | No       |
| `⛔ missing '🆗' in response`        | The server does not return the expected ok response | Yes      |
| `⛔ http status '<status-code>'`    | The server sent incorrect status code               | Yes      |
| `⛔ url error <reason>`             | A URL error was detected                            | Yes      |
| `⛔ remote closed without response` | The remote server closed the connection             | Yes      |
