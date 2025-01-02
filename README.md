# Poetry Prompts

This is a Python script that reads a CSV of poetry prompts, randomly selects one I have not done and then sends them to my e-mail, at a schedule I set using `crontab`. 

For information about setting up non-gmail email services please references the [stmplib docs](https://docs.python.org/3/library/smtplib.html)

I added my Gmail App Password to my environment file using `EXPORT EMAILPASS='password'`

For scheduling on my mac I have used `crontab` with the following setting for one prompt every three days

```53 5 1-31/3 * * /Users/acmeuser/Documents/sync/code/email_poetry_prompts/env/bin/python3 /Users/    acmeuser/Documents/sync/code/email_poetry_prompts/daily_prompts.py```

If `crontab` is not working on your Mac, I was able to get it working by getting Vim fully configured using the Basic Version from this [Git Repo](https://github.com/amix/vimrc)

For more detailed information (instead of a CSV it references Notion), check the blog post below.

Based on [Blog Article](https://medium.com/@marco_caloba/c918c962e6b0)
