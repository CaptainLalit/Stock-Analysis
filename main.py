from nsepy import get_history, get_expiry_date
from datetime import date, datetime
from calendar import monthrange
import random

now = datetime.now()

start_year = int(input("Enter start year(>= 2000): "))
end_year = int(input(f"Enter end year(<= {now.year}): "))
sip_amount = int(input("Enter sip amount(> 0): "))
increase_precentage_per_year = float(
    input("Increase sip amount per year in percentage(>= 0): "))
symbol = input("Enter index symbol(Ex: NIFTY 50): ")

result = {
    "first_day": {
        "Close": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "mid_day": {
        "Close": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "last_day": {
        "Close": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "second_last_day": {
        "Close": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "third_last_day": {
        "Close": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        }
    },
    "fourth_last_day": {
        "Close": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        },
        "Open": {
            "invested": 0,
            "total_units": 0,
            "last_closing_price": 0
        }
    },
}

result_every_day = {}

print("Skipping current month if current year is selected in analysis")

for y in range(start_year, end_year + 1):
    last_month = now.month - 1 if now.year == y else 12

    for m in range(1, last_month + 1):
        mr = monthrange(y, m)

        nse_data = get_history(symbol=symbol.upper(),
                               start=date(y, m, 1),
                               end=date(y, m, mr[1]),
                               # expiry_date=get_expiry_date(y, m),
                               index=True)

        for key, value in result.items():
            investment_day = 0
            if key == "last_day":
                investment_day = len(nse_data) - 1
            elif key == "mid_day":
                investment_day = len(nse_data) // 2
            elif key == "second_last_day":
                investment_day = len(nse_data) - 2
            elif key == "third_last_day":
                investment_day = len(nse_data) - 3
            elif key == "fourth_last_day":
                investment_day = len(nse_data) - 4

            last_closing_price = nse_data.iloc[investment_day]["Close"]

            for investment_time in value.keys():
                result[key][investment_time]["last_closing_price"] = last_closing_price
                result[key][investment_time]["invested"] += sip_amount
                result[key][investment_time]["total_units"] += sip_amount / \
                    nse_data.iloc[investment_day][investment_time]

        # for investment_day in range(1, len(nse_data) + 1):
        #     if not bool(result_every_day.get(f"day_{investment_day}", None)):
        #         result_every_day[f"day_{investment_day}"] = {
        #             "Close": {
        #                 "invested": 0,
        #                 "total_units": 0,
        #                 "last_closing_price": 0
        #             },
        #             "Open": {
        #                 "invested": 0,
        #                 "total_units": 0,
        #                 "last_closing_price": 0
        #             }
        #         }

        #     last_closing_price = nse_data.iloc[investment_day - 1]["Close"]

        #     for investment_time in result_every_day[f"day_{investment_day}"].keys():
        #         result_every_day[f"day_{investment_day}"][investment_time]["last_closing_price"] = last_closing_price
        #         result_every_day[f"day_{investment_day}"][investment_time]["total_units"] += sip_amount / \
        #             nse_data.iloc[investment_day - 1][investment_time]

        # increment the sip amount
        sip_amount += int(sip_amount * (increase_precentage_per_year / 100))

    print("=" * 50)
    print(f"YEAR {y}")
    for key, value in result.items():
        print("*" * 21, "  ", key, "  ", "*" * 21)
        for investment_time in value.keys():
            print("-" * 21, "  ", investment_time, "  ", "-" * 21)
            print(f"Current SIP amount: {sip_amount}")
            print(
                f'Total amount invested till year {y}: {result[key][investment_time]["invested"]}')
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
        amount_invested = result[key][investment_time]["invested"]
        current_value = int(result[key][investment_time]["last_closing_price"]
                            * result[key][investment_time]["total_units"])
        print("-" * 21, "  ", investment_time, "  ", "-" * 21)
        print(
            f"Total amount invested: {amount_invested}")
        print(
            f'Total value: {current_value}')
        print(
            f'Total units bought via sip of {sip_amount}: {result[key][investment_time]["total_units"]}')
        print(
            f'Absolute returns: {(current_value - amount_invested) / amount_invested * 100}')
        print(
            f'SIP CAGR on final invested amount: {((current_value / amount_invested) ** (1 / (end_year - start_year)) - 1) * 100}')
        print("*" * 50)
print("=" * 50)
print("\n\n")
print("=" * 50)
print("Raw result")
print(result)
print("=" * 50)
print("\n\n")

# print("=" * 50)
# print(f"Final Result of investing in any particular day of month: ")
# for key, value in result_every_day.items():
#     print(
#         key,
#         " -> ",
#         f'{int(value["Open"]["last_closing_price"]* value["Open"]["total_units"])} / {int(value["Open"]["total_units"])}',
#         "  ",
#         f'{int(value["Close"]["last_closing_price"] * value["Close"]["total_units"])} / {int(value["Open"]["total_units"])}'
#     )
# print("\n\n")
# print("=" * 50)
# print("Raw result")
# print(result_every_day)
# print("=" * 50)
