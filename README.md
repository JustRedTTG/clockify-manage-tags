# Clockify tag manager
The idea of this tool is to allow invoicing using only the free plan,
by manually editing the tags of the time entries for you.

Doing this allows you to filter unpaid time entries in the overview page!
## What it does:
- Adds unpaid tag to all time entries
- Allows you to replace unpaid tag with paid tag

## How to use:
### 1. Get your Workspace ID
- go to your workspace settings

![Workspace settings](/docs/workspace_settings.png "Workspace settings")

- Copy your Workspace ID from the URL bar

![Workspace ID](/docs/workspace_id.png "Workspace ID")

### 2. Get your API key
- go to your profile preferences

![Profile preferences](/docs/profile_preferences.png "Profile preferences")

- go to the advanced section

![Advanced section](/docs/profile_advanced.png "Advanced section")

- generate your api key

![API key](/docs/generate_api_key.png "API key")

### 3. Optionally if you haven't already, create your tags

![Tags](/docs/tag_creation.png "Tags")

### 4. Add the workspace ID and API key to a .env file

![Initial .env](/docs/initial_env.png "Initial .env")

### 5. Run the script to get the rest of the variables
- Getting the user ID

![Getting the user ID](/docs/workspace_users_id.png "Getting the user ID")

- Getting the tag IDs

![Getting the tag IDs](/docs/workspace_tags_id.png "Getting the tag IDs")

### 6. You're ready to go!
Running the script again will add the unpaid tag to all time entries
if they don't already have it.

After you've been paid you can run the script and press enter to replace all unpaid time entries with the paid tag.