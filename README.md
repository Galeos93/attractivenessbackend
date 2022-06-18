This repository contains various attractiveness-related applications that are
exposed via APIs with Flask.

Launch the app locally with the following commands:

- `docker build -t attractiveness_backend`
- `docker run --env PORT=8080 -p 8080:8080 attractiveness_backend`

Once launched, you can send queries to the API:

```bash
curl --location --request POST 'http://0.0.0.0:8080/attractiveness/rate' \
--header 'Content-Type: multipart/form-data' \
--form 'file=@/home/agarcia/filename.png'
```

This will return you a JSON with the cropped image used for the analysis and the
attractiveness score.