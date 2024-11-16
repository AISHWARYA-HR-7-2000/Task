# PDF Co-Viewer

A real-time co-viewer for PDF presentations, enabling multiple users to follow along with a PDF document in sync. This application allows an admin user to navigate through the PDF, with all connected viewers following the same page in real-time.

## Features

- *Admin Control*: Only the admin can navigate through the PDF slides. Viewers' pages are synchronized to the admin's actions.
- *Real-Time Synchronization*: As the admin changes the page, all viewers see the updated page immediately.
- *Navigation Buttons*: Viewers can't change the page manually, but the admin has full control over navigation using the "Previous" and "Next" buttons.
- *WebSocket Communication*: Uses Socket.IO to manage real-time communication and synchronization between the admin and viewers.

## Technologies Used

- *Frontend*: HTML, CSS, and JavaScript (Socket.IO for real-time communication)
- *Backend*: Python (FastAPI, Socket.IO for WebSocket handling)
- *PDF Parsing*: PyPDF2 to extract PDF information like the number of pages
- *WebSocket*: Socket.IO to handle real-time communication

## Requirements

To run the project, you will need to install the following dependencies:


pip install -r requirements.txt

uvicorn main:app --reload

Visit http://127.0.0.1:8000 to access the PDF co-viewer.
Multiple users can open the same link to join the session.
The admin user can set themselves as the admin, which will allow them to control the page navigation for all viewers.

The admin can click on "Set Admin" to become the presenter.
The admin can then navigate through the PDF using the "Previous" and "Next" buttons.
All connected viewers will follow the admin's actions and see the same page in real-time.
