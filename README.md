# todo-app
Todo Application Backend

# High Level Specification
### Create:
- [x] Accepts title(should be a minimum of 8 characters), deadline (cannot be in the past) and status (default to shelved)
- [x] Status cannot be complete

### Update:
- [ ]Title and deadline can be changed
- [ ] Once task has been completed, no field can be changed
- [ ] updated_at field will automatically get populated based on the most recent update

### Delete:
- [x] Any task can be deleted

### Read:
- Tasks can be searched based on title, status and date_range

### Others:
- [ ] Everything should be timezone aware
