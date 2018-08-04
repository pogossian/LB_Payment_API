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
###### _don't use without ssl_

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
