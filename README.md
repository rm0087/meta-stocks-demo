# MetaStocks

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy ORM
- **Frontend**: React
- **Database**: SQLite
- **Package Managers**: pipenv (for Python dependencies), npm (for Node.js dependencies)

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm
- pipenv

### Backend Setup

1. **Clone the repository**:
   ```bash
   fork MetaStocks to your repo
   git clone git@github.com:USERNAME/meta-stocks-demo.git
   cd meta-stocks-demo
   ```

2. **Install Python dependencies**:
   ```bash
   pipenv install
   ```

3. **Activate the pipenv shell**:
   ```bash
   pipenv shell
   ```

4. **Initialize the database**:
   ```bash
   cd server
   flask db init
   flask db migrate
   flask db upgrade
   ```

### Frontend Setup

1. **Navigate to the client directory**:
   ```bash
   cd ../client
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the React application**:
   ```bash
   npm start
   ```

   The application will run on `http://localhost:3000`.

## Usage

- **Accessing the Application**: Open your browser and go to `http://localhost:3000`.