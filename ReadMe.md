# Email File Processor

### Overview

This repository contains a Django web application designed to upload CSV files containing email addresses, process them for validity, and provide functionality to download processed files. The application is equipped with features to handle file uploads, process the emails for validity, and allow users to download the processed files.

### Features

- **File Upload**: Users can upload CSV files containing email addresses.
- **Email Validation**: The application validates each email address in the uploaded file.
- **File Processing**: After validation, the application generates a processed CSV file with an additional column indicating the validity status of each email.
- **Download Functionality**: Users can download both the original and processed files.
- **Error Handling**: The application handles various error scenarios gracefully and provides feedback to users via messages.

### Components

- **index.html**: This template renders the main page of the application, allowing users to upload files and displaying the list of uploaded files.
- **views.py**: Contains Django view functions responsible for handling file upload, processing, deletion, and download operations.
- **models.py**: Defines the Django model for storing uploaded files.
- **validate_email.py**: Contains the email validation function using the `validate_email` library.
- **README.md**: This file provides documentation and instructions for setting up and running the application.

### Setup and Usage

1.  **Clone the Repository**: Clone the repository to your local machine.

    `git clone https://github.com/gargmegham/EmailValidator.git`

2.  **Install Dependencies**: Install the required Python dependencies listed in `requirements.txt`.

    `pip install -r requirements.txt`

3.  **Database Setup**: Configure the database settings in `settings.py` according to your database setup. Perform migrations to create necessary database tables.

    `python manage.py makemigrations python manage.py migrate`

4.  **Run the Server**: Start the Django development server.

    `python manage.py runserver`

5.  **Access the Application**: Visit `http://localhost:8000` in your web browser to access the application.

### Usage Instructions

- **File Upload**: Click on the "Choose File" button to select a CSV file containing email addresses. Click on "Upload" to upload the file.
- **File Processing**: Once uploaded, the application automatically processes the file, validates the email addresses, and generates a processed CSV file.
- **Download Files**: Users can download both the original and processed files by clicking on the respective download buttons.
- **Delete Files**: Uploaded files can be deleted by clicking on the delete button next to each file.

### Contribution Guidelines

Contributions to the repository are welcome. If you find any issues or would like to add new features, please follow these guidelines:

- Fork the repository and create a new branch for your feature or bug fix.
- Ensure that your code follows PEP 8 style guidelines.
- Submit a pull request with a clear description of the changes you have made.

[Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [meghamgarg@gmail.com](mailto:meghamgarg@gmail.com).
