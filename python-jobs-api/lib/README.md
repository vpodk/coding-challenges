# Problem #1

Make a job processing system in which jobs can have dependencies on other jobs. A user specifies the job they would like to run with a text file that looks like this:
```bash
# id identifying job in rest of file.
job_id job1
# program and arguments. run the program through the bash shell.
program cat /tmp/file2 /tmp/file3 /tmp/file4
# jobs depended on.
parent_job_ids job2 job3 job4
job_id job2
program echo hi > /tmp/file2
job_id job3
program echo bye > /tmp/file3
job_id job4
program cat /tmp/file2 > /tmp/file4; echo again >> /tmp/file4
parent_job_ids job2
```
Write a program in Python which takes this input and runs the jobs to completion with these conditions:

- Before a job can run, the jobs it depends on must have finished.
- Run jobs in parallel when possible. The user specifies the maximum number of
simultaneous running jobs as an argument to the program.

Also
- If you need external libraries, include their source code.
- Include the steps to build your program.


# Solution #1

```bash
cd lib
python3 jobs.py jobs.txt
```
