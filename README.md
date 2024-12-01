# todo-app
Todo Application Backend

# High Level Specification
### Create:
- [x] Accepts title(should be a minimum of 8 characters), deadline (cannot be in the past) and status (default to shelved)
- [x] Status cannot be complete

### Update:
- [X] Title, deadline and status can be changed
- [X] Once task has been completed, it  cannot be updated
- [ ] updated_at field will automatically get populated based on the most recent update

### Delete:
- [x] Any task can be deleted

### Read:
- [X] Tasks can be searched based on title, status and date_range

### Others:
- [ ] Everything should be timezone aware
