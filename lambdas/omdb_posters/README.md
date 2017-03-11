# s3strm/posters

Listens for events on `s3://<movie_bucket>/<imdb_id>/video.mp4` and generates posters at `s3://<movie_bucket>/<imdb_id>/poster.jpeg`.


## Setup


0. Deploy [s3strm/s3strm](https://github.com/s3strm/s3strm).
1. Configure `./settings.inc` (see [settings.inc.sample](./settings.inc.sample) for options).
2. Deploy with `make deploy`
3. Deploy [s3strm/movies](https://github.com/s3strm/movies).

