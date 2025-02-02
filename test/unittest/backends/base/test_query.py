from superduperdb.backends.mongodb.query import Collection
from superduperdb.base.document import Document


def test_execute_insert_and_find(local_empty_db):
    collection = Collection('documents')
    collection.insert_many([Document({'this': 'is a test'})]).execute(local_empty_db)
    r = collection.find_one().execute(local_empty_db)
    assert r['this'] == 'is a test'


def test_execute_complex_query(local_empty_db):
    collection = Collection('documents')
    collection.insert_many(
        [Document({'this': f'is a test {i}'}) for i in range(100)]
    ).execute(local_empty_db)

    cur = collection.find().limit(10).sort('this', -1).execute(local_empty_db)
    expected = [f'is a test {i}' for i in range(99, 89, -1)]
    cur_this = [r['this'] for r in cur]
    assert sorted(cur_this) == sorted(expected)


def test_execute_like_queries(db):
    collection = Collection('documents')
    # get a data point for testing
    r = collection.find_one().execute(db)

    out = (
        collection.like({'x': r['x']}, vector_index='test_vector_search', n=10)
        .find()
        .execute(db)
    )

    ids = list(out.scores.keys())
    scores = out.scores

    assert str(r['_id']) in ids[:3]
    assert scores[ids[0]] > 0.999999

    # pre-like
    result = (
        collection.like(Document({'x': r['x']}), vector_index='test_vector_search', n=1)
        .find_one()
        .execute(db)
    )

    assert result['_id'] == r['_id']

    q = collection.find().like(
        Document({'x': r['x']}), vector_index='test_vector_search', n=3
    )

    # check queries we didn't have before
    y = collection.distinct('y').execute(db)
    assert set(y) == {0, 1}

    # post-like
    result = q.execute(db)
