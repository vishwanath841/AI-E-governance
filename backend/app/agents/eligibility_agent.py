import json
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent


class EligibilityAgent(BaseAgent):
    """
    Scheme Eligibility Agent - Analyzes citizen profiles and matches schemes.
    
    Responsibilities:
    - Analyze citizen profile
    - Match eligible schemes from database
    - Return eligibility score
    - Check missing documents
    """
    
    def __init__(self):
        super().__init__("eligibility_agent")
    
    def _perform_action(self, action: str, **kwargs) -> Any:
        """Perform eligibility-specific actions."""
        if action == "analyze_profile":
            return self._analyze_profile(kwargs.get("user_profile"))
        elif action == "match_schemes":
            return self._match_schemes(kwargs.get("user_profile"))
        elif action == "calculate_score":
            return self._calculate_eligibility_score(
                kwargs.get("user_profile"),
                kwargs.get("scheme")
            )
        elif action == "get_eligibility":
            return self._get_eligibility_details(
                kwargs.get("user_id"),
                kwargs.get("scheme_id")
            )
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _analyze_profile(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze citizen profile for scheme eligibility.
        
        Args:
            user_profile: Dictionary containing user information
            
        Returns:
            Dictionary containing profile analysis
        """
        analysis = {
            "user_id": user_profile.get("user_id"),
            "income_level": self._categorize_income(user_profile.get("income", 0)),
            "age_category": self._categorize_age(user_profile.get("age", 0)),
            "residence_type": user_profile.get("residence_type", "unknown"),
            "employment_status": user_profile.get("employment_status", "unknown"),
            "family_size": user_profile.get("family_size", 0),
            "has_disability": user_profile.get("has_disability", False),
            "is_bpl": user_profile.get("is_bpl", False)
        }
        
        return {
            "profile_analysis": analysis,
            "recommended_categories": self._get_recommended_categories(analysis)
        }
    
    def _categorize_income(self, income: int) -> str:
        """Categorize income level."""
        if income < 100000:
            return "very_low"
        elif income < 250000:
            return "low"
        elif income < 500000:
            return "middle"
        elif income < 1000000:
            return "high"
        else:
            return "very_high"
    
    def _categorize_age(self, age: int) -> str:
        """Categorize age group."""
        if age < 18:
            return "minor"
        elif age < 30:
            return "young_adult"
        elif age < 50:
            return "adult"
        elif age < 60:
            return "senior"
        else:
            return "elderly"
    
    def _get_recommended_categories(self, analysis: Dict[str, Any]) -> List[str]:
        """Get recommended scheme categories based on profile."""
        categories = []
        
        if analysis["income_level"] in ["very_low", "low"]:
            categories.append("income_support")
        
        if analysis["is_bpl"]:
            categories.append("bpl_welfare")
        
        if analysis["age_category"] == "elderly":
            categories.append("senior_citizen")
        
        if analysis["has_disability"]:
            categories.append("disability_support")
        
        if analysis["family_size"] > 5:
            categories.append("large_family_support")
        
        return categories
    
    def _match_schemes(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match eligible schemes based on user profile.
        
        Args:
            user_profile: Dictionary containing user information
            
        Returns:
            Dictionary containing matched schemes
        """
        # In a real implementation, this would query the database
        # For MVP, we'll return mock scheme matches
        
        profile_analysis = self._analyze_profile(user_profile)
        recommended_categories = profile_analysis["recommended_categories"]
        
        # Mock scheme database
        all_schemes = [
            {
                "id": 1,
                "scheme_name": "Pradhan Mantri Awas Yojana",
                "category": "housing",
                "eligibility_rules": {
                    "max_income": 300000,
                    "residence_type": ["rural", "urban"]
                }
            },
            {
                "id": 2,
                "scheme_name": "National Health Protection Scheme",
                "category": "healthcare",
                "eligibility_rules": {
                    "max_income": 500000,
                    "is_bpl": True
                }
            },
            {
                "id": 3,
                "scheme_name": "Scholarship for Higher Education",
                "category": "education",
                "eligibility_rules": {
                    "max_income": 800000,
                    "age_max": 25
                }
            },
            {
                "id": 4,
                "scheme_name": "Old Age Pension Scheme",
                "category": "senior_citizen",
                "eligibility_rules": {
                    "min_age": 60,
                    "max_income": 200000
                }
            },
            {
                "id": 5,
                "scheme_name": "Disability Support Scheme",
                "category": "disability_support",
                "eligibility_rules": {
                    "has_disability": True
                }
            }
        ]
        
        # Filter schemes based on user profile
        matched_schemes = []
        for scheme in all_schemes:
            eligibility_result = self._calculate_eligibility_score(user_profile, scheme)
            if eligibility_result["is_eligible"]:
                matched_schemes.append({
                    "scheme": scheme,
                    "eligibility": eligibility_result
                })
        
        # Sort by eligibility score
        matched_schemes.sort(key=lambda x: x["eligibility"]["score"], reverse=True)
        
        return {
            "total_schemes": len(matched_schemes),
            "matched_schemes": matched_schemes,
            "categories": recommended_categories
        }
    
    def _calculate_eligibility_score(self, user_profile: Dict[str, Any], scheme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate eligibility score for a specific scheme.
        
        Args:
            user_profile: User profile information
            scheme: Scheme information
            
        Returns:
            Dictionary containing eligibility score and details
        """
        rules = scheme.get("eligibility_rules", {})
        score = 0
        max_score = 100
        reasons = []
        missing_documents = []
        
        # Check income eligibility
        if "max_income" in rules:
            user_income = user_profile.get("income", 0)
            if user_income <= rules["max_income"]:
                score += 30
            else:
                reasons.append("Income exceeds maximum limit")
        
        # Check age eligibility
        if "min_age" in rules:
            user_age = user_profile.get("age", 0)
            if user_age >= rules["min_age"]:
                score += 25
            else:
                reasons.append("Age below minimum requirement")
        
        if "age_max" in rules:
            user_age = user_profile.get("age", 0)
            if user_age <= rules["age_max"]:
                score += 25
            else:
                reasons.append("Age above maximum limit")
        
        # Check BPL status
        if "is_bpl" in rules:
            if user_profile.get("is_bpl", False) == rules["is_bpl"]:
                score += 20
            else:
                reasons.append("BPL status mismatch")
        
        # Check disability
        if "has_disability" in rules:
            if user_profile.get("has_disability", False) == rules["has_disability"]:
                score += 20
            else:
                reasons.append("Disability requirement not met")
        
        # Check required documents
        required_docs = scheme.get("required_documents", [])
        user_docs = user_profile.get("documents", [])
        
        for doc in required_docs:
            if doc not in user_docs:
                missing_documents.append(doc)
                score -= 10
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return {
            "is_eligible": score >= 50,  # Eligible if score >= 50%
            "score": score,
            "max_score": max_score,
            "reasons": reasons,
            "missing_documents": missing_documents
        }
    
    def _get_eligibility_details(self, user_id: int, scheme_id: int) -> Dict[str, Any]:
        """
        Get detailed eligibility information for a specific scheme.
        
        Args:
            user_id: The user ID
            scheme_id: The scheme ID
            
        Returns:
            Dictionary containing detailed eligibility information
        """
        # In a real implementation, this would query the database
        return {
            "user_id": user_id,
            "scheme_id": scheme_id,
            "message": "Eligibility details retrieved"
        }
