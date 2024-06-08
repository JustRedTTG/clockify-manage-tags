import api
import environment

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
    exit()
else:
    print("Your tags are set correctly!")

print("Getting time entries...")
time_entries = api.get_time_entries()
print(f"Found {len(time_entries)} time entries.")

print("Checking tags...")

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

if len(time_entries_with_unpaid_tag) > 0:
    print("Continue if you were paid {amt} [Enter to continue, Ctrl+C to exit]")
    input()

    print("Setting all unpaid to paid...")
    api.replace_tag(time_entries_with_unpaid_tag, environment.unpaid_tag_id,
                    environment.paid_tag_id)

print("You're all set!")
input()
