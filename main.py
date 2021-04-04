from nsepy import get_history, get_expiry_date
from datetime import date, datetime
from calendar import monthrange
import random

now = datetime.now()

start_year = int(input("Enter start year(>= 2000): "))
end_year = int(input(f"Enter end year(<= {now.year}): "))
sip_amount = int(input("Enter sip amount(> 0): "))
symbol = input("Enter index symbol(Ex: NIFTY 50)")

result = {
    "first_day": {
        "Close": {
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "mid_day": {
        "Close": {
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "last_day": {
        "Close": {
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "second_last_day": {
        "Close": {
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "total_units": 0,
            "last_closing_price": 0
        }
    },
}

month_count = 0

for y in range(start_year, end_year + 1):
    last_month = now.month if now.year == y else 12

    for m in range(1, last_month + 1):
        mr = monthrange(y, m)

        nse_data = get_history(symbol=symbol.upper(),
                               start=date(y, m, 1),
                               end=date(y, m, mr[1]),
                               # expiry_date=get_expiry_date(y, m),
                               index=True)

        month_count += 1

        for key, value in result.items():
            investment_day = 0
            if key == "last_day":
                investment_day = len(nse_data) - 1
            elif key == "mid_day":
                investment_day = len(nse_data) // 2
            elif key == "second_last_day":
                investment_day = len(nse_data) - 2

            last_closing_price = nse_data.iloc[investment_day]["Close"]

            for investment_time in value.keys():
                result[key][investment_time]["last_closing_price"] = last_closing_price
                result[key][investment_time]["total_units"] += sip_amount / \
                    nse_data.iloc[investment_day][investment_time]

    print("=" * 50)
    print(f"YEAR {y}")
    for key, value in result.items():
        print("*" * 21, "  ", key, "  ", "*" * 21)
        for investment_time in value.keys():
            print("-" * 21, "  ", investment_time, "  ", "-" * 21)
            print(
                f"Total amount invested till year {y}: {month_count * sip_amount}")
            print(
                f'Total value at the end of the year {y}: {int(result[key][investment_time]["last_closing_price"] * result[key][investment_time]["total_units"])}')
            print(
                f'Total units bought via sip of {sip_amount} till year {y}: {result[key][investment_time]["total_units"]}')
            print("*" * 50)
    print("=" * 50)
    print("\n\n")


print("=" * 50)
print(f"Final Result: ")
for key, value in result.items():
    print("*" * 21, "  ", key, "  ", "*" * 21)
    for investment_time in value.keys():
        print("-" * 21, "  ", investment_time, "  ", "-" * 21)
        print(
            f"Total amount invested: {month_count * sip_amount}")
        print(
            f'Total value: {int(result[key][investment_time]["last_closing_price"] * result[key][investment_time]["total_units"])}')
        print(
            f'Total units bought via sip of {sip_amount}: {result[key][investment_time]["total_units"]}')
        print("*" * 50)
print("=" * 50)
print("\n\n")
print("=" * 50)
print("Raw result")
print(result)
print("=" * 50)
