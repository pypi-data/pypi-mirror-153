def run_everyday_between(start_time: str, end_time: str, job, *args, **kwargs):
    """run given job between given time.

    Args
    ----
        start_time (str): The time to be start
        end_time (str): The time to be end
        job (function): The function to be execute
    
    Optional
    --------
        args : if a function has a args
        kwargs : if a function has a kwargs
    """
    import datetime
    start_hour, start_minute = [int(x.strip()) for x in start_time.split(':')]
    end_hour, end_minute = [int(x.strip()) for x in end_time.split(':')]
    
    while True:
        now = datetime.datetime.now()
        if datetime.timedelta(hours=start_hour, minutes=start_minute) <= datetime.timedelta(hours=now.hour, minutes=now.minute) <= datetime.timedelta(hours=end_hour, minutes=end_minute):
            if args:
                if kwargs:
                    job(*args, **kwargs)
                else:
                    job(*args)
            else:
                if kwargs:
                    job(**kwargs)
                else:
                    job()