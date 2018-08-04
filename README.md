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

Deactivate virtualenv
`$ deactivate`
