<a href="https://www.superduperdb.com"><img src="https://raw.githubusercontent.com/blythed/superduperdb/main/img/symbol_purple.png" width="150" align="right" /></a>

# Welcome to SuperDuperDB!

> An AI-database management system for the full PyTorch model-development lifecycle

Full documentation [here](https://superduperdb.github.io/superduperdb).

## Installation

Requires:

- MongoDB
- RedisDB

Then install the python requirements

```
pip install -r requirements.txt
```

## Architecture

![](https://raw.githubusercontent.com/SuperDuperDB/superduperdb/main/img/architecture.png)

1. Client - run on client to send off requests to various work horses.
1. MongoDB - standard mongo deployment.
1. Vector lookup - deployment of sddb with faiss/ scaNN.
1. Job master - master node for job cluster, sends messages to redis (rq)
1. Redis database - database instance for rq master
1. Job worker - worker node(s) for jobs, computes vectors, and performs model trainings.
   Retrieves jobs from redis.