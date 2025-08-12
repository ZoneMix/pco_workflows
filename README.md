# Planning Center Python Workflows

A Python-based CLI repository for streamlined workflows with Planning Center Online (PCO). This project provides tools to manage people data, process custom fields, create import-ready CSVs, handle publishing episodes, and execute safe data deletions, all tailored for PCO's API. Designed for reliability and security, it includes robust error handling, rate limiting, and confirmation prompts for destructive operations.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ZoneMix/planning-center-python-workflows.git
cd planning-center-python-workflows
```

2. Install dependencies:

```bash
python3 -m venv venv
```

3. Set environment variables for PCO credentials (or use a `.env` file in the project root):

```bash
export PCO_APPLICATION_ID=your_app_id
export PCO_SECRET=your_secret
```

## Usage

Run the CLI with:

```bash
python3 run.py <command> [options]</command>
```

### Available Commands

1. **parse-authorized-pickups**
   - Description: Parses the "Authorized Pickups" field for a specific person by searching names, appending email and phone, and creating or updating a parsed version. Does nothing if the person is not found.
   - Options:
     - `--person`: Name of the person to process (required).
   - Usage: `python run.py parse-authorized-pickups --person "John Doe"`
   - Example: Processes entries for the specified person and outputs progress; echoes a message if the person or data is not found.

2. **create-csv**
   - Description: Transforms an input CSV into a PCO-compatible output CSV for data imports.
   - Options:
     - `--input`: Input CSV file path (required).
     - `--output`: Output CSV file path (required).
   - Usage: `python run.py create-csv --input input.csv --output output.csv`
   - Example: Formats phone numbers, dates, grades, and groups households.

3. **create-episode**
   - Description: Creates a new episode in PCO Publishing.
   - Options:
     - `--title`: Episode title (default: "New Episode").
   - Usage: `python run.py create-episode --title "My Episode"`
   - Example: Outputs the created episode details.

4. **delete-all**
   - Description: Deletes all people records, with optional skips. **Dangerous operation!**
   - Options:
     - `--skip-id`: Person IDs to skip (can be specified multiple times).
   - Usage: `python run.py delete-all --skip-id 123 --skip-id 456`
   - Safety: Requires confirmation before proceeding. Deletion is irreversible—back up data first!
   - Example: Fetches all IDs, skips specified ones, confirms, then deletes.

5. **delete-fields**
   - Description: Deletes all data for a specific custom field. **Dangerous operation!**
   - Options:
     - `--field`: Field name (required, e.g., "Grade").
   - Usage: `python run.py delete-fields --field "Grade"`
   - Safety: Requires confirmation before deleting.
   - Example: Deletes data for fields like "Medical Notes".

6. **get-field-data**
   - Description: Retrieves data for a specific custom or built-in field.
   - Options:
     - `--field`: Field name (required).
   - Usage: `python run.py get-field-data --field "Grade"`
   - Example: Outputs field ID (for custom fields) and all entries with person IDs and values.

7. **list-fields**
   - Description: Lists all built-in and custom field definitions with ID, Name, Slug, Data Type, and Sequence.
   - Usage: `python run.py list-fields`
   - Example: Outputs a formatted table of field definitions.

## Tutorial

### Setup
- Ensure PCO credentials are set in environment variables or a `.env` file.
- Run `pytest` to verify utility functions.

### Example Workflow: Data Import Preparation
1. Prepare an `input.csv` with columns like "First Name", "Last Name", "Birth Month and Day", etc.
2. Run `create-csv` to generate `output.csv`.
3. Import `output.csv` into PCO manually.

### Example Workflow: Parsing Pickups
- Run `parse-authorized-pickups --person "John Doe"` to process authorized pickups for a specific person.

### Example Workflow: Listing Fields
- Run `list-fields` to view all built-in and custom field definitions.

### Example Workflow: Deletion
- Run `delete-fields --field "Medical Notes"` to delete field data.
  - Confirm when prompted to avoid accidental data loss.
- Always test in a sandbox PCO account to prevent unintended data changes.

### Best Practices
- **Security**: Credentials are securely loaded from environment variables or `.env`.
- **Error Handling**: Commands include comprehensive exception handling with user-friendly error messages.
- **Testing**: Unit tests cover utility functions; expand as needed for custom workflows.
- **Rate Limiting**: API calls include a 0.2-second sleep to respect PCO's rate limits (~5 requests/second).
- **Safety**: Destructive operations (e.g., `delete-all`, `delete-fields`) require explicit user confirmation to prevent accidental data loss.

If you encounter issues, check API response details or enable logging for deeper debugging.
