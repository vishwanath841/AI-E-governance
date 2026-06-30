"""
Database initialization script for JanSahayak AI.
This script creates the database tables and populates them with sample data.
"""

from app.core.database import Base, engine, SessionLocal
from app.models import User, Document, Scheme, Application, AuditLog
import json

def init_database():
    """Initialize the database with tables and sample data."""
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if schemes already exist
        existing_schemes = db.query(Scheme).count()
        if existing_schemes > 0:
            print("Sample data already exists. Skipping data insertion.")
            return
        
        # Insert sample schemes
        print("Inserting sample schemes...")
        sample_schemes = [
            Scheme(
                scheme_name="Pradhan Mantri Awas Yojana",
                description="Housing for All scheme to provide affordable housing to the urban poor",
                eligibility_rules=json.dumps({
                    "max_income": 300000,
                    "residence_type": ["rural", "urban"],
                    "no_pucca_house": True
                }),
                benefits="Financial assistance for constructing houses",
                required_documents=json.dumps(["aadhaar_card", "income_certificate", "residence_proof"]),
                min_income=0,
                max_income=300000,
                age_requirement=18,
                is_active=1
            ),
            Scheme(
                scheme_name="National Health Protection Scheme",
                description="Health insurance scheme providing coverage of up to ₹5 lakh per family per year",
                eligibility_rules=json.dumps({
                    "max_income": 500000,
                    "is_bpl": True
                }),
                benefits="Health coverage for secondary and tertiary care hospitalization",
                required_documents=json.dumps(["aadhaar_card", "bpl_card", "bank_statement"]),
                min_income=0,
                max_income=500000,
                age_requirement=0,
                is_active=1
            ),
            Scheme(
                scheme_name="Scholarship for Higher Education",
                description="Scholarship scheme for meritorious students from economically weaker sections",
                eligibility_rules=json.dumps({
                    "max_income": 800000,
                    "age_max": 25,
                    "min_marks": 80
                }),
                benefits="Financial assistance for higher education",
                required_documents=json.dumps(["aadhaar_card", "income_certificate", "mark_sheets", "bank_statement"]),
                min_income=0,
                max_income=800000,
                age_requirement=0,
                is_active=1
            ),
            Scheme(
                scheme_name="Old Age Pension Scheme",
                description="Monthly pension for senior citizens below poverty line",
                eligibility_rules=json.dumps({
                    "min_age": 60,
                    "max_income": 200000,
                    "is_bpl": True
                }),
                benefits="Monthly pension of ₹500-₹1000",
                required_documents=json.dumps(["aadhaar_card", "bpl_card", "age_proof", "bank_statement"]),
                min_income=0,
                max_income=200000,
                age_requirement=60,
                is_active=1
            ),
            Scheme(
                scheme_name="Disability Support Scheme",
                description="Financial assistance and support for persons with disabilities",
                eligibility_rules=json.dumps({
                    "has_disability": True,
                    "disability_certificate": True
                }),
                benefits="Monthly pension and assistive devices",
                required_documents=json.dumps(["aadhaar_card", "disability_certificate", "income_certificate", "bank_statement"]),
                min_income=0,
                max_income=0,
                age_requirement=0,
                is_active=1
            ),
            Scheme(
                scheme_name="Mahatma Gandhi National Rural Employment Guarantee Act",
                description="Guarantee of 100 days of wage employment in a financial year to rural households",
                eligibility_rules=json.dumps({
                    "residence_type": ["rural"],
                    "adult_members": True
                }),
                benefits="100 days of wage employment per year",
                required_documents=json.dumps(["aadhaar_card", "bank_statement", "residence_proof"]),
                min_income=0,
                max_income=0,
                age_requirement=18,
                is_active=1
            ),
            Scheme(
                scheme_name="Pradhan Mantri Jan Dhan Yojana",
                description="Financial inclusion program ensuring access to financial services",
                eligibility_rules=json.dumps({
                    "no_bank_account": True
                }),
                benefits="Bank account with debit card and insurance cover",
                required_documents=json.dumps(["aadhaar_card", "passport_photo"]),
                min_income=0,
                max_income=0,
                age_requirement=0,
                is_active=1
            ),
            Scheme(
                scheme_name="Ujjwala Yojana",
                description="Providing clean cooking fuel (LPG) to BPL households",
                eligibility_rules=json.dumps({
                    "is_bpl": True,
                    "no_lpg_connection": True
                }),
                benefits="Free LPG connection and subsidy",
                required_documents=json.dumps(["aadhaar_card", "bpl_card", "bank_statement", "residence_proof"]),
                min_income=0,
                max_income=0,
                age_requirement=18,
                is_active=1
            )
        ]
        
        db.add_all(sample_schemes)
        db.commit()
        print(f"Inserted {len(sample_schemes)} sample schemes!")
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
