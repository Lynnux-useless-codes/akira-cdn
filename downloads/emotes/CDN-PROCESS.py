from PIL import Image
import os
import json

# Function to rename .txt files in a directory
def rename_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # Remove everything before the first hyphen
            new_filename = filename.split('-', 1)[-1].strip()

            # Remove the extension if it exists
            new_filename = os.path.splitext(new_filename)[0]

            new_path = os.path.join(directory, new_filename + '.txt')
            os.rename(os.path.join(directory, filename), new_path)
            print(f"Renamed {filename} to {new_filename}.txt")

# Function to rename .ogg files in a directory
def rename_ogg_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.ogg'):
            new_filename = filename.split('-', 1)[-1].strip()  # Remove everything before the first hyphen
            new_path = os.path.join(directory, new_filename)
            os.rename(os.path.join(directory, filename), new_path)
            print(f"Renamed {filename} to {new_filename}")

# Function to convert .tif files to .png and delete the original .tif
def convert_tif_to_png(directory):
    for file in os.listdir(directory):
        if file.endswith('.tif'):
            tif_path = os.path.join(directory, file)
            png_path = os.path.splitext(tif_path)[0] + '.png'

            try:
                im = Image.open(tif_path)
                im.save(png_path)
                os.remove(tif_path)  # Delete the original .tif file
                print(f"Converted {tif_path} to {png_path} and removed original")
            except Exception as e:
                print(f"Failed to convert {tif_path}: {str(e)}")

# Function to generate directory listing and save it as JSON
def generate_directory_listing(directory):
    listing = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.isdir(item_path):
            item_type = "&lt;DIRECTORY&gt;" if os.path.isdir(item_path) else os.path.splitext(item)[1].upper() + " file"
            item_size = "N/A" if os.path.isdir(item_path) else f"{os.path.getsize(item_path) / 1024:.2f} KB"
            item_date_modified = os.path.getmtime(item_path)
            relative_path = os.path.relpath(item_path, root_directory)
            listing.append({
                "name": os.path.basename(relative_path.replace("\\", "/")),  # Use os.path.basename to get only the filename
                "type": item_type,
                "size": item_size,
                "dateModified": item_date_modified
            })
    return listing

# HTML (index.html) as a Python string
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="/images/my-avatar_120.webp">
    <title>CDN - Lynnux</title>
    <link rel="stylesheet" type="text/css" href="/style.css">

    <!-- Discord Embed -->
    <meta property="og:title" content="Reaction Images" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="http://cdn.lynnux.xyz/Reactions/" />
    <meta name="theme-color" content="#ff47ff">
    <meta name="twitter:card" content="summary_large_image">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YSD2Q72W1H"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-YSD2Q72W1H');
    </script>
</head>
<body>
    <h1 id="fileLocation">/ParentDirectory/CurrentDirectory/</h1>
    <div id="container">
        <table class="sortable">
            <thead>
                <tr >
                    <th>Filename</th>
                    <th>Type</th>
                    <th>Size</th>
                    <th>Date Modified</th>
                </tr>
            </thead>
            <tr class='directory'>
                <td><a href='../' class='name'>...</a></td>
                <td><a href='../'>&lt;GO BACK&gt;</a></td>
                <td sorttable_customkey='1'><a href='../'>N/A</a></td>
                <td sorttable_customkey='1'><a href='../'>N/A</a></td>
            </tr>
            <tbody id="fileList"></tbody>
        </table>
    </div>
    <button id="mode-toggle">
        <ion-icon name="moon-outline"></ion-icon>
    </button>
    <script src="script.js"></script>
    <script src="/mode.js"></script>
</body>
<script>
    // Get the current URL of the page
    var url = window.location.href;

    // Extract the parent directory and directory names from it
    var parent_directory = url.split("/").slice(-3, -2)[0];
    var directory = url.split("/").slice(-2, -1)[0];

    // Set the content of the h1 element to the desired value
    var fileLocation = document.getElementById("fileLocation");
    fileLocation.innerHTML = "/" + parent_directory + "/" + directory + "/";
</script>
</html>
"""

# JavaScript (script.js) as a Python string
js_content = """
// Function to convert size from KB to bytes and remove letters
function convertSizeToBytes(size) {
    // Remove any non-numeric characters (letters, spaces, etc.)
    const numericString = size.replace(/[^0-9.]/g, '');
    // Convert the numeric string to a floating-point number
    const numericValue = parseFloat(numericString);
    // Check if the size string contains 'KB' and convert to bytes
    if (size.toLowerCase().includes('kb')) {
        return numericValue * 1024; // 1 KB = 1024 bytes
    } else {
        return numericValue; // Already in bytes or unknown format
    }
}

// script.js
function displayDirectoryListing() {
    console.log("Fetching JSON data...")
    const fileList = document.getElementById('fileList');
    fetch('output.json')
        .then(response => response.json())
        .then(data => {
            const filteredFiles = data.filter(item => !item.name.endsWith('.html') && !item.name.endsWith('.json') && !item.name.endsWith('.psd') && !item.name.endsWith('.py') && !item.name.endsWith('.js'));

            filteredFiles.forEach(item => {
                const itemName = item.name.split('/').pop();
                const sizeInBytes = convertSizeToBytes(item.size);
0
                // Check if it's a directory or a file
                const isDirectory = item.type === "Directory";
                const typeText = isDirectory ? "<DIRECTORY>" : `${item.type.toUpperCase()} file`;

                // Check if the item is not in a subdirectory
                const isFileInSubdirectory = item.name.split('/').length > 1;

                if (!isFileInSubdirectory) {
                    const row = document.createElement('tr');
                    const typeClass = isDirectory ? "folder" : "image";
                    row.innerHTML = `
                        <td><a class="name">${itemName}</a></td>
                        <td><a class="${typeClass}">${item.type}</a></td>
                        <td sorttable_customkey="${sizeInBytes}"><a>${item.size}</a></td>
                        <td sorttable_customkey="${item.dateModified}"><a>${new Date(item.dateModified * 1000).toLocaleString()}</a></td>
                    `;

                    // Add an event listener to the table row to make it clickable
                    row.addEventListener('click', function () {
                        // Get the filename from the first cell of the clicked row
                        const fileName = row.querySelector('td:first-child').textContent;

                        // If it's not an HTML or JSON file, navigate to it (replace 'your_base_url' with your actual base URL)
                        if (!fileName.endsWith('.html') && !fileName.endsWith('.json')) {
                            const fileUrl = `./${fileName}`; // Construct the URL
                            window.location.href = fileUrl; // Navigate to the URL
                        }
                    });

                    fileList.appendChild(row);
                }
            });
        })
        .catch(error => console.error(error));
}

displayDirectoryListing();
"""

# Function to process a directory and its subdirectories recursively
def process_directory(directory):
    # Rename .ogg files
    rename_ogg_files(directory)
    
    # Convert .tif to .png and delete original .tif
    convert_tif_to_png(directory)

    # Generate and save directory listing as JSON
    directory_data = generate_directory_listing(directory)
    output_json_file = os.path.join(directory, 'output.json')
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(directory_data, json_file, indent=4)
        print(f'Directory listing data has been generated and saved to {output_json_file}')

    # Create Index.html
    html_file_path = os.path.join(directory, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
        print(f'HTML file has been generated and saved to {html_file_path}')

    # Create Script.js
    js_file_path = os.path.join(directory, 'script.js')
    with open(js_file_path, 'w', encoding='utf-8') as js_file:
        js_file.write(js_content)
        print(f'JavaScript file has been generated and saved to {js_file_path}')

    # Recursively process subdirectories
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            process_directory(subdir_path)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    root_directory = os.path.join(current_directory)

    # Start processing the main directory and its subdirectories
    process_directory(root_directory)
    # rename_txt_files(root_directory)
