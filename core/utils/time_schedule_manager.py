from core.database import queries

from datetime import datetime, time, timedelta


async def time_scheduler():
    is_exists_post = await queries.check_schedule_post()
    if is_exists_post[0][0]:
        latest_post_date = await queries.get_time_last_post()
        latest_post_date = latest_post_date[0][0]

        if time(7, 30) > latest_post_date.time() >= time(1, 30):
            send_time = latest_post_date.replace(hour=7)
            return send_time
        else:
            send_time = latest_post_date + timedelta(hours=1)
            return send_time
    else:
        if time(1, 30) < datetime.now().time() < time(7, 30):
            today_date = datetime.today().date()
            first_post_time = time(7, 30)
            send_time = datetime.combine(today_date, first_post_time)
            return send_time
        else:
            current_time = datetime.now().time()
            if current_time.minute >= 30:
                current_date = datetime.now()
                plus_one_hour_time = current_date + timedelta(hours=1)
                send_time = plus_one_hour_time.replace(minute=30, second=0)
                return send_time
            else:
                current_date = datetime.now()
                send_time = current_date.replace(minute=30, second=0)
                return send_time
