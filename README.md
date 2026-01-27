💰 Expense Tracker (Python Desktop App)

A modern desktop-based Expense Tracker built using Python (Tkinter) that allows users to record, manage, and visualize daily expenses.
The application provides real-time summaries, category-wise analysis, and interactive charts for better financial awareness.

🎯 Built by Akshay S

✨ Features

➕ Add new expenses with:

Amount

Category

Date

Description

🗑️ Delete selected expenses

📊 Visual analytics using Matplotlib:

Category-wise expense distribution

Spending trends

📈 Smart summary dashboard:

Total expenses

Current month spending

Most spent category

Average daily expense

💾 Persistent storage using JSON file

🖥️ Clean and modern GUI using Tkinter + ttk styling

🛠️ Tech Stack

Language: Python

GUI Framework: Tkinter (ttk)

Data Storage: JSON (expenses.json)

Visualization: Matplotlib

Date Handling: datetime module

📂 Project Structure
expense-tracker/
│
├── expense_tracker.py      # Main application file
├── expenses.json           # Stored expense data (auto-created)
├── README.md               # Project documentation

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker

2️⃣ Install required libraries
pip install matplotlib


(Tkinter comes pre-installed with Python)

3️⃣ Run the application
python expense_tracker.py

🧠 How the Application Works

User adds an expense via the GUI

Data is saved automatically to expenses.json

Expense table updates instantly

Charts and summaries refresh in real time

User can delete any selected entry


🚀 Future Enhancements

📅 Date range filters

📤 Export expenses to CSV / Excel

🔐 User authentication

☁️ Cloud database support

📱 Mobile / Web version

🤝 Contributing

Contributions are welcome!
Feel free to fork this repository and submit pull requests.

