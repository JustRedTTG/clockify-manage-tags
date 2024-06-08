import api
import environment
from helper import calculate_cost


def pause():
    try:
        input()
    except KeyboardInterrupt:
        exit()


if environment.user_id is None:
    print("Getting workspace users...\n")
    for user in api.get_workspace_users():
        print(f"User: `{user['name']}`\n"
              f"Email: {user['email']}\n"
              f"ID: {user['id']}\n")
    print("Please set your user ID in the environment file.")
    pause()
    exit()

print("Getting tags...")
tags = api.get_tags()

tag_ids = [tag['id'] for tag in tags]


def check_tag_missing(tag_name: str):
    return getattr(environment, tag_name) is None or getattr(environment, tag_name) not in tag_ids


missing_tags = []

for tag_name in ['paid_tag_id', 'unpaid_tag_id']:
    if check_tag_missing(tag_name):
        missing_tags.append(tag_name)

if len(missing_tags) > 0:
    print(
        f"Notice! Please set your tags in the environment file.\n"
        f"Missing tags: {', '.join(tuple(tag.upper() for tag in missing_tags))}\n\n"
        f"Here are the tags you have:\n")

    tag = None

    for tag in filter(lambda _tag: not _tag['archived'], tags):
        print(f'Tag `{tag["name"]}`\nID: {tag["id"]}\n')

    if tag is None:
        print('No tags found.')
        if len(tags) > 0:
            print('- However archived tags were found.')
    pause()
    exit()
else:
    print("Your tags are set correctly!")

print("Getting time entries...")
time_entries = api.get_time_entries()
print(f"Found {len(time_entries)} time entries.")

print("Checking time entries...")

time_entries_with_no_tags = []
time_entries_with_unpaid_tag = []
time_entries_with_paid_tag = []

for time_entry in time_entries:
    tags = time_entry['tagIds']
    if environment.unpaid_tag_id in tags:
        time_entries_with_unpaid_tag.append(time_entry)
    elif environment.paid_tag_id in tags:
        time_entries_with_paid_tag.append(time_entry)
    else:
        time_entries_with_no_tags.append(time_entry)

print(
    f"\nFound {len(time_entries_with_no_tags)} time entries with no tags.\n"
    f"Found {len(time_entries_with_unpaid_tag)} time entries with unpaid tag.\n"
    f"Found {len(time_entries_with_paid_tag)} time entries with paid tag.\n"
)

if len(time_entries_with_no_tags) > 0:
    print("Adding unpaid tag to time entries with no tags...")

    api.add_tag(time_entries_with_no_tags, environment.unpaid_tag_id)

    time_entries_with_unpaid_tag.extend(time_entries_with_no_tags)
    time_entries_with_no_tags.clear()

amount_unpaid = calculate_cost(time_entries_with_unpaid_tag)
amount_paid = calculate_cost(time_entries_with_paid_tag)

combined_paid = {}
for currency, amount in amount_unpaid.items():
    combined_paid[currency] = combined_paid.get(currency, 0) + amount
for currency, amount in amount_paid.items():
    combined_paid[currency] = combined_paid.get(currency, 0) + amount

print("Earnings:\n\n",
      '\n'.join(tuple(
          f"In {currency}:\n"
          f"Amount paid: {amount_paid.get(currency, 0):.2f}\n"
          f"Amount unpaid: {amount_unpaid.get(currency, 0):.2f}\n"
          f"Combined earnings: {combined_paid.get(currency, 0):.2f} {currency}\n"
          for currency in combined_paid.keys()
      )), sep='')

if len(time_entries_with_unpaid_tag) > 0:
    print(f"Continue if you were paid ",
          ", ".join(f"{amount:.2f} {currency}" for currency, amount in amount_unpaid.items()),
          " [Enter to continue, Ctrl+C to exit]", sep='')
    pause()

    print("Setting all unpaid to paid...")
    api.replace_tag(time_entries_with_unpaid_tag, environment.unpaid_tag_id,
                    environment.paid_tag_id)

print("You're all set!")
pause()
