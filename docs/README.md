

### Database Schema

Create `raven` schema:

    python manager.py

    db.create_all()

Create `ejabberd` schema:

    psql -U ejabber -W ejabberdb -h 127.0.0.1 < misc/ejabberd-schema.sql

### Links

- [ejabberd admin console](http://113.31.147.198:5280/admin/)
