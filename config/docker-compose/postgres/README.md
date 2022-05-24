## Postgres Configuration Tips

### setup user for django db

* create username with password:
```postgresql
CREATE USER <username> WITH PASSWORD 'pwd';
```
* permissions:
```postgresql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <username>;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO <username>;
```