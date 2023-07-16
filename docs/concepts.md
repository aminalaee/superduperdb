# Important Concepts

The SuperDuperDB workflow looks like this:

1. The user adds data to SuperDuperDB, which may include user defined **encoders**, and external web or other content.
2. The user uploads one or more **models** including weights or parameters to SuperDuperDB, configuring which models should be applied to which data, by linking models to a
   query and key. 
3. (Optionally) SuperDuperDB creates a **job** to train the uploaded models on the data contained in the database.
4. SuperDuperDB creates a **job** applying the **models** to their configured data and the outputs are stored in the documents to which the **models** were applied.
5. SuperDuperDB **watches** for when new data comes in, when the **models** which have already been uploaded are reactivated.
6. (Optionally) SuperDuperDB retrains **models** on the latest data.
7. SuperDuperDB creates a **job** to apply the **models** to data, which has yet to be processed, and the outputs
   are stored in the documents to which the **models** were applied.
8. At inference time, the outputs of the applied **models** may be queried using classifical DB queries,
   or, if the outputs are vectors, searched using a **vector-index**.

![](img/cycle-linear.svg)

The key concepts are:

* [Encoders](#encoders)
* [Models](#models)
* [Watchers](#watchers)
* [Vector-Indexes](#vector-indexes)
* [Jobs](#jobs)

## Encoders

A type is a Python object registered with a SuperDuperDB collection which manages how
model outputs or database content are converted to and from ``bytes`` so that these may be
stored and retrieved from the database. Creating types is a prerequisite to adding models
which have non-Jsonable outputs to a collection, as well as adding content to the database
of a more sophisticated variety, such as images, tensors and so forth.

A type is any class with ``.encode`` and ``.decode`` methods
as well as an optional ``.types`` property.

Read in more detail here.

*Content*

Often building and training AI applications requires the awkward task of downloading, pulling and
scraping diverse bits of data from the web, file-servers and systems, and object storage.
To facilitate this, SuperDuperDB allows users to specify the **content** of a key-value pair
using references to external sources.
For those bits of content which are referred to in this way, SuperDuperDB creates a :ref:`job <Jobs>` which fetches the bytes from the
described location, and inserts these into MongoDB.


## Models

A **model** in SuperDuperDB is a PyTorch model, with (optionally) two additional methods ``preprocess``
and ``postprocess``. These methods are necessary so that the model knows how to convert content from 
the database to tensors, and also to convert outputs of the object into a form which is appropriate 
to be saved in the database.

Read in more detail here.

## Watchers

Once you have one or more models registered with SuperDuperDB, the model(s) can be set up to 
**watch** certain sub-keys (``key``) or full documents in MongoDB collections, and to compute outputs
from those inputs when new data comes in or updates are made to the database.

When a **watcher** is created based on a SuperDuperDB model, a dataloader is created which
loads data from the database, passes the data inside the configured ``key`` to the model's
``preprocess`` method, batches the tensors and passes these to the model's ``forward`` method,
and finally unpacks the batch and applies the model's ``postprocess`` method to the lines of 
output from the model. The results are saved in ``"_outputs.<key>.<model_name>"`` of the collection 
documents.

Read in more detail here.

## Vector-Indexes

Models and their outputs may be used in concert, to make the content of SuperDuperDB collections
searchable. A **vector-index** consists of one or more models, which produce PyTorch vector or tensor
outputs.

Examples of the use of vector-indexes are:

* Search by meaning in NLP
* Similar image recommendation
* Similar document embedding and recommendation
* Facial recognition
* ... (there are many possibilities)

For example, a semantic index could consist of a pair of models, where one model understands text and
the other understands images. Using this pair, one can search for images using a textual description of the image.

SuperDuperDB may be used to train or fine-tune semantic-indexes.

Read in more detail here.

## Jobs

Whenever SuperDuperDB does any of the following:

* Data insertion
* Data updates
* Model creation
* Model training
* Semantic index updates
* Neighbourhood calculations

then SuperDuperDB is required to perform certain longer running computations.
These computations are wrapped as **jobs** and these are executed asynchronously on
a pool of parallel workers.

SuperDuperDB may also be used in the foreground, so that calculations block the Python program. 
This is recommended for development purposes only.

Read in more detail here.