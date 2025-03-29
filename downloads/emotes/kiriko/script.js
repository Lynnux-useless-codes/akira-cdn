
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
