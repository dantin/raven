# README

### Database Schema

Create `raven` schema:

    python manager.py

    db.create_all()

Create `ejabberd` schema:

    psql -U ejabber -W ejabberdb -h 127.0.0.1 < misc/ejabberd-schema.sql

### Initialize Application

Create administrator:

    python manage.py fab create-admin

Rooms

    sudo ejabberdctl create_room room01 conference.localhost localhost
    sudo ejabberdctl muc_online_rooms localhost
    sudo ejabberdctl change_room_option room01 conference.localhost members_only true
    sudo ejabberdctl change_room_option room01 conference.localhost persistent true
    sudo ejabberdctl change_room_option room01 conference.localhost public false
    sudo ejabberdctl muc_online_rooms localhost
    sudo ejabberdctl set_room_affiliation room01 conference.localhost david@localhost member
    sudo ejabberdctl set_room_affiliation room01 conference.localhost usbot@localhost member
    sudo ejabberdctl get_room_options room01 conference.localhost

### Links

- [ejabberd admin console](http://192.168.69.1:5280/admin/)
