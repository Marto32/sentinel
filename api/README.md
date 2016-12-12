# The Sentinel API
This directory houses the component of sentinel that is ment to run in a persistent state on a different box than any of your clients / device monitors. This will continuously run the API that each device will interface with. The devices themselves only make calls to this API when triggered. This API is what handles all logic around logging and notifications. This adds an additional layer of security as the information collected lives in a separate place from the devices. Should anything happen to the monitoring devices, we will still be able to keep a record of everything that went on up until they went offline.

## Setup
Note that to initiate this server, you must call the `sentinel_api_app.py` with some system variable settings.

Before doing this, you must ensure that you can receive traffic on port `8080` as that is where our interface will live. This is being built for an AWS EC2 instance which has all incoming HTTP connections on port `80`. By default, only the root user has access to this port, so to work around this, you have to route all connections to port `80` to port `8080` using the following command (on a unix based machine):

`iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`

To delete this routing change, you can use this:

`iptables -t nat --line-numbers -n -L`

## Starting the server
To start the server, use the following command. You can run this on the actual box (assuming you only use it for this purpose), or you can run it in a tmux or screen session:

`V_ENV='production' PYTHONPATH=[path to /sentinel] VIRTUAL_ENV=[path to virtual env if you have one] PATH=[path to bin]:$PATH LOGCONFIG=lib/logging.conf [path to python] -- api/sentinel_api_app.py`

