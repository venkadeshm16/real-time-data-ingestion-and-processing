#!/usr/bin/env python3

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.shared_config import PATIENT_IDS, ICU_DOCTORS, ICU_WARDS, CRITICAL_TREATMENTS

class TestSharedConfig:
    
    def test_patient_ids_count(self):
        assert len(PATIENT_IDS) == 1000
        assert PATIENT_IDS[0] == "P0001"
        assert PATIENT_IDS[-1] == "P1000"
    
    def test_icu_doctors_not_empty(self):
        assert len(ICU_DOCTORS) > 0
        assert all(doctor.startswith("Dr.") for doctor in ICU_DOCTORS)
    
    def test_icu_wards_format(self):
        assert len(ICU_WARDS) == 5
        assert all(ward.startswith("ICU-") for ward in ICU_WARDS)
    
    def test_critical_treatments_not_empty(self):
        assert len(CRITICAL_TREATMENTS) > 0
        assert isinstance(CRITICAL_TREATMENTS, list)