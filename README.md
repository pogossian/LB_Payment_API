# LB_Payment_API

## Installation:

Go to var and clone the repository.

```
$ cd /var/
$ git clone https://github.com/pogossian/LB_Payment_API.git
```

Enter the directory and create virtualenv
```
$ cd LB_Payment_API/
$ python -m virtualenv env
```

Move uwsgi to virtualenv
`$ mv uwsgi env/bin/`

Activate virtualenv 
`$ source env/bin/activate`

Install requirements [LANBilling wrapper](https://github.com/brdk/lanbilling) and [Flask](https://github.com/pallets/flask)

After requirements installation remove repositories (if you clone them) and try to import installed modules in interactive mode

```
$ python
>>> import lanbilling
>>> import flask
>>> exit()
```

Deactivate virtualenv
`$ deactivate`

## Configuration:

Add payment class as shown in [screentshot](https://raw.githubusercontent.com/pogossian/LB_Payment_API/master/screenshots/lb_settings.png)

Go to mysql and select pay_classes

```
mysql> select * from pay_classes;
+----------+-----------+--------------------------------------+-------------+
| class_id | name      | descr                                | extern_code |
+----------+-----------+--------------------------------------+-------------+
|        0 | Default   | Платеж по умолчанию                  |             |
|        1 | terminal1 | First Terminal                       |             |
|        2 | terminal2 | Second Terminal                      |             |
|        3 | terminal3 | Third Terminal                       |             |
+----------+-----------+--------------------------------------+-------------+
4 rows in set (0.00 sec)

mysql> exit
Bye
```

Open api.py, go to 18 line and specify class name and class_id in 'pay_classid' dict (as it was in mysql)

```
pay_classid = {"terminal1": 1, "terminal2": 2, "terminal3": 3}
```

Then specify terminal name and authkey in 'keys' dict (line 12)

```
keys = {
		"terminal1": "74234hfn2i378423uif2f34",
		"terminal2": "8932nfn39sama0948834892",
		"terminal3": "8809dh01083mckklaoisiak"
}
```

And, at the end fill manager login/password at line 8

```
lbapi = LANBilling(manager='username', password='password', host='127.0.0.1', port=1502)
```

Save and exit

Create vhost in nginx for uwsgi

```
server {
        listen 444 default_server;
        server_name hostname;


        ssl on;
        ssl_certificate /etc/ssl/hostname.ca-bundle;
        ssl_certificate_key /etc/ssl/hostname.key;


        location / { try_files $uri @LB_Payment_API; }
        location @LB_Payment_API {
        include uwsgi_params;
        uwsgi_pass unix:/var/LB_Payment_API/lb_api.sock;
}

}
```
###### _don't use without ssl (unless you want be sniffed)_

Test and Reload nginx 
```
$ nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
$ /etc/init.d/nginx reload
Reloading nginx configuration: nginx.
```

Run uwsgi
```
/var/LB_Payment_API/env/bin/uwsgi --ini /var/LB_Payment_API/lb_api.ini
```

To stop uwsgi
```
/var/LB_Payment_API/env/bin/uwsgi --stop /var/run/uwsgi_lb_api
```
###### _use [superviser](http://supervisord.org) or custom script to start and stop uwsgi_

## Usage

Do request for check function (specify terminal, authkey and uid)

```
https://{hostname}:444/check/terminal=terminal1&authkey=74234hfn2i378423uif2f34&uid={user_id}
```

A successful request will bring back account name and agreement information.

```
{
  "name": "Customer Fullname",
  "agreements": [
    {
      "agrm_id": 4,
      "agrm_name": "28/07/2013/0001"
    },
    {
      "agrm_id": 14225,
      "agrm_name": "6435/01/06/2017-TV"
    },
    {
      "agrm_id": 16203,
      "agrm_name": "voip-00123/13/02/2018"
    },
    {
      "agrm_id": 16219,
      "agrm_name": "00136/14/02/2018-Voip"
    }
  ]
}
```

Do request for payment function (specify terminal, authkey, agrm_id, amount and receipt)

```
https://{hostname}:444/payment/terminal=terminal1&authkey=74234hfn2i378423uif2f34&agrm_id=14225&amount=100&receipt=20180521141520-14225
```

A successful request will bring back Payment ID.
```
{
"record_id": "809661"
}
```

Do request for status function (specify terminal, authkey and record_id)

```
https://{hostname}:444/status/terminal=terminal1&authkey=74234hfn2i378423uif2f34&record_id=809661
```

A successful request will bring back account id, agreement id, receipt, terminal name, amount,
timestamp and payment date
```
{
  "uid": 4,
  "timestamp": 1526897719,
  "receipt": "20180521141520-14225",
  "terminal": "terminal1",
  "amount": 100,
  "pay_date": "2018-05-21 14:15:19",
  "agrm_id": 14225
}
```
