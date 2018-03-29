title: MongoDB: Sorting by external weights
date: 2018-03-22

MongoDB aggregations can be sorted by any field in a document,
but they can also be sorted by external factors.

Say we have some documents with tags:

    :::python
    {'id': 'a', 'tag': 'foo'}
    {'id': 'b', 'tag': 'bar'}
    {'id': 'c', 'tag': 'baz'}
    {'id': 'd', 'tag': 'foo'}
    {'id': 'e', 'tag': 'bar'}
    {'id': 'f', 'tag': 'baz'}
    {'id': 'g', 'tag': 'foo'}

We can weight these documents by tag. Let's order them
'bar', 'foo', 'baz'. Any documents not tagged with those
three words will get ordered last.  We can also limit
the output, asking for the first 3 documents.

    :::python
    db.collection.aggregate([
       {"$addFields": {
           "weight": {"$cond": [
               {"$eq": ["$tag": "bar"] },
               3,
               {"$cond": [ 
                   {"$eq": ["$tag": "foo"] },
                   2,
                   {"$cond": [
                       {"$eq": ["$tag": "baz"] },
                       1,
                       0
                   ]}
               ]}
           ]}
       }},
       {"$sort": { "weight": -1} },
       {"$limit": 3}
    ])

This gives the proper sorted result:

    :::python
    {'id': 'b', 'tag': 'bar'}
    {'id': 'e', 'tag': 'bar'}
    {'id': 'a', 'tag': 'foo'}
    
Note that the tagged documents may be returned in
any order, so it's undefined which `bar` is sorted first,
or which `foo` is the third result.
