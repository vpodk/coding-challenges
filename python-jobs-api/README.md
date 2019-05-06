# Solution 1

```bash
cd lib
python3 jobs.py jobs.txt
```

# Solution 2

```bash
cd www
python3 server.py
```

## Endpoints:

| HTTP request         | Description   |
| -------------------- |---------------|
| `GET /`              | Shows test HTML [page](www/index.html). |
| `GET /jobs`          | Gets list of all jobs. |
| `POST /jobs`         | Creates a new job. |
| `GET /jobs/{job_id}` | Gets job status. |
