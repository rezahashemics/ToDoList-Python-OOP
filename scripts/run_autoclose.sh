crontab -e
# add line to run at 2:00 AM daily
0 2 * * * /path/to/ToDoList-Python-OOP/scripts/run_autoclose.sh >> /var/log/todolist_autoclose.log 2>&1
