import csv
import click
from pco_workflows.utils import (
    format_phone, yes_no_to_true_false, map_grade, get_status_and_membership,
    format_birthdate, format_anniversary
)

OUTPUT_HEADERS = [
    "remote_id", "First Name", "Middle Name", "Last Name",
    "Birthdate", "Anniversary", "Gender", "Grade", "Medical Notes", "Marital Status", "Status", "Membership",
    "Home Address Street Line 1", "Home Address City", "Home Address State", "Home Address Zip Code",
    "Mobile Phone Number", "Home Phone Number", "Work Phone Number",
    "Home Email", "Household ID", "Household Name", "Household Primary Contact",
    "Baptized", "Baptism Date", "Member By", "Membership Date", "Sunday School", "Small Group",
    "Emergency Contact", "Emergency Phone", "Allergies", "Authorized Pickup"
]

def create_import_csv(input_file, output_file, current_year=2025):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=OUTPUT_HEADERS)
            writer.writeheader()

            family_id = 1
            previous_last_name = None
            remote_id_counter = 1

            for row in reader:
                last_name = row.get("Last Name", "").strip()
                if last_name and last_name != previous_last_name:
                    family_id += 1
                    previous_last_name = last_name
                household_id = str(family_id) if last_name else "1"

                remote_id = str(remote_id_counter)
                remote_id_counter += 1

                birthdate = format_birthdate(row.get("Birth Month and Day", ""), row.get("Age", ""), current_year)
                anniversary = format_anniversary(row.get("Wedding Month and Day", ""))

                medical_notes = row.get("Allergy", "").lower()
                if medical_notes == "no":
                    medical_notes = ""

                grade = map_grade(row.get("School Grade", ""))

                mobile_phone = format_phone(row.get("Cell Phone", ""))
                home_phone = format_phone(row.get("Home Phone", ""))
                work_phone = format_phone(row.get("Work Phone", ""))

                baptized = yes_no_to_true_false(row.get("Baptized", ""))

                status, membership = get_status_and_membership(row.get("Member Status", ""))

                authorized_pickup = "|".join(filter(None, [row.get(f"Authorized Pick up {i}", "") for i in range(1, 9)]))

                relationship = row.get("Relationship", "").lower()
                household_primary_contact = "TRUE" if "head of household" in relationship or row.get("Primary Contact", "").lower() == "yes" else ""

                emergency_contact = row.get("Emergency Contact", "")
                if not emergency_contact:
                    primary_contact = row.get("Primary Contact", "")
                    first_name = row.get("First Name", "").lower()
                    if primary_contact:
                        primary_first_name = primary_contact.split()[0].lower() if primary_contact.split() else ""
                        if primary_first_name != first_name:
                            emergency_contact = primary_contact
                        else:
                            emergency_contact = row.get("Secondary Contact", "")
                    else:
                        emergency_contact = row.get("Secondary Contact", "")

                output_row = {
                    "remote_id": remote_id,
                    "First Name": row.get("First Name", ""),
                    "Middle Name": row.get("Middle Name", ""),
                    "Last Name": last_name,
                    "Birthdate": birthdate,
                    "Anniversary": anniversary,
                    "Gender": row.get("Gender", ""),
                    "Grade": str(grade) if grade != "" else "",
                    "Medical Notes": medical_notes,
                    "Marital Status": row.get("Marital Status", ""),
                    "Status": status,
                    "Membership": membership,
                    "Home Address Street Line 1": row.get("Address", ""),
                    "Home Address City": row.get("City", ""),
                    "Home Address State": row.get("State", ""),
                    "Home Address Zip Code": row.get("Zip Code", ""),
                    "Mobile Phone Number": mobile_phone,
                    "Home Phone Number": home_phone,
                    "Work Phone Number": work_phone,
                    "Home Email": row.get("E-Mail", ""),
                    "Household ID": household_id,
                    "Household Name": f"{last_name} Household" if last_name else "",
                    "Household Primary Contact": household_primary_contact,
                    "Baptized": baptized,
                    "Baptism Date": row.get("Baptized Date", ""),
                    "Member By": row.get("How Joined", ""),
                    "Membership Date": row.get("Date Joined", ""),
                    "Sunday School": row.get("Sunday School", ""),
                    "Small Group": row.get("Activities", ""),
                    "Emergency Contact": emergency_contact,
                    "Emergency Phone": format_phone(row.get("Emergency Phone", "")),
                    "Allergies": row.get("Allergy", ""),
                    "Authorized Pickup": authorized_pickup
                }
                writer.writerow(output_row)
        click.echo(f"CSV transformation complete. Output saved to {output_file}")
    except Exception as e:
        click.echo(f"Error in create_import_csv: {e}", err=True)
