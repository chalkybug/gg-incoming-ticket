from services import forecast
from datetime import datetime

# internal import
import debugpy

# main
if __name__ == "__main__":
    print(f"Chạy lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # debugpy.listen(("0.0.0.0", 5678))
    # debugpy.wait_for_client()
    # breakpoint()
    forecast()

    print(f"Chạy xong: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
