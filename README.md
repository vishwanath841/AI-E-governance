# JanSahayak AI - Government Welfare Assistant

A secure multi-agent government welfare assistant powered by ArmorIQ security layer. This MVP enables citizens to discover, verify, and apply for government welfare schemes through an AI-powered interface.

## 🚀 Features

### Core Functionality
- **AI-Powered Chat Interface**: Interactive chat with the Coordinator Agent for personalized assistance
- **Multi-Agent System**: 6 specialized agents working together with security oversight
- **Document Verification**: Upload and verify documents using OCR technology
- **Scheme Eligibility**: Intelligent matching of welfare schemes based on citizen profile
- **Application Management**: Complete application lifecycle from draft to approval
- **Real-time Audit Dashboard**: Monitor all agent actions with ArmorIQ security logging

### Security Features (ArmorIQ)
- **Action Verification**: Every agent action is verified before execution
- **Permission Control**: Granular permissions for each agent type
- **Audit Logging**: Complete traceability of all system actions
- **Unauthorized Action Blocking**: Automatic blocking of unauthorized actions
- **Real-time Monitoring**: Live dashboard of security events

### User Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Clean UI/UX**: Modern interface built with Tailwind CSS
- **Real-time Updates**: Live status updates for applications and documents
- **Multi-language Support**: Ready for regional language integration

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Authentication**: JWT (JSON Web Tokens)
- **OCR**: Tesseract
- **File Storage**: Local filesystem (MVP)
- **LLM Integration**: OpenAI API (optional)

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Icons**: Lucide React

### DevOps
- **Containerization**: Docker & Docker Compose
- **Database Management**: PostgreSQL
- **API Documentation**: FastAPI auto-generated docs

## 📋 Prerequisites

### For Docker Setup (Recommended)
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose

### For Manual Setup
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- pip (Python package manager)
- npm (Node package manager)

## 🚀 Installation

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd blr
```

2. **Configure environment variables**
```bash
# Copy example environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit backend/.env and add your configurations
# Edit frontend/.env.local if needed
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and secret keys
```

5. **Start PostgreSQL**
```bash
# Make sure PostgreSQL is running and create database
createdb jansahayak
```

6. **Run the backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env.local
# Edit .env.local if needed
```

4. **Run the frontend**
```bash
npm run dev
```

## ⚙️ Configuration

### Backend Environment Variables (.env)

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jansahayak

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your-openai-api-key-here

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# Application
APP_NAME=JanSahayak AI
APP_VERSION=1.0.0
```

### Frontend Environment Variables (.env.local)

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Application
NEXT_PUBLIC_APP_NAME=JanSahayak AI
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## 📊 Project Structure

```
blr/
├── backend/
│   ├── app/
│   │   ├── agents/          # Multi-agent implementations
│   │   │   ├── base_agent.py
│   │   │   ├── coordinator_agent.py
│   │   │   ├── verification_agent.py
│   │   │   ├── document_agent.py
│   │   │   ├── eligibility_agent.py
│   │   │   ├── submission_agent.py
│   │   │   └── notification_agent.py
│   │   ├── api/             # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── documents.py
│   │   │   ├── schemes.py
│   │   │   ├── applications.py
│   │   │   ├── agents.py
│   │   │   └── audit.py
│   │   ├── core/            # Core functionality
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── armoriq.py   # Security middleware
│   │   ├── models/          # Database models
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   ├── scheme.py
│   │   │   ├── application.py
│   │   │   └── audit_log.py
│   │   └── schemas/         # Pydantic schemas
│   ├── uploads/             # File storage directory
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── .env                 # Environment variables
├── frontend/
│   ├── app/
│   │   ├── lib/             # Utility functions
│   │   │   ├── api.ts       # API client
│   │   │   └── auth-context.tsx
│   │   ├── page.tsx         # Landing page
│   │   ├── login/           # Login page
│   │   ├── profile/         # User profile page
│   │   ├── documents/       # Document management
│   │   ├── schemes/         # Scheme discovery
│   │   ├── applications/    # Application tracking
│   │   └── audit/           # Audit dashboard
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   ├── next.config.js       # Next.js configuration
│   ├── tailwind.config.js   # Tailwind configuration
│   ├── Dockerfile           # Docker configuration
│   └── .env.local           # Environment variables
├── docker-compose.yml       # Multi-container setup
└── README.md                # This file
```

## 🔌 API Documentation

Once the backend is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

#### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile

#### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - Get user documents
- `POST /api/documents/{id}/verify` - Verify document

#### Schemes
- `GET /api/schemes/` - Get all schemes
- `POST /api/schemes/check-eligibility` - Check eligibility

#### Applications
- `POST /api/applications/` - Create application
- `GET /api/applications/` - Get user applications
- `POST /api/applications/{id}/submit` - Submit application

#### Agents
- `POST /api/agents/query` - Process user query
- `GET /api/agents/status` - Get agent status

#### Audit
- `GET /api/audit/` - Get audit logs
- `GET /api/audit/summary` - Get audit summary

## 🤖 Multi-Agent System

### Agent Architecture

1. **Coordinator Agent**
   - Receives citizen queries
   - Creates execution plans
   - Delegates tasks to other agents
   - Manages workflow orchestration

2. **Verification Agent**
   - Validates Aadhaar ID format
   - Validates mobile number format
   - Performs identity verification

3. **Document Agent**
   - Handles document uploads
   - Extracts text using OCR
   - Verifies document authenticity
   - Manages document storage

4. **Eligibility Agent**
   - Analyzes citizen profiles
   - Matches eligible schemes
   - Calculates eligibility scores
   - Identifies missing documents

5. **Submission Agent**
   - Generates application forms
   - Handles application submission
   - Updates application status
   - Manages form data

6. **Notification Agent**
   - Sends status notifications
   - Manages communication channels
   - Tracks notification delivery
   - Read-only access to user data

### ArmorIQ Security Layer

The ArmorIQ middleware provides:
- **Action Verification**: All agent actions pass through security checks
- **Permission Management**: Each agent has specific allowed actions
- **Audit Logging**: Complete traceability of all actions
- **Unauthorized Blocking**: Automatic blocking of prohibited actions

Example of security in action:
```python
# If Notification Agent tries to modify user data
result = armoriq.invoke("notification_agent", "modify_aadhaar")
# Returns: {"success": False, "error": "Action not permitted", "result": "blocked"}
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📝 Database Schema

### Tables
- **users**: Citizen information
- **documents**: Uploaded documents and verification status
- **schemes**: Government welfare schemes
- **applications**: Scheme applications
- **audit_logs**: Security and action logs

## 🔒 Security Considerations

### Production Deployment
1. Change default JWT secret key
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Implement rate limiting
5. Add input validation
6. Use prepared statements for database queries
7. Enable CORS with specific origins
8. Implement request throttling
9. Add monitoring and alerting
10. Regular security audits

### ArmorIQ Best Practices
- Regularly review audit logs
- Monitor blocked actions
- Update agent permissions as needed
- Implement time-based access controls
- Add anomaly detection

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Manual Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run backend server
4. Build and serve frontend
5. Configure reverse proxy (nginx)
6. Enable SSL/TLS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API docs at /docs endpoint

## 🙏 Acknowledgments

- Built with FastAPI and Next.js
- Security inspired by modern agent architecture
- OCR powered by Tesseract
- Icons by Lucide

## 📈 Roadmap

### Phase 1 (Current MVP)
- ✅ Basic multi-agent system
- ✅ Document verification
- ✅ Scheme eligibility
- ✅ Application management
- ✅ Audit dashboard

### Phase 2 (Future Enhancements)
- [ ] Multi-language support
- [ ] Advanced OCR with handwriting recognition
- [ ] Integration with real government APIs
- [ ] Mobile applications (iOS/Android)
- [ ] Advanced analytics dashboard
- [ ] Machine learning for scheme matching
- [ ] Video KYC integration
- [ ] Blockchain for document verification

### Phase 3 (Advanced Features)
- [ ] Voice-activated assistant
- [ ] Regional language NLP
- [ ] Predictive analytics
- [ ] Integration with payment gateways
- [ ] Advanced fraud detection
- [ ] Real-time collaboration with government officials

---

**Note**: This is an MVP for demonstration purposes. For production use, additional security measures, scalability improvements, and compliance checks should be implemented.
