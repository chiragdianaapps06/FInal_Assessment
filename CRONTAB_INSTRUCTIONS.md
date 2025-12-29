# Crontab Configuration for Project

To schedule the cron jobs, run `crontab -e` and add the following lines at the end of the file. 

**Note**: These entries use the absolute path to your project and virtual environment.

```bash
# 1. Daily Booking Aggregation (Daily at 11:59 PM)
59 23 * * * /home/chirag/Documents/FInal_Assessment/final_assessment/.venv/bin/python3 /home/chirag/Documents/FInal_Assessment/final_assessment/crons/daily_booking_aggregation.py >> /home/chirag/Documents/FInal_Assessment/final_assessment/logs/cron_aggregation.log 2>&1

# 2. Provider Availability Sync (Every Hour)
0 * * * * /home/chirag/Documents/FInal_Assessment/final_assessment/.venv/bin/python3 /home/chirag/Documents/FInal_Assessment/final_assessment/crons/provider_availability_sync.py >> /home/chirag/Documents/FInal_Assessment/final_assessment/logs/cron_sync.log 2>&1

# 3. Upcoming Booking Reminder (Every 6 Hours)
0 */6 * * * /home/chirag/Documents/FInal_Assessment/final_assessment/.venv/bin/python3 /home/chirag/Documents/FInal_Assessment/final_assessment/crons/upcoming_booking_reminder.py >> /home/chirag/Documents/FInal_Assessment/final_assessment/logs/cron_reminder.log 2>&1
```

### **Steps to Apply:**
1. Open your terminal.
2. Type `crontab -e`.
3. Paste the lines above into the editor.
4. Save and exit.

### **Verification:**
- You can check if the cron jobs are running by looking at the log files in the `logs/` directory:
  - `tail -f logs/cron_aggregation.log`
  - `tail -f logs/cron_sync.log`
  - `tail -f logs/cron_reminder.log`
- The results will also be visible in the **Activity Logs** within the Admin Panel.
