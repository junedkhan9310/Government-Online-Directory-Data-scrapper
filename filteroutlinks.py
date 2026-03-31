import database
import csv
import time
# Initialize lists for tracking found and not found links
links_found = []
links_notfound = []

def processLink(link):
    try:
        link = link.strip()  # Remove whitespace/newlines
        # Remove http:// or https:// if present
        if '//' in link:
            link = link.split('//')[1]

        if "/" in link:
            link = link.partition('/')[0]


        if "www" in link:
            link = link.partition('.')[2]
        # Get the part up to the first dot
        # part = link.partition('.')
        return link # e.g., 'aaeacluster.'
    except Exception as e:
        print(f"Error processing link '{link}': {e}")
        return None


def read_links(file_path):
    """
    Reads links from a text file (one per line).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
        return links  # <- return the list directly, not nested
    except Exception as e:
        print(f"Error reading links file: {str(e)}")
        return []


def write_links_to_csv(links, filename):
    """
    Writes a list of links to a CSV file.
    """
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for link in links:
                writer.writerow([link])
    except Exception as e:
        print(f"Error writing to CSV: {filename}, Error: {str(e)}")


def main():
    links = read_links('finalized.txt')

    connection = None
    mycursor = None
    thread_id = None

    try:
        connection = database.DB_Connection2()
        mycursor = connection.cursor()
        thread_id = connection.thread_id()

        for link in links:
            skip_keywords = ['twitter', 'youtube', 'facebook', 'instagram']
            if any(keyword in link for keyword in skip_keywords):
                print("skipped:-", link)
                continue
            link_header = processLink(link)

            if not link_header:
                print(f"Could not process: {link}")
                continue

            # Prepare SQL query safely
            sql = """
                SELECT id 
                FROM dms_wpw_tenderlinks 
                WHERE tender_link LIKE %s 
                AND added_WPW != 'D' 
                LIMIT 1
            """
            like_pattern = f"%{link_header}%"
            mycursor.execute(sql, (like_pattern,))
            results = mycursor.fetchall()

            if len(results) > 0:
                links_found.append(link)
            else:
                print("Adding link",link)
                links_notfound.append(link)

    except Exception as e:
        database.print_exception_details(e)
        if thread_id:
            database.kill_query(thread_id)

    finally:
        if mycursor:
            mycursor.close()
        if connection:
            connection.close()

        # Write results to CSV files
        write_links_to_csv(links_found, "CSV's/alreadyhavelink.csv")
        write_links_to_csv(links_notfound, "CSV's/newlinks.csv")


main()
