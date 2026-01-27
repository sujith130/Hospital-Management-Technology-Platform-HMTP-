"""
Backend Health Check Script
Tests if the backend can start and basic functionality works
"""
import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_backend():
    """Test backend imports and basic functionality"""
    issues = []
    warnings = []
    
    print("=" * 60)
    print("BACKEND HEALTH CHECK")
    print("=" * 60)
    
    # Test 1: Import main app
    print("\n[1/8] Testing main app import...")
    try:
        from app.main import app
        print("   [OK] Main app imports successfully")
    except Exception as e:
        issues.append(f"Failed to import main app: {e}")
        print(f"   [FAIL] Failed: {e}")
        return issues, warnings
    
    # Test 2: Check all routers are registered
    print("\n[2/8] Checking router registration...")
    routes = [route.path for route in app.routes]
    expected_routes = [
        "/api/v1/auth",
        "/api/v1/patients",
        "/api/v1/doctors",
        "/api/v1/appointments",
        "/api/v1/pharmacy",
        "/api/v1/labs",
        "/api/v1/billing",
        "/api/v1/audit",
        "/api/v1/procedures"
    ]
    
    for route_prefix in expected_routes:
        if any(route.startswith(route_prefix) for route in routes):
            print(f"   [OK] {route_prefix} registered")
        else:
            warnings.append(f"Route prefix {route_prefix} not found")
            print(f"   [WARN] {route_prefix} not found")
    
    # Test 3: Check database configuration
    print("\n[3/8] Checking database configuration...")
    try:
        from app.core.config import settings
        print(f"   [OK] Database URL configured: {settings.async_database_url[:50]}...")
        if "sqlite" in settings.async_database_url:
            warnings.append("Using SQLite database (development mode)")
            print("   [WARN] Using SQLite (development mode)")
    except Exception as e:
        issues.append(f"Database config error: {e}")
        print(f"   [FAIL] Failed: {e}")
    
    # Test 4: Check all models can be imported
    print("\n[4/8] Testing model imports...")
    models_to_test = [
        ("app.auth.models", "User"),
        ("app.patients.models", "Patient"),
        ("app.doctors.models", "Doctor", "DoctorAvailability"),
        ("app.appointments.models", "Appointment"),
        ("app.pharmacy.models", "Medicine", "Prescription"),
        ("app.labs.models", "LabTest"),
        ("app.billing.models", "Invoice", "Payment", "InsuranceClaim"),
        ("app.audit.models", "AuditLog"),
        ("app.procedures.models", "Procedure"),
    ]
    
    for module_path, *model_names in models_to_test:
        try:
            module = __import__(module_path, fromlist=model_names)
            for model_name in model_names:
                if hasattr(module, model_name):
                    print(f"   [OK] {module_path}.{model_name}")
                else:
                    issues.append(f"Model {model_name} not found in {module_path}")
                    print(f"   [FAIL] {module_path}.{model_name} not found")
        except Exception as e:
            issues.append(f"Failed to import {module_path}: {e}")
            print(f"   [FAIL] {module_path}: {e}")
    
    # Test 5: Check schemas
    print("\n[5/8] Testing schema imports...")
    schemas_to_test = [
        "app.auth.schemas",
        "app.patients.schemas",
        "app.doctors.schemas",
        "app.appointments.schemas",
        "app.pharmacy.schemas",
        "app.labs.schemas",
        "app.billing.schemas",
        "app.audit.schemas",
        "app.procedures.schemas",
    ]
    
    for schema_path in schemas_to_test:
        try:
            __import__(schema_path)
            print(f"   [OK] {schema_path}")
        except Exception as e:
            issues.append(f"Failed to import {schema_path}: {e}")
            print(f"   [FAIL] {schema_path}: {e}")
    
    # Test 6: Check authentication dependencies
    print("\n[6/8] Testing authentication setup...")
    try:
        from app.auth.deps import get_current_user, oauth2_scheme
        from app.auth.security import create_access_token, verify_password, get_password_hash
        print("   [OK] Authentication dependencies available")
    except Exception as e:
        issues.append(f"Authentication setup error: {e}")
        print(f"   [FAIL] Failed: {e}")
    
    # Test 7: Check middleware
    print("\n[7/8] Testing middleware...")
    try:
        from app.core.middleware import MultiTenantMiddleware, get_current_hospital_id
        print("   [OK] Multi-tenant middleware available")
    except Exception as e:
        issues.append(f"Middleware error: {e}")
        print(f"   [FAIL] Failed: {e}")
    
    # Test 8: Check audit logging
    print("\n[8/8] Testing audit logging...")
    try:
        from app.core.audit import log_audit_event
        print("   [OK] Audit logging available")
    except Exception as e:
        issues.append(f"Audit logging error: {e}")
        print(f"   [FAIL] Failed: {e}")
    
    # Security checks
    print("\n" + "=" * 60)
    print("SECURITY CHECKS")
    print("=" * 60)
    
    from app.core.config import settings
    if settings.SECRET_KEY == "YOUR_SUPER_SECRET_KEY_HERE_CHANGE_IN_PRODUCTION":
        warnings.append("SECURITY: Default SECRET_KEY is being used")
        print("   [WARN] WARNING: Default SECRET_KEY detected")
    
    # Check procedures router doesn't use auth
    try:
        from app.procedures.router import router as proc_router
        # Check if routes use get_current_user
        route_deps = []
        for route in proc_router.routes:
            if hasattr(route, 'dependencies'):
                route_deps.extend([dep.dependency for dep in route.dependencies])
        
        from app.auth.deps import get_current_user
        if get_current_user not in route_deps:
            warnings.append("SECURITY: Procedures router doesn't require authentication")
            print("   [WARN] WARNING: Procedures router doesn't require authentication")
    except:
        pass
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if issues:
        print(f"\n[FAIL] CRITICAL ISSUES FOUND: {len(issues)}")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n[OK] No critical issues found")
    
    if warnings:
        print(f"\n[WARN] WARNINGS: {len(warnings)}")
        for warning in warnings:
            print(f"   - {warning}")
    else:
        print("\n[OK] No warnings")
    
    print("\n" + "=" * 60)
    
    return issues, warnings

if __name__ == "__main__":
    issues, warnings = asyncio.run(test_backend())
    
    if issues:
        print("\n[FAIL] BACKEND HAS CRITICAL ISSUES")
        sys.exit(1)
    elif warnings:
        print("\n[WARN] BACKEND WORKS BUT HAS WARNINGS")
        sys.exit(0)
    else:
        print("\n[OK] BACKEND IS HEALTHY")
        sys.exit(0)
