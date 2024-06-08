import isodate


def calculate_cost(time_entries):
    amount = {}
    for time_entry in time_entries:
        currency = time_entry['hourlyRate']['currency']
        cost = time_entry['hourlyRate']['amount'] * isodate.parse_duration(time_entry['timeInterval']['duration']).total_seconds() / 3600
        cost /= 100
        amount[currency] = amount.get(currency, 0) + cost
    return amount