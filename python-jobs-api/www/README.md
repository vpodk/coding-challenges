# Problem #2

Write an HTTP API to make your job processing system available over the network. You may use any language and any API pattern of your choice. Your API should support these requests:

- Create a job: The user sends a job description file in the request. The server runs the job in the background and responds immediately to the request with a string job-id.
- Wait for a job to finish: The user sends a job-id in the request. The server responds with success if the job as finished, or waits until the job finishes to respond with success.

Include the steps to build and run your program.

# Solution #2

```bash
python3 server.py
```

## Endpoints:

| HTTP request         | Description   |
| -------------------- |---------------|
| `GET /`              | Shows test HTML [page](index.html). |
| `GET /jobs`          | Gets list of all jobs. |
| `POST /jobs`         | Creates a new job. |
| `GET /jobs/{job_id}` | Gets job status. |
