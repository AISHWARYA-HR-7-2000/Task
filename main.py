import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio
from PyPDF2 import PdfReader

app = FastAPI()

# Create a Socket.IO server instance
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio)

# Mount the Socket.IO application on the FastAPI app
app.mount('/socket.io', socket_app)

# Mount static files (e.g., PDFs)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track the current page
current_page = 1
admin_sid = None

# Function to calculate the total number of pages
def get_total_pages(pdf_path):
    reader = PdfReader(pdf_path)
    return len(reader.pages)

total_pages = get_total_pages("static/sample.pdf")

@app.get("/", response_class=HTMLResponse)
def index():
    """Render the PDF viewer frontend"""
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

# Socket.IO Events
@sio.event
async def set_admin(sid):
    global admin_sid
    admin_sid = sid
    print(f"Admin set to: {sid}")  # Debugging line
    
    # Emit event to disable set admin button in other tabs
    await sio.emit("admin_set", room='all_clients')
    
    # Emit event to disable navigation buttons for other users
    await sio.emit("disable_navigation", room='all_clients')
    
    # Enable navigation buttons for admin
    await sio.emit("enable_navigation_for_admin", to=sid)

@sio.event
async def change_page(sid, action_or_page):
    global current_page
    if sid == admin_sid:  # Only admin can change the page
        if isinstance(action_or_page, str):
            if action_or_page == 'next' and current_page < total_pages:
                current_page += 1
            elif action_or_page == 'previous' and current_page > 1:
                current_page -= 1
        else:
            current_page = min(max(1, action_or_page), total_pages)

        print(f"Admin {sid} changed page to: {current_page}")  # Debugging line

        # Emit to all connected clients to sync page
        await sio.emit("sync_page", current_page)  # Send the updated page to all users
        
        # Update navigation buttons for admin and others
        await sio.emit("update_navigation_for_admin", current_page, to=sid)
        await sio.emit("update_navigation_for_others", current_page, room='all_clients', skip_sid=sid)

@sio.event
async def connect(sid, environ):
    print(f"User connected: {sid}")  # Debugging line
    await sio.emit("sync_page", current_page, to=sid)
    await sio.emit("total_pages", total_pages, to=sid)
    await sio.enter_room(sid, 'all_clients')  # Join all clients to a room

@sio.event
async def disconnect(sid):
    global admin_sid
    print(f"User disconnected: {sid}")  # Debugging line
    await sio.leave_room(sid, 'all_clients')  # Leave

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)