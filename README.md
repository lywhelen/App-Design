# Tracklist

Get into the groove-- turn your study session into a vinyl record.

## Links
- **Frontend Repo:** https://github.com/yaraibrahimm/hackchallenge-frontend
- **Backend Repo:** https://github.com/lywhelen/App-Design

## Screenshots
<img width="359" height="781" alt="Screenshot 2026-05-02 at 12 05 06 AM" src="https://github.com/user-attachments/assets/0e13df90-4f3b-4236-b108-f9bbcceb0d02" />

<img width="357" height="780" alt="Screenshot 2026-05-02 at 12 05 34 AM" src="https://github.com/user-attachments/assets/22921ee4-ab3c-4d8e-9c3c-f0dc502a7762" />

<img width="359" height="777" alt="Screenshot 2026-05-02 at 12 04 21 AM" src="https://github.com/user-attachments/assets/734821fe-65ac-4a99-b90d-000020024f38" />


## About
Tracklist is a music-themed iOS study app that gamifies task completion through a vinyl record progress ring. Every task you add becomes a track on the record — as you complete them, the ring fills. When all tasks are done, Side A is complete.

## Features
- Vinyl record progress ring showing overall completion percentage
- Expandable music player UI on each task with a real time countdown timer and scrubbable progress bar
- Record scratch haptic animation when timer runs out, with options to mark complete, add time, continue, or edit
- Task creation and editing with time estimates in 30 minute increments, with priority markers and auto-calculated points
- On completion, task crosses out and moves to bottom, vinyl ring fills up, with spinning disc animation and music notes



## Requirements
- **SwiftUI:** Built entirely in SwiftUI using stacks, navigation, sheets, and custom components
- **Navigation:** NavigationStack with NavigationLink between dashboard, task creation, and edit screens
- **@State / @Binding / @ObservedObject:** Task state managed via @State and @Binding flowing through all views, with TaskViewModel as an ObservableObject
- **Networking:** URLSession used in NetworkManager to communicate with backend — supports GET, POST, PUT, and DELETE requests with JSON encoding/decoding
- **Data persistence:** Tasks and user data persisted on the backend and synced

## Notes
- The vinyl record, progress ring, music player UI, and record scratch animation are all custom built
- Haptic feedback is used throughout to enhance the music theme
- Backend repo linked above handles user accounts, task management, and the points/track system
