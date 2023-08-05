# Synopsis
This module is an add-on for Django REST Framework, based on Django LDP add-on. It serves django models for a notifications component, respecting the Linked Data Platform convention.
It aims at enabling people with little development skills to serve their own data, to be used with a LDP application.



# Models

## Notification
An object representing a notification. A notification has the following fields:

| Field     | Type                   | Default | Description                                               |
| --------- | ---------------------- | ------- | --------------------------------------------------------- |
| `user`    | `ForeignKey` to `User` |         | User targeted by the notification.                        |
| `author`  | `LDPUrlField`          |         | ID of the user at the origin of the notification          |
| `object`  | `LDPUrlField`          |         | ID of the object which is the subject of the notification |
| `type`    | `CharField`            |         | Short description of the notification                     |
| `summary` | `TextField`            |         | Longer description of the notification                    |
| `date`    | `DateTimeField`        | `now`   | Date of the notification                                  |
| `unread`  | `BooleanField`         | `True`  | Indicates that the notification has not been read yet.    |

NB: You can access to all the notifications of a User at `[host]/users/[id]/inbox`



## Subscription

An object allowing a User to be notified of any change on a resource or a container. A subscription has the following fields:

| Field    | Type       | Default | Description                                                  |
| -------- | ---------- | ------- | ------------------------------------------------------------ |
| `object` | `URLField` |         | ID of the resource or the container to watch                 |
| `inbox`  | `URLField` |         | ID of the inbox to notify when the resource or the container change |
| `field`  | `CharField` |         | (optional) if set, then object['field'] will be sent in the notification, not object |
| `disable_automatic_notifications`  | `BooleanField` |   `False`   | By default, notifications will be sent to this inbox everytime the target object/container is updated. Setting this flag to true prevents this behaviour, meaning that notifications will have to be triggered manually |

For convenience, when you create a subscription on an object, DjangoLDP-Notification will parse the object for any one-to-many nested field relations. It will then create nested-subscriptions, i.e. a subscription on the nested field which sends an update to the same inbox, passing the parent model. If this behaviour is undesired you can delete the `Subscription` instance

You can automatically create required subscriptions based on your settings.py with this management command:

```bash
./manage.py create_subscriptions
```

# Middlewares

There is a `CurrentUserMiddleware` that catches the connected user of the last performed HTTP request and adds 
to every model before it is saved. This is useful if you need to get the connected user that performed 
the last HTTP request in a `pre_saved` signal. You can get it by using the following line :

```python
getattr(instance, MODEL_MODIFICATION_USER_FIELD, "Unknown user")
```

`MODEL_MODIFICATION_USER_FIELD` is a constant that lies in `djangoldp_notification.middlewares` and 
`instance` is the instance of your model before save in DB.

# Signals

## Create notification on subscribed objects

When an object is saved, a notification is created for all the subscriptions related to this object.

## Send email when new notification

When a notification is created, an email is sent to the user.

# Django commands

This package also bring a few Django managment command. You can use them 
at the root of your SIB project.

## `mock_notification`

This lets you create mocked notifications. Useful for develpment.  

Usage:

```
python3 manage.py mock_notification [--size <number_of_notifications>]
```

Will create the number of dummy notifications specified by `--size`. 
By default, 0.

## `suppress_old_notifications`

Will suppress old notification. This is a maintenance command to prevent 
the server to blow under the weight of your notifications.

Usage:

```
python3 manage.py suppress_old_notifications [--older <time_period>]
```

This will erase notification older than the time period specified by 
`--older`. By default, 72h ago. `time_period` is expressed in minutes. 
`d`, `h` and `m` suffix are also valid to express periods in days, 
hours and minutes.

Examples:

```shell
# Default. Will delete notifications older than 72h
python3 manage.py mock_notification
# Default. Will delete notifications older than 10 minutes ago
python3 manage.py mock_notification --older 10
# Default. Will delete notifications older than 10 days ago
python3 manage.py mock_notification --older 10d
# Default. Will delete notifications older than 10 hours ago
python3 manage.py mock_notification --older 10h
```

## Check your datas integrity

Because of the way the DjangoLDP's federation work, you may want to send your notification to every subscribers sometimes.

Follow the [check_integrity](https://git.startinblox.com/djangoldp-packages/djangoldp#check-your-datas-integrity) command of DjangoLDP to get how much resources will be impacted:

```bash
./manage.py check_integrity
```

Then run this command to send notifications:

```bash
./manage.py check_integrity --send-subscription-notifications
```

Notice that you may have to restart your ActivityQueue or your DjangoLDP server, depending on [how you configured the ActivityQueueService](https://git.startinblox.com/djangoldp-packages/djangoldp/blob/master/djangoldp/conf/server_template/server/wsgi.py-tpl#L21-24)
