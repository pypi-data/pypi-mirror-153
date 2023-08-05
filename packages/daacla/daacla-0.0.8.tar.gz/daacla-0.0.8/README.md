
# daacla

Python module to management `dataclass` objects using SQLite


# Usage

```
from dataclasses import dataclass
from datetime import datetime

from daacla import Daacla, table


@dataclass
@table(key='url')  # `key` means primary key
class Post:  # makes `Post` table on the `db` database
    url: str
    created_at: float


db = Daacla()

# Update/Insert a record
db.upsert(Post(url='https://example.com/page/1', created_at=datetime.now().timestamp()))

# Check existence of the record
print( db.exists(Post, key='https://example.com/page/1') )  # → True

# Check existence of the record
print( db.exists(Post, key='https://example.com/page/NOTHING') )  # → False

# Search
url = 'https://example.com/page/1'
for post in db.select(Post, 'url = ?', url):
  print(post.url)  # → https://example.com/page/1
```
