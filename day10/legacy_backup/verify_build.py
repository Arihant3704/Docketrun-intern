import sys
import os

try:
    print("Importing labeler_app...")
    import labeler_app.main
    from labeler_app.controller import AppController
    from labeler_app.core.schema import ObjectMeta
    
    print("Instantiating Controller...")
    ctrl = AppController()
    
    print("Checking Core Managers...")
    assert ctrl.am is not None
    assert ctrl.pm is not None
    assert ctrl.tm is not None
    
    print("Testing Annotation Manager...")
    ctrl.am.add_object(1, "test_class", (255, 0, 0))
    assert 1 in ctrl.am.objects
    
    print("Build Verified Successfully.")
except Exception as e:
    print(f"VERIFICATION FAILED: {e}")
    sys.exit(1)
