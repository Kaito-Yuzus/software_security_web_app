from datetime import * 


start_time = datetime(2026, 3, 25, 18, 0, tzinfo=timezone.utc)

elapsed = datetime.now(timezone.utc) - start_time 

print(elapsed)